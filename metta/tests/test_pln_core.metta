;; ====================================================================
;; MeTTa Test: PLN Core Formulas
;; ====================================================================

!(import! &self metta:core:pln_tv)
!(import! &self metta:core:pln_formulas)

;; Test 1: PLN Negation
!(assertEqual
   (Truth_Negation (stv 0.7 0.9))
   (stv 0.30000000000000004 0.9))

;; Test 2: PLN Conjunction
!(assertEqual
   (Truth_Intersection (stv 0.8 0.9) (stv 0.5 0.6))
   (stv 0.4 0.54))

;; Test 3: PLN Deduction
!(let (stv $s $c) (Truth_Deduction (stv 1.0 0.9) (stv 0.9 0.8))
   (and (> $s 0.89) (> $c 0.64)))

;; Test 4: PLN Modus Ponens
!(let (stv $s $c) (Truth_ModusPonens (stv 0.95 0.90) (stv 0.85 0.80))
   (and (> $s 0.80) (> $c 0.58)))

;; Test 5: PLN Revision
!(let (stv $s $c) (Truth_Revision (stv 0.8 0.6) (stv 0.85 0.7))
   (and (> $c 0.75) (> $s 0.80)))
