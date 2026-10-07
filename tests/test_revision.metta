;; ==============================================================================
;; Test Suite: Probabilistic Revision
;; ==============================================================================

!(register-module! ../pln)

!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:revision)

;; Test 1: Reinforcing Evidence Combination
;; When two independent sources provide agreeing evidence, confidence increases.
!(let* (($tv1 (stv 0.85 0.70))
        ($tv2 (stv 0.90 0.80))
        ($tv_rev (pln-revise $tv1 $tv2)))
   (assertEqual (> (stv-c $tv_rev) 0.80) True))

;; Test 2: Conflicting Evidence Combination
;; Belief 1 (0.90 0.80) vs Belief 2 (0.10 0.80)
;; Equal weight results in neutral midpoint strength (0.50) with higher total evidence confidence.
!(let (stv $s $c) (pln-revise (stv 0.90 0.80) (stv 0.10 0.80))
   (assertEqual (and (== $s 0.50) (> $c 0.85)) True))

;; Test 3: Revision Commutativity (Order Independence)
;; E1 + E2 should produce the same strength and confidence as E2 + E1
!(let* (($tv_a (pln-revise (stv 0.80 0.60) (stv 0.95 0.85)))
        ($tv_b (pln-revise (stv 0.95 0.85) (stv 0.80 0.60))))
   (assertEqual (and (== (stv-s $tv_a) (stv-s $tv_b))
                     (== (stv-c $tv_a) (stv-c $tv_b))) True))

;; Test 4: Named Multi-Source Evidence Fusion
!(let (RevisionResult (Proposition $prop) (CombinedSTV (stv $s $c)) $srcs $inf $interp)
      (revise-evidence-sources CoffeeLeafRust FieldVisual (stv 0.85 0.70) LabPCR (stv 0.95 0.90))
   (assertEqual (and (> $s 0.90) (> $c 0.90)) True))
