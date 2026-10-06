;; ====================================================================
;; Agricultural PLN Inference Rules Library
;; Declarative inference patterns over agricultural relations
;; ====================================================================

;; Binary inference rules generator
(= (rb)
   (superpose (
     ;; Deduction over Inheritance (Varietal Taxonomy & Susceptibility):
     ;; (Inheritance X Y), (Inheritance Y Z) |- (Inheritance X Z)
     (rule ded (Inheritance $x $y) (Inheritance $y $z) (Inheritance $x $z))
     
     ;; Deduction over Implication (Causal Diagnostic & Therapeutic Chains):
     ;; (→ X Y), (→ Y Z) |- (→ X Z)
     (rule ded (→ $x $y) (→ $y $z) (→ $x $z))
     
     ;; Modus Ponens (Symptom-to-Disease & Disease-to-Treatment Detachment):
     ;; P, (→ P Q) |- Q
     (rule mp $p (→ $p $q) $q)
   )))

;; Unary inference rules generator
(= (rb1)
   (superpose (
     ;; Symmetry of Cultivar / Botanical Similarity:
     ;; (Similarity X Y) |- (Similarity Y X)
     (rule1 sim_sym (Similarity $x $y) (Similarity $y $x))
   )))
