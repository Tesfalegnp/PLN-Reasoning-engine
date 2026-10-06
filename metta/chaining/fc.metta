;; ====================================================================
;; PLN Forward Chainer with Step Bounding
;; ====================================================================

;; Rule truth function dispatchers
(= (Truth_Apply_Rule2 ded $tv1 $tv2) (Truth_Deduction $tv1 $tv2))
(= (Truth_Apply_Rule2 mp $tv1 $tv2) (Truth_ModusPonens $tv1 $tv2))
(= (Truth_Apply_Rule2 and_intro $tv1 $tv2) (Truth_Intersection $tv1 $tv2))

(= (Truth_Apply_Rule1 sim_sym $tv1) $tv1)
(= (Truth_Apply_Rule1 not_intro $tv1) (Truth_Negation $tv1))

;; --------------------------------------------------------------------
;; Forward Chainer: (fc (⊢ $premise $tv) $depth)
;; --------------------------------------------------------------------

;; 1. Base Case: Return current derivation at depth Z
(= (fc (⊢ $premise $tv) Z)
   (Derivation (⊢ $premise $tv) (Initial $premise)))

;; 2. Recursive Step: Derive new facts via binary rules, unary rules, or keep premise
(= (fc (⊢ $p1 $tv1) (S $k))
   (superpose (
     ;; Keep current premise
     (Derivation (⊢ $p1 $tv1) (Initial $p1))
     
     ;; Binary rule derivation: $p1 matches first premise
     (let* (((rule $ruleName $p1 $p2 $concl) (rb))
            ((⊢ $p2 $tv2) (kb))
            ($tvConcl (Truth_Apply_Rule2 $ruleName $tv1 $tv2)))
       (fc (⊢ $concl $tvConcl) $k))
       
     ;; Binary rule derivation: $p1 matches second premise
     (let* (((rule $ruleName $p0 $p1 $concl) (rb))
            ((⊢ $p0 $tv0) (kb))
            ($tvConcl (Truth_Apply_Rule2 $ruleName $tv0 $tv1)))
       (fc (⊢ $concl $tvConcl) $k))
       
     ;; Unary rule derivation
     (let* (((rule1 $ruleName $p1 $concl) (rb1))
            ($tvConcl (Truth_Apply_Rule1 $ruleName $tv1)))
       (fc (⊢ $concl $tvConcl) $k))
   )))
