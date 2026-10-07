;; ==============================================================================
;; Test Suite: Edge Cases and Robustness
;; ==============================================================================
;; Tests engine resilience against:
;;   1. Unknown crops / diseases / symptoms
;;   2. Extreme / boundary STV inputs (0.0, 1.0, out of bounds)
;;   3. Empty query matches
;;   4. Conflicting evidence reconciliation
;;   5. Missing evidence degradation
;;   6. Duplicate evidence stability
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)
!(import! &self pln:abduction)
!(import! &self pln:revision)
!(import! &self pln:forward)
!(import! &self pln:backward)

;; Test 1: Unknown Crop Query Handling (returns empty collection gracefully without crashing)
!(let $res (collapse (abduce-crop-diagnosis &self NonExistentCrop OrangeLeafSpots 0.90 0.85))
   (assertEqual (size-atom $res) 0))

;; Test 2: Unknown Symptom Query Handling
!(let $res (collapse (abduce-crop-diagnosis &self Coffee NonExistentSymptom 0.90 0.85))
   (assertEqual (size-atom $res) 0))

;; Test 3: Boundary STV Values (0.0, 1.0, and out-of-range clamping)
!(let (stv $s1 $c1) (stv-create -0.5 1.5)
   (assertEqual (and (== $s1 0.0) (== $c1 1.0)) True))

!(let (stv $s2 $c2) (pln-deduce (stv 0.0 0.0) (stv 1.0 1.0))
   (assertEqual (== $s2 0.0) True))

;; Test 4: Extreme Conflicting Evidence Revision (Total Disagreement)
!(let (stv $s_conf $c_conf) (pln-revise (stv 1.0 0.90) (stv 0.0 0.90))
   (assertEqual (and (== $s_conf 0.50) (> $c_conf 0.90)) True))

;; Test 5: Idempotent / Consistent Revision under Duplicate Evidence
!(let (stv $s_dup $c_dup) (pln-revise (stv 0.80 0.50) (stv 0.80 0.50))
   (assertEqual (and (== $s_dup 0.80) (> $c_dup 0.50)) True))

;; Test 6: Missing Evidence Forward Reasoning Graceful Degradation
!(let $risk_only (collapse (forward-infer-risk &self Coffee HighHumidity))
   (assertEqual (> (size-atom $risk_only) 0) True))
