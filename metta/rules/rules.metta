;; ====================================================================
;; PLN Inference Rules Library (Agriculture-Oriented Alias)
;; ====================================================================

;; Binary inference rules generator
(= (rb)
   (superpose (
     ;; Deduction over Inheritance (Varietal Taxonomy & Susceptibility):
     (rule ded (Inheritance $x $y) (Inheritance $y $z) (Inheritance $x $z))
     
     ;; Deduction over Implication (Causal Diagnostic & Therapeutic Chains):
     (rule ded (→ $x $y) (→ $y $z) (→ $x $z))
     
     ;; Modus Ponens (Symptom-to-Disease & Disease-to-Treatment Detachment):
     (rule mp $p (→ $p $q) $q)
   )))

;; Unary inference rules generator
(= (rb1)
   (superpose (
     ;; Symmetry of Cultivar / Botanical Similarity:
     (rule1 sim_sym (Similarity $x $y) (Similarity $y $x))
   )))
