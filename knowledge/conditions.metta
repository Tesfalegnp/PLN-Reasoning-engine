;; ==============================================================================
;; agri-pln-metta: Environmental and Soil Conditions Knowledge Module
;; ==============================================================================
;; Defines weather parameters, soil conditions, cultural microclimates,
;; and their probabilistic risk influence on plant diseases and disorders.
;; ==============================================================================

;; Condition Entities
(Condition HighHumidity)
(Condition ExcessMoisture)
(Condition PoorDrainage)
(Condition WaterloggedSoil)
(Condition WarmTemperature)
(Condition HighTemperature)
(Condition DroughtStress)
(Condition DenseCanopyShade)
(Condition AcidicSoil)
(Condition OverheadIrrigation)
(Condition LowSoilFertility)
(Condition PoorAirCirculation)

;; Environmental Condition Categories
(ConditionCategory HighHumidity AtmosphericMicroclimate)
(ConditionCategory ExcessMoisture PrecipitationMoisture)
(ConditionCategory PoorDrainage EdaphicSoilPhysics)
(ConditionCategory WaterloggedSoil EdaphicSoilPhysics)
(ConditionCategory WarmTemperature AtmosphericThermal)
(ConditionCategory HighTemperature AtmosphericThermal)
(ConditionCategory DroughtStress WaterDeficit)
(ConditionCategory DenseCanopyShade CulturalManagement)
(ConditionCategory AcidicSoil EdaphicSoilChemistry)
(ConditionCategory OverheadIrrigation CulturalManagement)
(ConditionCategory LowSoilFertility EdaphicNutritional)
(ConditionCategory PoorAirCirculation CulturalMicroclimate)

;; Inter-Condition Causal Influence: (Relation promotes <ConditionA> <ConditionB> (stv Strength Confidence))
(Relation promotes PoorDrainage WaterloggedSoil (stv 0.90 0.85))
(Relation promotes OverheadIrrigation HighHumidity (stv 0.85 0.80))
(Relation promotes DenseCanopyShade HighHumidity (stv 0.80 0.80))
(Relation promotes DenseCanopyShade PoorAirCirculation (stv 0.85 0.85))
(Relation promotes ExcessMoisture HighHumidity (stv 0.92 0.90))
(Relation promotes PoorAirCirculation HighHumidity (stv 0.78 0.75))

;; Environmental Risk Influence on Diseases: (Relation increases-risk <Condition> <Disease> (stv Strength Confidence))
;; Represents P(Disease | Condition) risk amplification

;; Coffee Diseases
(Relation increases-risk HighHumidity CoffeeLeafRust (stv 0.85 0.80))
(Relation increases-risk WarmTemperature CoffeeLeafRust (stv 0.75 0.75))
(Relation increases-risk DenseCanopyShade CoffeeLeafRust (stv 0.70 0.75))
(Relation increases-risk ExcessMoisture CoffeeBerryDisease (stv 0.82 0.80))
(Relation increases-risk LowSoilFertility BrownEyeSpot (stv 0.75 0.70))

;; Cereal Diseases
(Relation increases-risk HighHumidity MaizeRust (stv 0.80 0.80))
(Relation increases-risk WarmTemperature MaizeRust (stv 0.72 0.75))
(Relation increases-risk HighHumidity WheatStemRust (stv 0.82 0.80))
(Relation increases-risk HighHumidity TeffRust (stv 0.75 0.75))
(Relation increases-risk WarmTemperature PowderyMildew (stv 0.78 0.75))

;; Solanaceae & Root Pathogens
(Relation increases-risk ExcessMoisture LateBlight (stv 0.90 0.90))
(Relation increases-risk HighHumidity LateBlight (stv 0.88 0.85))
(Relation increases-risk WaterloggedSoil RootRot (stv 0.88 0.85))
(Relation increases-risk PoorDrainage RootRot (stv 0.82 0.80))
(Relation increases-risk HighTemperature BacterialWilt (stv 0.80 0.75))
(Relation increases-risk WaterloggedSoil BacterialWilt (stv 0.75 0.70))

;; Nutritional Disorders
(Relation increases-risk LowSoilFertility NitrogenDeficiency (stv 0.92 0.90))
(Relation increases-risk AcidicSoil NitrogenDeficiency (stv 0.70 0.75))
(Relation increases-risk AcidicSoil PotassiumDeficiency (stv 0.65 0.70))

;; Physiological Disorders
(Relation increases-risk DroughtStress Wilting (stv 0.88 0.85))
(Relation increases-risk DroughtStress StuntedGrowth (stv 0.80 0.80))
