;; ====================================================================
;; Coffee Agriculture & Coffee Plant Disease Knowledge Base
;; Domain: Agronomy & Plant Pathology
;; Supported Pathologies:
;;   - Coffee Leaf Rust (Hemileia vastatrix)
;;   - Coffee Berry Disease (Colletotrichum kahawae)
;;   - Nitrogen Chlorosis / Nutrient Deficiency
;; ====================================================================

;; --------------------------------------------------------------------
;; Agricultural Domain Ontology & Concept Types
;; --------------------------------------------------------------------
(: CoffeePlant Type)
(: Disease Type)
(: Symptom Type)
(: EnvironmentalRisk Type)
(: SoilCondition Type)
(: Treatment Type)
(: Variety Type)

;; Entities
(: CoffeePlant01 CoffeePlant)
(: CoffeePlant02 CoffeePlant)
(: CoffeePlant03 CoffeePlant)
(: CoffeePlant04 CoffeePlant)

(: CoffeeLeafRust Disease)
(: CoffeeBerryDisease Disease)
(: NitrogenDeficiency Disease)

(: OrangeRustPustules Symptom)
(: DarkBerryLesions Symptom)
(: YellowLeafChlorosis Symptom)
(: BerryNecrosis Symptom)
(: PrematureLeafDrop Symptom)

(: HighHumidity EnvironmentalRisk)
(: HeavyRainfall EnvironmentalRisk)
(: DenseShadedCanopy EnvironmentalRisk)
(: AcidicLeachedSoil SoilCondition)

(: CopperFungicideSpray Treatment)
(: TargetedBerryFungicide Treatment)
(: NitrogenFertilizer Treatment)
(: CanopyPruning Treatment)

;; --------------------------------------------------------------------
;; Knowledge Base Definition: (kb)
;; Evaluated natively by Backward Chainer and Forward Chainer
;; --------------------------------------------------------------------
(= (kb)
   (superpose (
     ;; ----------------------------------------------------------------
     ;; 1. Observed Field Facts (Field Scouting & Sensor Observations)
     ;; ----------------------------------------------------------------
     ;; CoffeePlant01: Classic Coffee Leaf Rust presentation in humid plot
     (⊢ (HasSymptom CoffeePlant01 OrangeRustPustules) (stv 0.88 0.85))
     (⊢ (HasSymptom CoffeePlant01 YellowLeafChlorosis) (stv 0.75 0.70))
     (⊢ (EnvironmentalRisk CoffeePlant01 HighHumidity) (stv 0.92 0.90))
     (⊢ (EnvironmentalRisk CoffeePlant01 DenseShadedCanopy) (stv 0.80 0.75))
     (⊢ (Inheritance CoffeePlant01 ArabicaBourbon) (stv 1.00 0.95))

     ;; CoffeePlant02: Coffee Berry Disease presentation during wet season
     (⊢ (HasSymptom CoffeePlant02 DarkBerryLesions) (stv 0.90 0.85))
     (⊢ (HasSymptom CoffeePlant02 BerryNecrosis) (stv 0.82 0.78))
     (⊢ (EnvironmentalRisk CoffeePlant02 HeavyRainfall) (stv 0.85 0.80))

     ;; CoffeePlant03: Nutrient Deficiency presentation (soil leaching)
     (⊢ (HasSymptom CoffeePlant03 YellowLeafChlorosis) (stv 0.85 0.80))
     (⊢ (SoilCondition CoffeePlant03 AcidicLeachedSoil) (stv 0.80 0.75))

     ;; CoffeePlant04: Negative control (healthy/early plot without pustules or lesions)
     (⊢ (EnvironmentalRisk CoffeePlant04 HighHumidity) (stv 0.60 0.50))

     ;; Variety taxonomy & susceptibility
     (⊢ (Inheritance ArabicaBourbon SusceptibleToRust) (stv 0.95 0.90))
     (⊢ (Similarity ArabicaTypica ArabicaBourbon) (stv 0.90 0.85))

     ;; ----------------------------------------------------------------
     ;; 2. Agronomic Diagnostic Rules (Modus Ponens Implications)
     ;; ----------------------------------------------------------------
     ;; Diagnostic: Specific symptom -> Disease afflicted
     (⊢ (→ (HasSymptom $p OrangeRustPustules) (AfflictedWith $p CoffeeLeafRust)) (stv 0.95 0.90))
     (⊢ (→ (HasSymptom $p DarkBerryLesions) (AfflictedWith $p CoffeeBerryDisease)) (stv 0.92 0.88))
     (⊢ (→ (HasSymptom $p BerryNecrosis) (AfflictedWith $p CoffeeBerryDisease)) (stv 0.88 0.82))

     ;; Agronomic differentiation: YellowLeafChlorosis can indicate NitrogenDeficiency
     (⊢ (→ (HasSymptom $p YellowLeafChlorosis) (AfflictedWith $p NitrogenDeficiency)) (stv 0.80 0.75))

     ;; Therapeutic Protocols: Disease afflicted -> Treatment required
     (⊢ (→ (AfflictedWith $p CoffeeLeafRust) (RequiresTreatment $p CopperFungicideSpray)) (stv 0.92 0.88))
     (⊢ (→ (AfflictedWith $p CoffeeBerryDisease) (RequiresTreatment $p TargetedBerryFungicide)) (stv 0.90 0.85))
     (⊢ (→ (AfflictedWith $p NitrogenDeficiency) (RequiresTreatment $p NitrogenFertilizer)) (stv 0.95 0.92))

     ;; Cultural & Environmental Management
     (⊢ (→ (EnvironmentalRisk $p DenseShadedCanopy) (RequiresTreatment $p CanopyPruning)) (stv 0.85 0.80))

     ;; Multi-step climate risk progression
     (⊢ (→ (EnvironmentalRisk $p HighHumidity) (FavorableMicroclimate $p RustFavorable)) (stv 0.88 0.85))
     (⊢ (→ (FavorableMicroclimate $p RustFavorable) (ElevatedRustRisk $p)) (stv 0.85 0.80))
   )))
