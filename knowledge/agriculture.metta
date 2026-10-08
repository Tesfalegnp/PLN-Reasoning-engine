;; ============================================================
;; AGRICULTURAL KNOWLEDGE BASE
;; Facts only
;;
;; STV format:
;; (stv strength confidence)
;;
;; strength    = estimated degree that the statement is true
;; confidence  = reliability of the available evidence
;; ============================================================


;; ------------------------------------------------------------
;; WEATHER / ENVIRONMENT
;; ------------------------------------------------------------

(: F1 (soil-dry)           (stv 0.90 0.90))
(: F2 (temperature-high)   (stv 0.85 0.88))
(: F3 (rainfall-low)       (stv 0.80 0.82))


;; ------------------------------------------------------------
;; CROP CONDITION
;; ------------------------------------------------------------

(: F4 (coffee-plant-water-stressed)  (stv 0.70 0.65))
(: F5 (coffee-leaves-wilting)        (stv 0.75 0.70))


;; ------------------------------------------------------------
;; RESOURCES
;; ------------------------------------------------------------

(: F6 (water-available)      (stv 0.95 0.90))
(: F7 (farmer-can-irrigate)  (stv 0.90 0.85))


;; ------------------------------------------------------------
;; DISEASE OBSERVATIONS
;; ------------------------------------------------------------

(: F8 (coffee-leaves-have-orange-spots)  (stv 0.88 0.80))
(: F9 (leaf-rust-favorable-humidity)     (stv 0.78 0.72))