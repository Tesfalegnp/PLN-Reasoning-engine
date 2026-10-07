;; ==============================================================================
;; agri-pln-metta: Treatment Recommendation Queries Module
;; ==============================================================================
;; Provides domain queries for Integrated Pest Management (IPM) recommendations:
;;   - Curative treatments for diagnosed diseases
;;   - Preventive remediation for environmental triggers
;;   - Integrated management packages (Curative + Cultural + Preventive)
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)

;; Query 1: Curative Treatments for Diagnosed Disease
(= (query-curative-treatments $disease)
   (match &self (Relation effective-treatment $treatment $disease (stv $s $c))
     (match &self (TreatmentType $treatment $modality)
       (CurativeRecommendation
         (TargetDisease $disease)
         (TreatmentAction $treatment)
         (Modality $modality)
         (EfficacySTV (stv $s $c))
         (ExpectedOutcome "Suppresses active pathogen infection")))))

;; Query 2: Preventive Remediation for Adverse Environmental Conditions
(= (query-preventive-remediation $condition)
   (match &self (Relation alleviates $treatment $condition (stv $s $c))
     (match &self (TreatmentType $treatment $modality)
       (PreventiveRemediation
         (AdverseCondition $condition)
         (RemediationAction $treatment)
         (Modality $modality)
         (AlleviationSTV (stv $s $c))
         (ExpectedOutcome "Mitigates microclimate conducive to pathogen growth")))))

;; Query 3: Integrated Management Package for Crop + Disease + Condition
(= (query-integrated-ipm-package $crop $disease $condition)
   (match &self (Relation effective-treatment $curative $disease (stv $s1 $c1))
     (match &self (Relation alleviates $preventive $condition (stv $s2 $c2))
       (match &self (Susceptible $crop $disease (stv $s_susc $c_susc))
         (let* (($tv_curative (formula-deduction (stv $s_susc $c_susc) (stv $s1 $c1)))
                ($tv_preventive (formula-deduction (stv $s_susc $c_susc) (stv $s2 $c2))))
           (IntegratedIPMPackage
             (Crop $crop)
             (TargetDisease $disease)
             (ConduciveCondition $condition)
             (CurativeAction (Action $curative) (STV $tv_curative))
             (CulturalRemediation (Action $preventive) (STV $tv_preventive))
             (Strategy "Combined Curative Chemical/Biological Suppression + Cultural Microclimate Modification")))))))
