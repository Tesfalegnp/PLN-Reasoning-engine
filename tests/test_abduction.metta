;; ==============================================================================
;; Test Suite: Probabilistic Abduction
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:abduction)

;; Test 1: Direct STV Abduction Formula
;; Rule: CoffeeLeafRust -> OrangeLeafSpots (0.90 0.85)
;; Observed Symptom: OrangeLeafSpots (0.95 0.90)
;; Prior: CoffeeLeafRust (0.30 0.85)
!(let (stv $s $c) (pln-abduce (stv 0.90 0.85) (stv 0.95 0.90) (stv 0.30 0.85))
   (assertEqual (and (> $s 0.70) (> $c 0.50)) True))

;; Test 2: Epistemic Moderation (Abduction confidence is moderated compared to input confidence)
!(let* (($tv_rule (stv 0.90 0.90))
        ($tv_obs (stv 0.90 0.90))
        ($tv_pri (stv 0.30 0.90))
        ($tv_res (pln-abduce $tv_rule $tv_obs $tv_pri)))
   (assertEqual (< (stv-c $tv_res) (stv-c $tv_obs)) True))

;; Test 3: Crop-Scoped Diagnostic Abduction
;; Coffee + OrangeLeafSpots -> Hypothesize CoffeeLeafRust
!(let (CropDiagnosisHypothesis (Crop Coffee) (HypothesizedDisease $dis) (TriggerSymptom OrangeLeafSpots) (STV (stv $s $c)) $ev $inf $status)
      (abduce-crop-diagnosis &self Coffee OrangeLeafSpots 0.95 0.90)
   (assertEqual (and (== $dis CoffeeLeafRust) (> $s 0.60)) True))

;; Test 4: Multiple Competing Explanations for YellowLeaves
;; Causes of YellowLeaves in Tomato: LateBlight, EarlyBlight, NitrogenDeficiency, RootRot
!(let $causes (collapse (abduce-causes-for-symptom &self YellowLeaves 0.90 0.85))
   (assertEqual (> (size-atom $causes) 2) True))
