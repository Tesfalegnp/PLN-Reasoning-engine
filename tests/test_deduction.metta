;; ==============================================================================
;; Test Suite: Probabilistic Deduction
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)

;; Test 1: Direct STV Deduction Math (A -> B: 0.85 0.80, B -> C: 0.90 0.85)
;; s = 0.85 * 0.90 = 0.765, c = 0.80 * 0.85 * 0.85 = 0.578
!(let (stv $s $c) (pln-deduce (stv 0.85 0.80) (stv 0.90 0.85))
   (assertEqual (and (> $s 0.76) (< $s 0.77)) True))

;; Test 2: Epistemic Confidence Decay Across Deductive Chain
!(let* (($tv1 (stv 0.80 0.80))
        ($tv2 (stv 0.80 0.80))
        ($tv_res (pln-deduce $tv1 $tv2)))
   (assertEqual (< (stv-c $tv_res) (stv-c $tv1)) True))

;; Test 3: Relational Condition -> Disease -> Symptom Deduction
;; HighHumidity (increases-risk 0.85 0.80) CoffeeLeafRust (causes 0.90 0.85) OrangeLeafSpots
!(let (DeductionResult $prem (STV (stv $s $c)) $exp $path)
      (deduce-condition-to-symptom &self HighHumidity OrangeLeafSpots)
   (assertEqual (and (> $s 0.76) (< $s 0.77)) True))

;; Test 4: Relational Condition -> Disease -> Treatment Deduction
;; HighHumidity -> CoffeeLeafRust -> CopperFungicide
!(let (DeductionResult $prem (STV (stv $s $c)) $exp $path)
      (deduce-condition-to-treatment &self HighHumidity CopperFungicide)
   (assertEqual (and (> $s 0.74) (> $c 0.50)) True))
