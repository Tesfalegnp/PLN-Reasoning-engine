;; ==============================================================================
;; agri-pln-metta: Backward Chaining Inference Module
;; ==============================================================================
;; Implements goal-driven backward chaining over the unified agricultural KB:
;;   Target Goal: e.g. "Is CoffeeLeafRust affecting this crop?"
;;   Backward Search:
;;     1. Identifies required supporting premises (Susceptibility, Risk Conditions, Causal Symptoms).
;;     2. Evaluates observed evidence against required premises.
;;     3. Identifies verified supporting evidence vs. unresolved / missing evidence.
;;     4. Computes overall goal STV reflecting uncertainty of incomplete evidence.
;;     5. Returns complete backward proof tree.
;;
;; Operates on the exact same underlying knowledge base as forward chaining.
;; Avoids circular reasoning via goal-directed premise matching.
;; ==============================================================================

!(import! &self stv)
!(import! &self formulas)
!(import! &self deduction)
!(import! &self abduction)
!(import! &self revision)

;; Backward Query 1: Find all potential supporting premises for a target disease in the KB
(= (backward-find-premises $space $target_disease)
   (let* (($susc (collapse (match $space (Susceptible $crop $target_disease $tv) (SusceptibleCrop $crop $tv))))
          ($cond (collapse (match $space (Relation increases-risk $c $target_disease $tv) (RiskCondition $c $tv))))
          ($sym (collapse (match $space (Relation causes $target_disease $s $tv) (CausalSymptom $s $tv))))
          ($treat (collapse (match $space (Relation effective-treatment $t $target_disease $tv) (EffectiveTreatment $t $tv)))))
     (GoalPremiseTemplate
       (TargetDisease $target_disease)
       (SusceptibilityPremises $susc)
       (RiskConditionPremises $cond)
       (SymptomPremises $sym)
       (TreatmentOptions $treat))))

;; Backward Query 2: Goal Verification with Complete Evidence (Crop + Condition + Symptom)
(= (backward-verify-goal-complete $space $crop $target_disease $obs_cond $obs_sym)
   (match $space (Susceptible $crop $target_disease (stv $s_susc $c_susc))
     (match $space (Relation increases-risk $obs_cond $target_disease (stv $s_risk $c_risk))
       (match $space (Relation causes $target_disease $obs_sym (stv $s_sym $c_sym))
         (match $space (PriorDisease $target_disease (stv $s_pri $c_pri))
           (let* (($tv_premise_env (formula-deduction (stv $s_susc $c_susc) (stv $s_risk $c_risk)))
                  ($tv_premise_sym (formula-abduction (stv $s_sym $c_sym) (stv 0.95 0.90) (stv $s_pri $c_pri)))
                  ($tv_goal (formula-revision $tv_premise_env $tv_premise_sym)))
             (BackwardProofTree
               (Goal (VerifyDisease $target_disease))
               (GoalStatus VerifiedSupported)
               (GoalSTV $tv_goal)
               (VerifiedEvidence
                 (Premise1 (CropMatch $crop) (Susceptibility (stv $s_susc $c_susc)))
                 (Premise2 (ConditionMatch $obs_cond) (RiskSupport (stv $s_risk $c_risk)))
                 (Premise3 (SymptomMatch $obs_sym) (CausalSupport (stv $s_sym $c_sym))))
               (MissingEvidence None)
               (BackwardProofPath
                 ((Goal $target_disease) <- (Premises ($crop $obs_cond $obs_sym)))))))))))

;; Backward Query 3: Goal Verification with Incomplete Evidence (e.g. Symptom present, Condition Missing)
(= (backward-verify-goal-incomplete $space $crop $target_disease $obs_sym)
   (match $space (Susceptible $crop $target_disease (stv $s_susc $c_susc))
     (match $space (Relation causes $target_disease $obs_sym (stv $s_sym $c_sym))
       (match $space (PriorDisease $target_disease (stv $s_pri $c_pri))
         (match $space (Relation increases-risk $missing_cond $target_disease (stv $s_cond $c_cond))
           (let* (($tv_sym_only (formula-abduction (stv $s_sym $c_sym) (stv 0.80 0.70) (stv $s_pri $c_pri)))
                  ;; Confidence penalized due to missing environmental confirmation
                  ($tv_penalized (stv (stv-s $tv_sym_only) (* (stv-c $tv_sym_only) 0.65))))
             (BackwardProofTree
               (Goal (VerifyDisease $target_disease))
               (GoalStatus PartiallySupportedIncompleteEvidence)
               (GoalSTV $tv_penalized)
               (VerifiedEvidence
                 (Premise1 (CropMatch $crop) (Susceptibility (stv $s_susc $c_susc)))
                 (Premise2 (SymptomMatch $obs_sym) (CausalSupport (stv $s_sym $c_sym))))
               (MissingEvidence
                 (UnobservedRiskCondition $missing_cond (TypicalRisk (stv $s_cond $c_cond))))
               (Interpretation "Hypothesis partially supported by symptoms; missing environmental confirmation reduces confidence.")
               (BackwardProofPath
                 ((Goal $target_disease) <- (Verified $obs_sym) + (Missing $missing_cond))))))))))
