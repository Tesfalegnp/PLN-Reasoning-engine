;; ==============================================================================
;; agri-pln-metta: Diagnostic Queries Module
;; ==============================================================================
;; Provides domain-specific diagnostic queries for agricultural extension agents:
;;   - Single-symptom crop diagnosis
;;   - Differential diagnosis (multiple competing candidate causes)
;;   - Multi-symptom composite diagnosis
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)
!(import! &self pln:abduction)
!(import! &self pln:revision)

;; Query 1: Diagnose Crop from Observed Symptom
(= (query-diagnose-symptom $crop $symptom)
   (abduce-crop-diagnosis &self $crop $symptom 0.95 0.90))

;; Query 2: Differential Diagnosis for Symptoms with Multiple Possible Causes (e.g. YellowLeaves)
(= (query-differential-diagnosis $crop $symptom)
   (match &self (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match &self (Relation causes $disease $symptom (stv $s_cause $c_cause))
       (match &self (PriorDisease $disease (stv $s_pri $c_pri))
         (let* (($tv_abduced (formula-abduction (stv $s_cause $c_cause) (stv 0.90 0.85) (stv $s_pri $c_pri)))
                ($tv_final (formula-deduction (stv $s_susc $c_susc) $tv_abduced)))
           (DifferentialCandidate
             (CandidateDisease $disease)
             (CropTarget $crop)
             (SymptomTrigger $symptom)
             (STV $tv_final)
             (Etiology
               (PriorRisk (stv $s_pri $c_pri))
               (SymptomStrength (stv $s_cause $c_cause))
               (CropSusceptibility (stv $s_susc $c_susc)))))))))

;; Query 3: Multi-Symptom Composite Diagnosis (Evidence Revision over two symptoms)
(= (query-multi-symptom-diagnosis $crop $symptom1 $symptom2)
   (match &self (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match &self (Relation causes $disease $symptom1 (stv $s1 $c1))
       (match &self (Relation causes $disease $symptom2 (stv $s2 $c2))
         (match &self (PriorDisease $disease (stv $s_pri $c_pri))
           (let* (($tv_abd1 (formula-abduction (stv $s1 $c1) (stv 0.90 0.85) (stv $s_pri $c_pri)))
                  ($tv_abd2 (formula-abduction (stv $s2 $c2) (stv 0.90 0.85) (stv $s_pri $c_pri)))
                  ($tv_revised (formula-revision $tv_abd1 $tv_abd2))
                  ($tv_final (formula-deduction (stv $s_susc $c_susc) $tv_revised)))
             (MultiSymptomDiagnosisResult
               (Crop $crop)
               (ConfirmedDisease $disease)
               (ObservedSymptoms ($symptom1 $symptom2))
               (STV $tv_final)
               (Inference (Abduction + MultiSymptomRevision)))))))))
