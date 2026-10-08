;; ============================================================
;; AGRICULTURAL RULE BASE
;; Rules only
;;
;; Rule structure:
;;
;; (: RULE_ID
;;    (rule
;;       premise-1
;;       premise-2
;;       conclusion
;;       (stv strength confidence)))
;;
;; Rules are stored directly as atoms in &self so they are
;; visible after import.
;; ============================================================


;; ============================================================
;; WATER STRESS
;; ============================================================

;; R1:
;; Dry soil + high temperature
;; -> coffee plant is water stressed

(: R1
   (rule
      (soil-dry)
      (temperature-high)
      (coffee-plant-water-stressed)
      (stv 0.92 0.85)))


;; ============================================================
;; IRRIGATION RECOMMENDATION
;; ============================================================

;; R2:
;; Water stress + water available
;; -> irrigation recommended

(: R2
   (rule
      (coffee-plant-water-stressed)
      (water-available)
      (irrigation-recommended)
      (stv 0.90 0.82)))


;; ============================================================
;; STRONGER IRRIGATION ACTION
;; ============================================================

;; R3:
;; Irrigation recommended + farmer can irrigate
;; -> irrigate coffee plant

(: R3
   (rule
      (irrigation-recommended)
      (farmer-can-irrigate)
      (irrigate-coffee-plant)
      (stv 0.95 0.88)))


;; ============================================================
;; DISEASE RISK
;; ============================================================

;; R4:
;; Orange leaf spots + favorable humidity
;; -> coffee leaf rust suspected

(: R4
   (rule
      (coffee-leaves-have-orange-spots)
      (leaf-rust-favorable-humidity)
      (coffee-leaf-rust-suspected)
      (stv 0.88 0.78)))


;; ============================================================
;; DISEASE MANAGEMENT
;; ============================================================

;; R5:
;; Rust suspected + farmer can irrigate
;; -> inspect coffee field

(: R5
   (rule
      (coffee-leaf-rust-suspected)
      (farmer-can-irrigate)
      (inspect-coffee-field)
      (stv 0.75 0.65)))


;; ============================================================
;; MULTI-HOP AGRICULTURAL REASONING
;; ============================================================

;; R6:
;; Wilting + water stress
;; -> irrigation urgency high

(: R6
   (rule
      (coffee-leaves-wilting)
      (coffee-plant-water-stressed)
      (irrigation-urgency-high)
      (stv 0.86 0.75)))


;; R7:
;; Irrigation urgency high + water available
;; -> immediate irrigation recommended

(: R7
   (rule
      (irrigation-urgency-high)
      (water-available)
      (immediate-irrigation-recommended)
      (stv 0.93 0.80)))