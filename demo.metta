;; ==============================================================================
;; agri-pln-metta: Interactive Demonstration
;; ==============================================================================
;; Demonstrates domain-specific agricultural probabilistic logic network (PLN)
;; reasoning over interconnected agronomic knowledge in MeTTa.
;; ==============================================================================

!(register-module! knowledge)
!(register-module! pln)

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
;; DEMO BANNER
;; ==============================================================================
!(BANNER "==============================================================================")
!(BANNER " agri-pln-metta: Agricultural Probabilistic Logic Network Engine in MeTTa")
!(BANNER "==============================================================================")

;; ==============================================================================
;; QUERY 1: Forward Diagnostic Reasoning from Field Observations
;; USER: My coffee farm has high humidity and orange spots on the leaves. What is causing this and how should I treat it?
;; ==============================================================================
!(SECTION "DEMO 1: Forward Diagnostic Chaining & IPM Treatment Prescription")
!(USER_QUERY "Observations: Crop=Coffee, Condition=HighHumidity, Symptom=OrangeLeafSpots")
!(SYSTEM_REASONING (forward-chain-full &self Coffee HighHumidity OrangeLeafSpots))

;; ==============================================================================
;; QUERY 2: Handling Incomplete / Uncertain Evidence
;; USER: Orange leaf spots are visible on my coffee plants, but weather humidity data is missing.
;; ==============================================================================
!(SECTION "DEMO 2: Incomplete Evidence Handling & Uncertainty Penalty")
!(USER_QUERY "Goal: Verify CoffeeLeafRust with missing environmental data")
!(SYSTEM_REASONING (backward-verify-goal-incomplete &self Coffee CoffeeLeafRust OrangeLeafSpots))

;; ==============================================================================
;; QUERY 3: Differential Diagnosis for Multiple Candidate Explanations
;; USER: My coffee leaves are turning yellow. What could be the cause?
;; ==============================================================================
!(SECTION "DEMO 3: Differential Diagnosis (Multiple Competing Explanations)")
!(USER_QUERY "Observed: Coffee leaves turning yellow (YellowLeaves)")
!(SYSTEM_REASONING
   (match &self (Susceptible Coffee $disease (stv $s_susc $c_susc))
     (match &self (Relation causes $disease YellowLeaves (stv $s_cause $c_cause))
       (match &self (PriorDisease $disease (stv $s_pri $c_pri))
         (let* (($tv_abd (formula-abduction (stv $s_cause $c_cause) (stv 0.90 0.85) (stv $s_pri $c_pri)))
                ($tv_fin (formula-deduction (stv $s_susc $c_susc) $tv_abd)))
           (DifferentialDiagnosis
             (Crop Coffee)
             (Symptom YellowLeaves)
             (HypothesizedCause $disease)
             (CalculatedSTV $tv_fin)))))))

;; ==============================================================================
;; QUERY 4: Evidence Revision (Multi-Source Fusion & Conflicting Evidence)
;; USER: Initial field scouting gave STV (0.85, 0.70). Now lab PCR test gave STV (0.95, 0.90). What is the updated belief?
;; ==============================================================================
!(SECTION "DEMO 4A: Multi-Source Belief Revision (Agreeing Evidence)")
!(USER_QUERY "Fusion of Field Scouting (0.85 0.70) + Laboratory PCR (0.95 0.90)")
!(SYSTEM_REASONING (revise-evidence-sources CoffeeLeafRust FieldVisualScouting (stv 0.85 0.70) LabPCRDiagnostic (stv 0.95 0.90)))

!(SECTION "DEMO 4B: Conflicting Evidence Revision")
!(USER_QUERY "Conflicting: Visual Rust Symptoms (0.90 0.80) vs Negative Lab Test (0.10 0.80)")
!(SYSTEM_REASONING (revise-evidence-sources CoffeeLeafRust FieldVisualScouting (stv 0.90 0.80) NegativeLabTest (stv 0.10 0.80)))

;; ==============================================================================
;; QUERY 5: Multi-Step Causal Chaining with Uncertainty Propagation (3-Hop Path)
;; USER: How does poor field drainage lead to plant wilting?
;; ==============================================================================
!(SECTION "DEMO 5: Multi-Step Causal Chaining (PoorDrainage -> WaterloggedSoil -> RootRot -> Wilting)")
!(USER_QUERY "Trace causal path from PoorDrainage to Wilting")
!(SYSTEM_REASONING (chain-3-hop &self promotes PoorDrainage WaterloggedSoil increases-risk RootRot causes Wilting))

;; ==============================================================================
;; QUERY 6: Goal-Driven Backward Chaining
;; USER: Verify if Coffee Leaf Rust is the cause on a coffee farm with high humidity and orange leaf spots.
;; ==============================================================================
!(SECTION "DEMO 6: Goal-Driven Backward Chaining Proof Tree")
!(USER_QUERY "Goal: Verify CoffeeLeafRust with complete supporting observations")
!(SYSTEM_REASONING (backward-verify-goal-complete &self Coffee CoffeeLeafRust HighHumidity OrangeLeafSpots))

;; ==============================================================================
;; QUERY 7: Inductive Rule Learning from Farm Survey Data
;; USER: In our regional agricultural survey, 18 out of 20 farms with high humidity developed rust. Can we induce a risk rule?
;; ==============================================================================
!(SECTION "DEMO 7: Inductive Risk Rule Learning from Agricultural Field Surveys")
!(USER_QUERY "Induce risk rule from 18 positive cases out of 20 surveyed farms")
!(SYSTEM_REASONING (induce-farm-risk-rule HighHumidity CoffeeLeafRust 18.0 20.0))
