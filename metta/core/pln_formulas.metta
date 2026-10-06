;; ====================================================================
;; PLN Core Inference Formulas (Audited against official trueagi-io/pln)
;; ====================================================================

;; --------------------------------------------------------------------
;; Consistency Conditions from PLN book / lib_pln.metta
;; --------------------------------------------------------------------
(: smallest-intersection-probability (-> Number Number Number))
(= (smallest-intersection-probability $As $Bs)
   (clamp (/safe (- (+ $As $Bs) 1.0) $As) 0.0 1.0))

(: largest-intersection-probability (-> Number Number Number))
(= (largest-intersection-probability $As $Bs)
   (clamp (/safe $Bs $As) 0.0 1.0))

(: conditional-probability-consistency (-> Number Number Number Bool))
(= (conditional-probability-consistency $As $Bs $ABs)
   (and (< 0.0 $As)
        (and (<= (smallest-intersection-probability $As $Bs) $ABs)
             (<= $ABs (largest-intersection-probability $As $Bs)))))

;; --------------------------------------------------------------------
;; 1. PLN Deduction Formula
;; --------------------------------------------------------------------

;; Full 5-argument formula from official lib_pln.metta:
;; Takes priors P, Q, R and conditionals (P -> Q), (Q -> R)
(: Truth_Deduction_Full (-> TruthValue TruthValue TruthValue TruthValue TruthValue TruthValue))
(= (Truth_Deduction_Full (stv $Ps $Pc)
                         (stv $Qs $Qc)
                         (stv $Rs $Rc)
                         (stv $PQs $PQc)
                         (stv $QRs $QRc))
   (if (and (conditional-probability-consistency $Ps $Qs $PQs)
            (conditional-probability-consistency $Qs $Rs $QRs))
       (stv (if (< 0.9999 $Qs)
                $Rs
                (+ (* $PQs $QRs) (/safe (* (- 1.0 $PQs) (- $Rs (* $Qs $QRs))) (- 1.0 $Qs))))
            (* (* $PQs $QRs) (* $PQc $QRc)))
       (stv 1.0 0.0)))

;; Operational 2-argument chaining formula (unconditioned default prior):
(: Truth_Deduction (-> TruthValue TruthValue TruthValue))
(= (Truth_Deduction (stv $s1 $c1) (stv $s2 $c2))
   (let* (($s (clamp (* $s1 $s2) 0.0 1.0))
          ($c (clamp (* (* $s1 $s2) (* $c1 $c2)) 0.0 1.0)))
     (stv $s $c)))

;; --------------------------------------------------------------------
;; 2. PLN Modus Ponens Formula (lib_pln.metta)
;; Incorporates background base rate P(Q | ~P) = 0.02
;; --------------------------------------------------------------------
(: Truth_ModusPonens (-> TruthValue TruthValue TruthValue))
(= (Truth_ModusPonens (stv $sP $cP) (stv $sImp $cImp))
   (let* (($s (clamp (+ (* $sP $sImp) (* 0.02 (- 1.0 $sP))) 0.0 1.0))
          ($c (clamp (* (* $sP $sImp) (* $cP $cImp)) 0.0 1.0)))
     (stv $s $c)))

;; --------------------------------------------------------------------
;; 3. PLN Revision Formula (lib_pln.metta)
;; Fuses two independent estimates of the same statement.
;; --------------------------------------------------------------------
(: Truth_Revision (-> TruthValue TruthValue TruthValue))
(= (Truth_Revision (stv $s1 $c1) (stv $s2 $c2))
   (let* (($w1 (Truth_c2w $c1))
          ($w2 (Truth_c2w $c2))
          ($wTotal (+ $w1 $w2))
          ($sNumerator (+ (* $s1 $w1) (* $s2 $w2)))
          ($s (clamp (/safe $sNumerator $wTotal) 0.0 1.0))
          ($c (clamp (Truth_w2c $wTotal) 0.0 0.999999)))
     (stv $s $c)))

;; --------------------------------------------------------------------
;; 4. PLN Induction Formula (lib_pln.metta Appendix A)
;; Given: B -> A, B -> C |- A -> C
;; --------------------------------------------------------------------
(: Truth_Induction_Full (-> TruthValue TruthValue TruthValue TruthValue TruthValue TruthValue))
(= (Truth_Induction_Full (stv $sA $cA)
                         (stv $sB $cB)
                         (stv $sC $cC)
                         (stv $sBA $cBA)
                         (stv $sBC $cBC))
   (stv (clamp (+ (/safe (* (* $sBA $sBC) $sB) $sA)
                  (* (- 1.0 (/safe (* $sBA $sB) $sA))
                     (/safe (- $sC (* $sB $sBC)) (- 1.0 $sB))))
               0.0 1.0)
        (clamp (Truth_w2c (* (* $sBC $cBC) $cBA)) 0.0 1.0)))

;; Operational 2-argument induction (assuming equal base rates):
(: Truth_Induction (-> TruthValue TruthValue TruthValue))
(= (Truth_Induction (stv $sBA $cBA) (stv $sBC $cBC))
   (let* (($s (clamp (* $sBA $sBC) 0.0 1.0))
          ($c (clamp (Truth_w2c (* (* $sBC $cBC) $cBA)) 0.0 1.0)))
     (stv $s $c)))

;; --------------------------------------------------------------------
;; 5. PLN Abduction Formula (lib_pln.metta Appendix A)
;; Given: A -> B, C -> B |- A -> C
;; --------------------------------------------------------------------
(: Truth_Abduction_Full (-> TruthValue TruthValue TruthValue TruthValue TruthValue TruthValue))
(= (Truth_Abduction_Full (stv $sA $cA)
                         (stv $sB $cB)
                         (stv $sC $cC)
                         (stv $sAB $cAB)
                         (stv $sCB $cCB))
   (stv (clamp (+ (/safe (* (* $sAB $sCB) $sC) $sB)
                  (/safe (* $sC (* (- 1.0 $sAB) (- 1.0 $sCB)))
                         (- 1.0 $sB)))
               0.0 1.0)
        (clamp (Truth_w2c (* (* $sAB $cAB) $cCB)) 0.0 1.0)))

;; Operational 2-argument abduction:
(: Truth_Abduction (-> TruthValue TruthValue TruthValue))
(= (Truth_Abduction (stv $sAB $cAB) (stv $sCB $cCB))
   (let* (($s (clamp (* $sAB $sCB) 0.0 1.0))
          ($c (clamp (Truth_w2c (* (* $sAB $cAB) $cCB)) 0.0 1.0)))
     (stv $s $c)))
