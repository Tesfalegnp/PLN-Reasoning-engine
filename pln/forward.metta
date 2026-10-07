;; ==============================================================================
;; agri-pln-metta: Forward Chaining Inference Module
;; ==============================================================================
;; Implements data-driven forward chaining:
;;   Starting from observed facts:
;;     - Observed Crop (e.g. Coffee)
;;     - Observed Environmental Conditions (e.g. HighHumidity)
;;     - Observed Plant Symptoms (e.g. OrangeLeafSpots)
;;   The engine fires applicable causal, risk, and treatment rules in forward order:
;;     1. Condition -> Inferred Disease Risk (Deduction)
;;     2. Symptom + Risk -> Inferred Disease Diagnosis (Abduction + Revision)
;;     3. Diagnosed Disease -> Inferred Treatment Recommendation (Deduction)
;;     4. Condition -> Environmental Remediation Action (Deduction)
;;
;; Protects against infinite loops via tiered acyclic relational chaining.
;; ==============================================================================

!(import! &self stv)
!(import! &self formulas)
!(import! &self deduction)
!(import! &self abduction)
!(import! &self revision)

;; Forward Step 1: Infer Disease Risk from Observed Environmental Condition
(= (forward-infer-risk $space $crop $condition)
   (match $space (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match $space (Relation increases-risk $condition $disease (stv $s_risk $c_risk))
       (let $tv_risk (formula-deduction (stv $s_susc $c_susc) (stv $s_risk $c_risk))
         (ForwardRisk
           (Crop $crop)
           (Condition $condition)
           (RiskOfDisease $disease)
           (STV $tv_risk)
           (Rule (increases-risk $condition $disease))
           (Inference ForwardDeduction))))))

;; Forward Step 2: Infer Disease Diagnosis from Crop + Condition + Symptom Observations
(= (forward-infer-diagnosis $space $crop $condition $symptom)
   (match $space (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match $space (Relation increases-risk $condition $disease (stv $s_risk $c_risk))
       (match $space (Relation causes $disease $symptom (stv $s_cause $c_cause))
         (match $space (PriorDisease $disease (stv $s_pri $c_pri))
           (let* (($tv_env_risk (formula-deduction (stv $s_susc $c_susc) (stv $s_risk $c_risk)))
                  ($tv_abduced (formula-abduction (stv $s_cause $c_cause) (stv 0.95 0.90) (stv $s_pri $c_pri)))
                  ($tv_combined (formula-revision $tv_env_risk $tv_abduced)))
             (ForwardDiagnosis
               (Crop $crop)
               (InferredDisease $disease)
               (SupportingEvidence
                 (ObservedCondition $condition)
                 (ObservedSymptom $symptom)
                 (CropSusceptibility $crop -> $disease))
               (STV $tv_combined)
               (ReasoningPath ($condition -> increases-risk -> $disease -> causes -> $symptom))
               (Inference (ForwardDeduction + Abduction + Revision)))))))))

;; Forward Step 3: Infer Treatment Recommendations from Diagnosed Disease
(= (forward-infer-treatment $space $disease (stv $s_diag $c_diag))
   (match $space (Relation effective-treatment $treatment $disease (stv $s_treat $c_treat))
     (let $tv_rec (formula-deduction (stv $s_diag $c_diag) (stv $s_treat $c_treat))
       (ForwardTreatmentRecommendation
         (TargetDisease $disease)
         (RecommendedTreatment $treatment)
         (STV $tv_rec)
         (Rule (effective-treatment $treatment $disease))
         (Inference ForwardDeduction)))))

;; Complete End-to-End Forward Reasoning Pipeline
(= (forward-chain-full $space $crop $condition $symptom)
   (match $space (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match $space (Relation increases-risk $condition $disease (stv $s_risk $c_risk))
       (match $space (Relation causes $disease $symptom (stv $s_cause $c_cause))
         (match $space (PriorDisease $disease (stv $s_pri $c_pri))
           (match $space (Relation effective-treatment $treatment $disease (stv $s_treat $c_treat))
             (let* (($tv_risk (formula-deduction (stv $s_susc $c_susc) (stv $s_risk $c_risk)))
                    ($tv_abduced (formula-abduction (stv $s_cause $c_cause) (stv 0.95 0.90) (stv $s_pri $c_pri)))
                    ($tv_diag (formula-revision $tv_risk $tv_abduced))
                    ($tv_rec (formula-deduction $tv_diag (stv $s_treat $c_treat))))
               (ForwardReasoningResult
                 (Observations (Crop $crop) (Condition $condition) (Symptom $symptom))
                 (Diagnosis
                   (Disease $disease)
                   (STV $tv_diag))
                 (Treatment
                   (Action $treatment)
                   (STV $tv_rec))
                 (ReasoningChain
                   (Step1 (Condition $condition) -> (RiskOf $disease) (STV $tv_risk))
                   (Step2 (Symptom $symptom) -> (AbducedCause $disease) (STV $tv_abduced))
                   (Step3 (FusedBelief $disease) (STV $tv_diag))
                   (Step4 (Prescribe $treatment) (STV $tv_rec)))
                 (InferenceSummary "Full forward chain: Environment + Symptom -> Diagnosis -> Treatment")))))))))
