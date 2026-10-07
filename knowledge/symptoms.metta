;; ==============================================================================
;; agri-pln-metta: Symptoms Knowledge Module
;; ==============================================================================
;; Defines agricultural symptoms and their probabilistic causal relationships
;; with diseases and nutritional deficiencies.
;; ==============================================================================

;; Symptom Entities
(Symptom OrangeLeafSpots)
(Symptom YellowLeaves)
(Symptom BrownPustules)
(Symptom WaterSoakedLesions)
(Symptom WhitePowderyPatches)
(Symptom Wilting)
(Symptom StuntedGrowth)
(Symptom PrematureBerryDrop)
(Symptom MarginalLeafScorching)
(Symptom ConcentricRingSpots)
(Symptom DarkSunkenBerryLesions)
(Symptom StemRustPustules)

;; Symptom Manifestation Site
(SymptomSite OrangeLeafSpots LowerLeafSurface)
(SymptomSite YellowLeaves FoliageGeneral)
(SymptomSite BrownPustules FoliageGeneral)
(SymptomSite WaterSoakedLesions FoliageAndStem)
(SymptomSite WhitePowderyPatches UpperLeafSurface)
(SymptomSite Wilting EntireCanopy)
(SymptomSite StuntedGrowth WholePlant)
(SymptomSite PrematureBerryDrop FruitBerries)
(SymptomSite MarginalLeafScorching LeafMargins)
(SymptomSite ConcentricRingSpots FoliageGeneral)
(SymptomSite DarkSunkenBerryLesions FruitBerries)
(SymptomSite StemRustPustules PlantStem)

;; Causal Relations: (Relation causes <Disease> <Symptom> (stv Strength Confidence))
;; Represents P(Symptom | Disease)

;; Coffee Diseases -> Symptoms
(Relation causes CoffeeLeafRust OrangeLeafSpots (stv 0.90 0.85))
(Relation causes CoffeeLeafRust YellowLeaves (stv 0.70 0.80))
(Relation causes CoffeeLeafRust PrematureLeafDrop (stv 0.75 0.80))

(Relation causes CoffeeBerryDisease DarkSunkenBerryLesions (stv 0.92 0.90))
(Relation causes CoffeeBerryDisease PrematureBerryDrop (stv 0.88 0.85))

(Relation causes BrownEyeSpot ConcentricRingSpots (stv 0.82 0.80))
(Relation causes BrownEyeSpot YellowLeaves (stv 0.60 0.75))

;; Maize & Cereal Diseases -> Symptoms
(Relation causes MaizeRust BrownPustules (stv 0.88 0.85))
(Relation causes MaizeRust YellowLeaves (stv 0.65 0.75))
(Relation causes NorthernLeafBlight ConcentricRingSpots (stv 0.80 0.80))

(Relation causes WheatStemRust StemRustPustules (stv 0.90 0.85))
(Relation causes WheatStemRust BrownPustules (stv 0.85 0.80))

(Relation causes TeffRust BrownPustules (stv 0.82 0.80))
(Relation causes TeffRust YellowLeaves (stv 0.55 0.70))

;; Solanaceae Diseases -> Symptoms
(Relation causes LateBlight WaterSoakedLesions (stv 0.92 0.90))
(Relation causes LateBlight YellowLeaves (stv 0.75 0.80))
(Relation causes LateBlight Wilting (stv 0.70 0.80))

(Relation causes EarlyBlight ConcentricRingSpots (stv 0.85 0.85))
(Relation causes EarlyBlight YellowLeaves (stv 0.65 0.75))

(Relation causes BacterialWilt Wilting (stv 0.90 0.90))
(Relation causes BacterialWilt StuntedGrowth (stv 0.70 0.75))

(Relation causes PowderyMildew WhitePowderyPatches (stv 0.94 0.90))
(Relation causes PowderyMildew YellowLeaves (stv 0.60 0.75))

(Relation causes RootRot Wilting (stv 0.85 0.85))
(Relation causes RootRot YellowLeaves (stv 0.78 0.80))
(Relation causes RootRot StuntedGrowth (stv 0.80 0.85))

;; Abiotic Nutritional Deficiencies -> Symptoms
(Relation causes NitrogenDeficiency YellowLeaves (stv 0.90 0.90))
(Relation causes NitrogenDeficiency StuntedGrowth (stv 0.85 0.85))

(Relation causes PotassiumDeficiency MarginalLeafScorching (stv 0.88 0.85))
(Relation causes PotassiumDeficiency YellowLeaves (stv 0.50 0.70))

;; Diagnostic Inverse Indication: (Relation indicates <Symptom> <Disease> (stv Strength Confidence))
;; Represents P(Disease | Symptom) baseline heuristic indicator
(Relation indicates OrangeLeafSpots CoffeeLeafRust (stv 0.88 0.85))
(Relation indicates DarkSunkenBerryLesions CoffeeBerryDisease (stv 0.90 0.88))
(Relation indicates WaterSoakedLesions LateBlight (stv 0.85 0.85))
(Relation indicates WhitePowderyPatches PowderyMildew (stv 0.92 0.90))
(Relation indicates StemRustPustules WheatStemRust (stv 0.88 0.85))
(Relation indicates MarginalLeafScorching PotassiumDeficiency (stv 0.82 0.80))
