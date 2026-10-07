;; ==============================================================================
;; Test Suite: Probabilistic Induction
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:induction)

;; Test 1: Sample Count Induction Math
;; 18 positive out of 20 total farms surveyed (k=2.0)
;; s = 18.0 / 20.0 = 0.90, c = 20.0 / (20.0 + 2.0) = 0.90909
!(let (stv $s $c) (pln-induce-samples 18.0 20.0 2.0)
   (assertEqual (and (== $s 0.90) (> $c 0.90)) True))

;; Test 2: Low Sample Size Uncertainty
;; 2 positive out of 2 total farms (s = 1.0, but confidence should be low: 2 / 4 = 0.50)
!(let (stv $s $c) (pln-induce-samples 2.0 2.0 2.0)
   (assertEqual (and (== $s 1.0) (== $c 0.50)) True))

;; Test 3: Bayesian Inverse Induction
;; Inducing P(B|A) from P(A|B)=0.85 (c=0.80), P(A)=0.40 (c=0.70), P(B)=0.35 (c=0.75)
!(let (stv $s $c) (pln-induce-bayes (stv 0.85 0.80) (stv 0.40 0.70) (stv 0.35 0.75) )
   (assertEqual (and (> $s 0.70) (> $c 0.40)) True))

;; Test 4: Relational Farm Risk Rule Induction
!(let (InductionResult $rule $ev (STV (stv $s $c)) $type $exp)
      (induce-farm-risk-rule HighHumidity CoffeeLeafRust 16.0 20.0)
   (assertEqual (and (== $s 0.80) (> $c 0.88)) True))
