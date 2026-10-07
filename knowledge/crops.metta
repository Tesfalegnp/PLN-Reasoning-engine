;; ==============================================================================
;; agri-pln-metta: Crops Knowledge Module
;; ==============================================================================
;; Defines agricultural crops, botanical families, economic context,
;; environmental affinities, and disease susceptibilities with PLN STVs.
;; ==============================================================================

;; Crop Entities
(Crop Coffee)
(Crop Maize)
(Crop Wheat)
(Crop Teff)
(Crop Tomato)
(Crop Potato)
(Crop Barley)

;; Crop Classification
(CropFamily Coffee Rubiaceae)
(CropFamily Maize Poaceae)
(CropFamily Wheat Poaceae)
(CropFamily Teff Poaceae)
(CropFamily Tomato Solanaceae)
(CropFamily Potato Solanaceae)
(CropFamily Barley Poaceae)

;; Crop Category
(CropType Coffee PerennialCashCrop)
(CropType Maize CerealStaple)
(CropType Wheat CerealStaple)
(CropType Teff IndigenousCereal)
(CropType Tomato Horticultural)
(CropType Potato TuberCrop)
(CropType Barley CerealCrop)

;; Crop Disease Susceptibilities with PLN Simple Truth Values (Strength Confidence)
;; Strength = conditional probability of disease occurrence given crop presence in susceptible environment
;; Confidence = empirical agronomic evidence certainty
(Susceptible Coffee CoffeeLeafRust (stv 0.85 0.90))
(Susceptible Coffee CoffeeBerryDisease (stv 0.70 0.85))
(Susceptible Coffee BrownEyeSpot (stv 0.65 0.80))
(Susceptible Coffee RootRot (stv 0.60 0.75))

(Susceptible Maize MaizeRust (stv 0.80 0.85))
(Susceptible Maize NorthernLeafBlight (stv 0.75 0.80))
(Susceptible Maize NitrogenDeficiency (stv 0.70 0.85))

(Susceptible Wheat WheatStemRust (stv 0.85 0.90))
(Susceptible Wheat PowderyMildew (stv 0.75 0.80))
(Susceptible Wheat FusariumHeadBlight (stv 0.65 0.75))

(Susceptible Teff TeffRust (stv 0.75 0.80))
(Susceptible Teff DampingOff (stv 0.60 0.70))
(Susceptible Teff NitrogenDeficiency (stv 0.65 0.75))

(Susceptible Tomato LateBlight (stv 0.90 0.95))
(Susceptible Tomato EarlyBlight (stv 0.80 0.85))
(Susceptible Tomato BacterialWilt (stv 0.70 0.80))

(Susceptible Potato LateBlight (stv 0.92 0.95))
(Susceptible Potato BacterialWilt (stv 0.72 0.80))
(Susceptible Potato PotatoScab (stv 0.60 0.70))

;; Crop Prior Base Rates (Baseline presence in targeted farming zones)
(PriorCrop Coffee (stv 0.95 0.99))
(PriorCrop Maize (stv 0.95 0.99))
(PriorCrop Wheat (stv 0.90 0.99))
(PriorCrop Teff (stv 0.92 0.99))
(PriorCrop Tomato (stv 0.88 0.99))
(PriorCrop Potato (stv 0.85 0.99))
