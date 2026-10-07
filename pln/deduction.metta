;; ==============================================================================
;; agri-pln-metta: Probabilistic Deduction Module
;; ==============================================================================
;; Implements forward transitive deduction over agricultural causal and risk links:
;;   Premise 1: (Relation R1 A B TV1)
;;   Premise 2: (Relation R2 B C TV2)
;;   Conclusion: Derived link A -> C with computed STV and explanatory proof path.
;; ==============================================================================

!(import! &self stv)
!(import! &self formulas)

;; Direct PLN deduction function on STVs
(= (pln-deduce (stv $s1 $c1) (stv $s2 $c2))
   (formula-deduction (stv $s1 $c1) (stv $s2 $c2)))

;; Multi-hop 2-step deduction over AtomSpace relations
(= (deduce-relation-step $space $rel1 $rel2 $a $b $c)
   (match $space (Relation $rel1 $a $b (stv $s1 $c1))
     (match $space (Relation $rel2 $b $c (stv $s2 $c2))
       (DeducedLink
         (From $a)
         (Via $b)
         (To $c)
         (STV (formula-deduction (stv $s1 $c1) (stv $s2 $c2)))
         (Rule (Deduction ($rel1 $a $b) ($rel2 $b $c)))
         (Path ($a -> $b -> $c))))))

;; Agricultural Condition -> Disease -> Symptom Deduction
;; Example: HighHumidity -> CoffeeLeafRust -> OrangeLeafSpots
(= (deduce-condition-to-symptom $space $condition $symptom)
   (match $space (Relation increases-risk $condition $disease (stv $s1 $c1))
     (match $space (Relation causes $disease $symptom (stv $s2 $c2))
       (DeductionResult
         (Premises (Condition $condition) (IntermediateDisease $disease) (TargetSymptom $symptom))
         (STV (formula-deduction (stv $s1 $c1) (stv $s2 $c2)))
         (Explanation (Deduction (increases-risk $condition $disease) (causes $disease $symptom)))
         (Path ($condition -> $disease -> $symptom))))))

;; Agricultural Condition -> Disease -> Treatment Deduction
;; Example: HighHumidity -> CoffeeLeafRust -> CopperFungicide
(= (deduce-condition-to-treatment $space $condition $treatment)
   (match $space (Relation increases-risk $condition $disease (stv $s1 $c1))
     (match $space (Relation effective-treatment $treatment $disease (stv $s2 $c2))
       (DeductionResult
         (Premises (Condition $condition) (DiseaseTarget $disease) (RecommendedTreatment $treatment))
         (STV (formula-deduction (stv $s1 $c1) (stv $s2 $c2)))
         (Explanation (Deduction (increases-risk $condition $disease) (effective-treatment $treatment $disease)))
         (Path ($condition -> $disease -> $treatment))))))
