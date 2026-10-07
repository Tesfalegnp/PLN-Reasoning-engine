;; ==============================================================================
;; agri-pln-metta: Environmental Risk Queries Module
;; ==============================================================================
;; Provides domain queries for proactive disease risk forecasting:
;;   - Single-condition crop vulnerability
;;   - Compound multi-condition risk assessment (e.g. HighHumidity + WarmTemperature)
;;   - Microclimate propagation risk (e.g. DenseCanopy -> HighHumidity -> Disease)
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)
!(import! &self pln:chaining)
!(import! &self pln:revision)

;; Query 1: Single Condition Risk Assessment for Crop
(= (query-crop-risk $crop $condition)
   (match &self (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match &self (Relation increases-risk $condition $disease (stv $s_risk $c_risk))
       (let $tv_risk (formula-deduction (stv $s_susc $c_susc) (stv $s_risk $c_risk))
         (CropRiskAssessment
           (Crop $crop)
           (EnvironmentalTrigger $condition)
           (VulnerableDisease $disease)
           (STV $tv_risk)
           (RiskLevel (if (> (stv-s $tv_risk) 0.65) HighRisk ModerateRisk))
           (Path ($condition -> increases-risk -> $disease)))))))

;; Query 2: Compound Multi-Condition Risk Assessment (HighHumidity + WarmTemperature)
(= (query-compound-risk $crop $condition1 $condition2)
   (match &self (Susceptible $crop $disease (stv $s_susc $c_susc))
     (match &self (Relation increases-risk $condition1 $disease (stv $s1 $c1))
       (match &self (Relation increases-risk $condition2 $disease (stv $s2 $c2))
         (let* (($tv_risk1 (formula-deduction (stv $s_susc $c_susc) (stv $s1 $c1)))
                ($tv_risk2 (formula-deduction (stv $s_susc $c_susc) (stv $s2 $c2)))
                ($tv_compound (formula-revision $tv_risk1 $tv_risk2)))
           (CompoundRiskAssessment
             (Crop $crop)
             (Conditions ($condition1 $condition2))
             (VulnerableDisease $disease)
             (CompoundSTV $tv_compound)
             (Inference DualConditionRiskRevision)))))))

;; Query 3: Microclimate Chain Risk (e.g. DenseCanopyShade -> HighHumidity -> CoffeeLeafRust)
(= (query-microclimate-chain-risk $crop $cultural_factor $intermediate_condition)
   (match &self (Relation promotes $cultural_factor $intermediate_condition (stv $s1 $c1))
     (match &self (Susceptible $crop $disease (stv $s_susc $c_susc))
       (match &self (Relation increases-risk $intermediate_condition $disease (stv $s2 $c2))
         (let* (($tv_chain (formula-deduction (stv $s1 $c1) (stv $s2 $c2)))
                ($tv_final (formula-deduction (stv $s_susc $c_susc) $tv_chain)))
           (MicroclimateChainResult
             (Crop $crop)
             (RootCause $cultural_factor)
             (PromotedCondition $intermediate_condition)
             (ResultingDiseaseRisk $disease)
             (STV $tv_final)
             (Path ($cultural_factor -> promotes -> $intermediate_condition -> increases-risk -> $disease))))))))
