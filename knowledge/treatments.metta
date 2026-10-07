;; ==============================================================================
;; agri-pln-metta: Treatments and Interventions Knowledge Module
;; ==============================================================================
;; Defines agricultural treatments, fungicides, cultural management actions,
;; biological controls, and their probabilistic effectiveness against diseases.
;; ==============================================================================

;; Treatment Entities
(Treatment CopperFungicide)
(Treatment SystemicFungicide)
(Treatment ImproveDrainage)
(Treatment CanopyPruning)
(Treatment BalancedNPKFertilization)
(Treatment DripIrrigationConversion)
(Treatment RemoveInfectedDebris)
(Treatment ResistantCultivar)
(Treatment BioControlTrichoderma)
(Treatment SoilLiming)

;; Treatment Modality Classification
(TreatmentType CopperFungicide ChemicalContactProtectant)
(TreatmentType SystemicFungicide ChemicalSystemicCurative)
(TreatmentType ImproveDrainage CulturalPhysicalAgronomy)
(TreatmentType CanopyPruning CulturalMicroclimateManagement)
(TreatmentType BalancedNPKFertilization AgronomicNutritional)
(TreatmentType DripIrrigationConversion WaterManagementEngineering)
(TreatmentType RemoveInfectedDebris SanitationPhytosanitary)
(TreatmentType ResistantCultivar GeneticBreedingHostResistance)
(TreatmentType BioControlTrichoderma BiologicalAntagonism)
(TreatmentType SoilLiming EdaphicChemicalAmendment)

;; Treatment Effectiveness against Diseases: (Relation effective-treatment <Treatment> <Disease> (stv Strength Confidence))
;; Represents P(DiseaseSuppression | TreatmentApplied)

;; Coffee Treatments
(Relation effective-treatment CopperFungicide CoffeeLeafRust (stv 0.88 0.85))
(Relation effective-treatment SystemicFungicide CoffeeLeafRust (stv 0.92 0.90))
(Relation effective-treatment CanopyPruning CoffeeLeafRust (stv 0.70 0.80))
(Relation effective-treatment ResistantCultivar CoffeeLeafRust (stv 0.95 0.95))

(Relation effective-treatment CopperFungicide CoffeeBerryDisease (stv 0.85 0.85))
(Relation effective-treatment SystemicFungicide CoffeeBerryDisease (stv 0.90 0.90))
(Relation effective-treatment RemoveInfectedDebris CoffeeBerryDisease (stv 0.75 0.80))

(Relation effective-treatment BalancedNPKFertilization BrownEyeSpot (stv 0.80 0.80))
(Relation effective-treatment CopperFungicide BrownEyeSpot (stv 0.78 0.75))

;; Cereal Treatments
(Relation effective-treatment SystemicFungicide MaizeRust (stv 0.85 0.85))
(Relation effective-treatment ResistantCultivar MaizeRust (stv 0.92 0.90))
(Relation effective-treatment SystemicFungicide WheatStemRust (stv 0.88 0.85))
(Relation effective-treatment ResistantCultivar WheatStemRust (stv 0.95 0.95))
(Relation effective-treatment SystemicFungicide PowderyMildew (stv 0.90 0.88))
(Relation effective-treatment SystemicFungicide TeffRust (stv 0.80 0.80))

;; Solanaceae & Root Treatments
(Relation effective-treatment CopperFungicide LateBlight (stv 0.82 0.85))
(Relation effective-treatment SystemicFungicide LateBlight (stv 0.94 0.92))
(Relation effective-treatment ResistantCultivar LateBlight (stv 0.90 0.90))

(Relation effective-treatment ImproveDrainage RootRot (stv 0.85 0.85))
(Relation effective-treatment BioControlTrichoderma RootRot (stv 0.78 0.75))
(Relation effective-treatment ResistantCultivar BacterialWilt (stv 0.88 0.85))

;; Nutritional & Soil Amendments
(Relation effective-treatment BalancedNPKFertilization NitrogenDeficiency (stv 0.95 0.95))
(Relation effective-treatment BalancedNPKFertilization PotassiumDeficiency (stv 0.92 0.90))
(Relation effective-treatment SoilLiming AcidicSoil (stv 0.90 0.90))

;; Treatment Alleviation of Environmental Conditions: (Relation alleviates <Treatment> <Condition> (stv Strength Confidence))
(Relation alleviates CanopyPruning HighHumidity (stv 0.75 0.80))
(Relation alleviates CanopyPruning DenseCanopyShade (stv 0.90 0.90))
(Relation alleviates CanopyPruning PoorAirCirculation (stv 0.85 0.85))
(Relation alleviates ImproveDrainage PoorDrainage (stv 0.92 0.90))
(Relation alleviates ImproveDrainage WaterloggedSoil (stv 0.90 0.90))
(Relation alleviates DripIrrigationConversion HighHumidity (stv 0.80 0.80))
(Relation alleviates SoilLiming AcidicSoil (stv 0.90 0.90))
