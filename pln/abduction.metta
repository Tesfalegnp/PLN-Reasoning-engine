;; ==============================================================================
;; agri-pln-metta: Probabilistic Abduction Module
;; ==============================================================================
;; Implements diagnostic abductive inference:
;;   Given:
;;     1. Observed Symptom / Effect B (with STV_obs)
;;     2. Causal Rule: Disease A causes Symptom B (with STV_rule)
;;     3. Prior Prevalence: PriorDisease A (with STV_prior)
;;   Derives:
;;     Hypothesis: Disease A as plausible explanation, with computed STV.
;;
;; Distinguishes observed evidence from hypothesized cause.
;; Generates multiple competing candidate hypotheses when multiple causes exist.
;; ==============================================================================

!(import! &self stv)
!(import! &self formulas)

;; Direct STV abduction function
(= (pln-abduce (stv $s_rule $c_rule) (stv $s_obs $c_obs) (stv $s_pri $c_pri))
   (formula-abduction (stv $s_rule $c_rule) (stv $s_obs $c_obs) (stv $s_pri $c_pri)))

(= (pln-abduce-default (stv $s_rule $c_rule) (stv $s_obs $c_obs))
   (formula-abduction-default (stv $s_rule $c_rule) (stv $s_obs $c_obs)))

;; Abduce candidate disease explanations for an observed symptom across AtomSpace
(= (abduce-causes-for-symptom $space $symptom $s_obs $c_obs)
   (match $space (Relation causes $disease $symptom (stv $s_rule $c_rule))
     (match $space (PriorDisease $disease (stv $s_pri $c_pri))
       (let $tv (formula-abduction (stv $s_rule $c_rule) (stv $s_obs $c_obs) (stv $s_pri $c_pri))
         (AbductionHypothesis
           (HypothesizedCause $disease)
           (ObservedSymptom $symptom)
           (STV $tv)
           (Inference (Abduction (causes $disease $symptom) (Observed $symptom)))
           (Interpretation (Explanation $disease "is a probabilistically supported explanation, not a certainty")))))))

;; Crop-Scoped Abduction: Restricts candidate diseases to those affecting the specific crop
(= (abduce-crop-diagnosis $space $crop $symptom $s_obs $c_obs)
   (match $space (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match $space (Relation causes $disease $symptom (stv $s_rule $c_rule))
       (match $space (PriorDisease $disease (stv $s_pri $c_pri))
         (let* (($abduced_tv (formula-abduction (stv $s_rule $c_rule) (stv $s_obs $c_obs) (stv $s_pri $c_pri)))
                ($final_tv (formula-deduction (stv $s_susc $c_susc) $abduced_tv)))
           (CropDiagnosisHypothesis
             (Crop $crop)
             (HypothesizedDisease $disease)
             (TriggerSymptom $symptom)
             (STV $final_tv)
             (Evidence
               (CropSusceptibility (Susceptible $crop $disease (stv $s_susc $c_susc)))
               (CausalLink (causes $disease $symptom (stv $s_rule $c_rule)))
               (ObservedSymptom (Observed $symptom (stv $s_obs $c_obs))))
             (Inference (Abduction + SusceptibilityConstraint))
             (Status PlausibleHypothesis)))))))
