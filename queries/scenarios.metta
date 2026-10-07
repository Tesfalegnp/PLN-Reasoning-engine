;; ==============================================================================
;; agri-pln-metta: Comprehensive Evaluation Scenarios Module
;; ==============================================================================
;; Implements the 7 required evaluation scenarios demonstrating all core PLN capabilities:
;;   Scenario 1: Strongly Supported Conclusion (Deduction)
;;   Scenario 2: Incomplete / Uncertain Evidence (Missing Evidence Handling)
;;   Scenario 3: Multiple Plausible Explanations (Differential Diagnosis)
;;   Scenario 4: New / Conflicting Evidence (Belief Revision)
;;   Scenario 5: Multi-Step Causal Inference (Uncertainty Propagation)
;;   Scenario 6: Data-Driven Forward Chaining (Observations -> Diagnosis -> Treatment)
;;   Scenario 7: Goal-Driven Backward Chaining (Target Goal -> Premise Search -> Proof)
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)
!(import! &self pln:induction)
!(import! &self pln:abduction)
!(import! &self pln:revision)
!(import! &self pln:chaining)
!(import! &self pln:forward)
!(import! &self pln:backward)

;; ==============================================================================
;; SCENARIO 1: Strongly Supported Conclusion (Probabilistic Deduction)
;; High Humidity increases risk of Coffee Leaf Rust; Coffee Leaf Rust causes Orange Leaf Spots.
;; ==============================================================================
(= (run-scenario-1)
   (let $deduced (deduce-condition-to-symptom &self HighHumidity OrangeLeafSpots)
     (ScenarioOutput
       (Scenario 1)
       (Title "Strongly Supported Conclusion (Deduction)")
       (Given "High Humidity increases risk of Coffee Leaf Rust; Coffee Leaf Rust causes Orange Leaf Spots")
       (Result $deduced)
       (Interpretation "High Humidity probabilistically predicts Orange Leaf Spots via Coffee Leaf Rust intermediate path."))))

;; ==============================================================================
;; SCENARIO 2: Incomplete / Uncertain Evidence
;; Coffee crop + Orange Leaf Spots observed, but environmental humidity is missing.
;; Engine derives lower-confidence conclusion and flags missing environmental risk confirmation.
;; ==============================================================================
(= (run-scenario-2)
   (let $proof (backward-verify-goal-incomplete &self Coffee CoffeeLeafRust OrangeLeafSpots)
     (ScenarioOutput
       (Scenario 2)
       (Title "Incomplete / Uncertain Evidence")
       (ObservedEvidence (Crop Coffee) (Symptom OrangeLeafSpots))
       (MissingEvidence (Condition HighHumidity))
       (Result $proof)
       (Interpretation "Without environmental humidity confirmation, hypothesis confidence is penalized from 0.74 to lower confidence, and missing evidence is explicitly reported."))))

;; ==============================================================================
;; SCENARIO 3: Multiple Plausible Explanations (Differential Abduction)
;; Symptom: YellowLeaves observed on Coffee.
;; Engine returns all candidate causes (NitrogenDeficiency, RootRot, CoffeeLeafRust, BrownEyeSpot)
;; with their individual calculated STVs.
;; ==============================================================================
(= (run-scenario-3)
   (let $candidates (match &self (Susceptible Coffee $disease (stv $s_susc $c_susc))
                      (match &self (Relation causes $disease YellowLeaves (stv $s_cause $c_cause))
                        (match &self (PriorDisease $disease (stv $s_pri $c_pri))
                          (let* (($tv_abd (formula-abduction (stv $s_cause $c_cause) (stv 0.90 0.85) (stv $s_pri $c_pri)))
                                 ($tv_fin (formula-deduction (stv $s_susc $c_susc) $tv_abd)))
                            (CandidateExplanation
                              (Disease $disease)
                              (STV $tv_fin))))))
     (ScenarioOutput
       (Scenario 3)
       (Title "Multiple Plausible Explanations (Differential Diagnosis)")
       (ObservedSymptom (Crop Coffee) (Symptom YellowLeaves))
       (Result $candidates)
       (Interpretation "Multiple candidate diseases explain YellowLeaves; each has its distinct probabilistic STV."))))

