;; ==============================================================================
;; agri-pln-metta: Diseases and Disorders Knowledge Module
;; ==============================================================================
;; Defines plant diseases, pathogens, abiotic nutrient deficiencies,
;; biological classifications, severity ratings, and prior base rates.
;; ==============================================================================

;; Disease Entities
(Disease CoffeeLeafRust)
(Disease CoffeeBerryDisease)
(Disease BrownEyeSpot)
(Disease MaizeRust)
(Disease NorthernLeafBlight)
(Disease WheatStemRust)
(Disease PowderyMildew)
(Disease TeffRust)
(Disease LateBlight)
(Disease EarlyBlight)
(Disease BacterialWilt)
(Disease RootRot)
(Disease NitrogenDeficiency)
(Disease PotassiumDeficiency)

;; Pathogen and Etiology Classification
(PathogenType CoffeeLeafRust Fungal_Hemileia_vastatrix)
(PathogenType CoffeeBerryDisease Fungal_Colletotrichum_kahawae)
(PathogenType BrownEyeSpot Fungal_Cercospora_coffeicola)
(PathogenType MaizeRust Fungal_Puccinia_sorghi)
(PathogenType NorthernLeafBlight Fungal_Exserohilum_turcicum)
(PathogenType WheatStemRust Fungal_Puccinia_graminis)
(PathogenType PowderyMildew Fungal_Erysiphales)
(PathogenType TeffRust Fungal_Uromyces_eragrostidis)
(PathogenType LateBlight Oomycete_Phytophthora_infestans)
(PathogenType EarlyBlight Fungal_Alternaria_solani)
(PathogenType BacterialWilt Bacterial_Ralstonia_solanacearum)
(PathogenType RootRot Fungal_Fusarium_Pythium_Complex)
(PathogenType NitrogenDeficiency Abiotic_Nutrient_Disorder)
(PathogenType PotassiumDeficiency Abiotic_Nutrient_Disorder)

;; Broad Classification Type
(DiseaseCategory CoffeeLeafRust FungalFoliar)
(DiseaseCategory CoffeeBerryDisease FungalFruit)
(DiseaseCategory BrownEyeSpot FungalFoliar)
(DiseaseCategory MaizeRust FungalFoliar)
(DiseaseCategory NorthernLeafBlight FungalFoliar)
(DiseaseCategory WheatStemRust FungalFoliar)
(DiseaseCategory PowderyMildew FungalFoliar)
(DiseaseCategory TeffRust FungalFoliar)
(DiseaseCategory LateBlight OomyceteFoliarAndTuber)
(DiseaseCategory EarlyBlight FungalFoliar)
(DiseaseCategory BacterialWilt BacterialVascular)
(DiseaseCategory RootRot FungalRootSystem)
(DiseaseCategory NitrogenDeficiency AbioticNutritional)
(DiseaseCategory PotassiumDeficiency AbioticNutritional)

;; Baseline Regional Disease Priors P(Disease)
;; Represents background probability of occurrence across typical agricultural field seasons
(PriorDisease CoffeeLeafRust (stv 0.30 0.85))
(PriorDisease CoffeeBerryDisease (stv 0.20 0.80))
(PriorDisease BrownEyeSpot (stv 0.25 0.75))
(PriorDisease MaizeRust (stv 0.28 0.80))
(PriorDisease NorthernLeafBlight (stv 0.22 0.75))
(PriorDisease WheatStemRust (stv 0.25 0.80))
(PriorDisease PowderyMildew (stv 0.30 0.80))
(PriorDisease TeffRust (stv 0.22 0.75))
(PriorDisease LateBlight (stv 0.35 0.85))
(PriorDisease EarlyBlight (stv 0.28 0.80))
(PriorDisease BacterialWilt (stv 0.18 0.75))
(PriorDisease RootRot (stv 0.22 0.75))
(PriorDisease NitrogenDeficiency (stv 0.40 0.85))
(PriorDisease PotassiumDeficiency (stv 0.25 0.80))
