;; ==============================================================================
;; Test Suite: Forward Chaining Inference
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

;; Test 1: Forward Risk Inference (Coffee + HighHumidity)
!(let (ForwardRisk (Crop Coffee) (Condition HighHumidity) (RiskOfDisease $dis) (STV (stv $s $c)) $rule $inf)
      (forward-infer-risk &self Coffee HighHumidity)
   (assertEqual (and (== $dis CoffeeLeafRust) (> $s 0.70)) True))

;; Test 2: Forward Disease Diagnosis (Coffee + HighHumidity + OrangeLeafSpots)
!(let (ForwardDiagnosis (Crop Coffee) (InferredDisease $dis) $ev (STV (stv $s $c)) $path $inf)
      (forward-infer-diagnosis &self Coffee HighHumidity OrangeLeafSpots)
   (assertEqual (and (== $dis CoffeeLeafRust) (and (> $s 0.70) (> $c 0.70))) True))

;; Test 3: Forward Treatment Derivation from Diagnosed Disease
!(let $treatments (collapse (forward-infer-treatment &self CoffeeLeafRust (stv 0.75 0.75)))
   (assertEqual (> (size-atom $treatments) 2) True))

;; Test 4: Full End-to-End Forward Chain
!(let $results (collapse (forward-chain-full &self Coffee HighHumidity OrangeLeafSpots))
   (assertEqual (> (size-atom $results) 0) True))