;; ==============================================================================
;; SCENARIO 4: New / Conflicting Evidence (Probabilistic Revision)
;; Initial field observation: CoffeeLeafRust (stv 0.85 0.70)
;; Laboratory PCR test: CoffeeLeafRust (stv 0.95 0.90)
;; Recombination yields updated belief with boosted confidence.
;; Also demonstrates conflicting evidence revision.
;; ==============================================================================
(= (run-scenario-4-agreeing)
   (let $rev (revise-evidence-sources CoffeeLeafRust FieldVisualScouting (stv 0.85 0.70) LabPCRDiagnostic (stv 0.95 0.90))
     (ScenarioOutput
       (Scenario 4A)
       (Title "New Reinforcing Evidence Revision")
       (InitialBelief (FieldVisualScouting (stv 0.85 0.70)))
       (NewEvidence (LabPCRDiagnostic (stv 0.95 0.90)))
       (Result $rev)
       (Interpretation "Confidence increases significantly as independent high-reliability lab evidence reinforces visual scouting."))))

(= (run-scenario-4-conflicting)
   (let $rev (revise-evidence-sources CoffeeLeafRust FieldVisualScouting (stv 0.90 0.80) LabNegativeMicroscopy (stv 0.10 0.80))
     (ScenarioOutput
       (Scenario 4B)
       (Title "Conflicting Evidence Revision")
       (Belief1 (FieldVisualScouting (stv 0.90 0.80)))
       (Belief2 (LabNegativeMicroscopy (stv 0.10 0.80)))
       (Result $rev)
       (Interpretation "Strength shifts to neutral 0.50 while confidence reflects combined weight of conflicting evidence."))))

;; ==============================================================================
;; SCENARIO 5: Multi-Step Causal Inference (Uncertainty Propagation)
;; 3-hop chain: PoorDrainage -> WaterloggedSoil -> RootRot -> Wilting
;; ==============================================================================
(= (run-scenario-5)
   (let $chain (chain-3-hop &self promotes PoorDrainage WaterloggedSoil increases-risk RootRot causes Wilting)
     (ScenarioOutput
       (Scenario 5)
       (Title "Multi-Step Causal Inference (3-Hop Chain)")
       (CausalPath (PoorDrainage -> WaterloggedSoil -> RootRot -> Wilting))
       (Result $chain)
       (Interpretation "Uncertainty propagates across 3 hops; strength and confidence decay progressively at each transition."))))

;; ==============================================================================
;; SCENARIO 6: Data-Driven Forward Chaining
;; Observations: Crop=Coffee, Condition=HighHumidity, Symptom=OrangeLeafSpots
;; Engine derives Inferred Disease + Recommended Curative/Preventive Treatments.
;; ==============================================================================
(= (run-scenario-6)
   (let $fwd (forward-chain-full &self Coffee HighHumidity OrangeLeafSpots)
     (ScenarioOutput
       (Scenario 6)
       (Title "Data-Driven Forward Chaining")
       (Observations (Crop Coffee) (Condition HighHumidity) (Symptom OrangeLeafSpots))
       (Result $fwd)
       (Interpretation "Engine matches premises in forward order: environmental risk -> symptom explanation -> disease diagnosis -> actionable IPM treatments."))))

;; ==============================================================================
;; SCENARIO 7: Goal-Driven Backward Chaining
;; Target Goal: Verify CoffeeLeafRust on Coffee farm with HighHumidity and OrangeLeafSpots.
;; Engine searches backward for required premises, verifies evidence, and constructs proof tree.
;; ==============================================================================
(= (run-scenario-7)
   (let $bc (backward-verify-goal-complete &self Coffee CoffeeLeafRust HighHumidity OrangeLeafSpots)
     (ScenarioOutput
       (Scenario 7)
       (Title "Goal-Driven Backward Chaining")
       (TargetGoal (VerifyDisease CoffeeLeafRust))
       (Result $bc)
       (Interpretation "Engine searches backward for required premises, verifies them against observations, and builds a complete proof tree."))))

;; Run All 7 Scenarios Sequentially
(= (run-all-scenarios)
   (AllScenariosResults
     (Scenario1 (run-scenario-1))
     (Scenario2 (run-scenario-2))
     (Scenario3 (run-scenario-3))
     (Scenario4Agreeing (run-scenario-4-agreeing))
     (Scenario4Conflicting (run-scenario-4-conflicting))
     (Scenario5 (run-scenario-5))
     (Scenario6 (run-scenario-6))
     (Scenario7 (run-scenario-7))))
