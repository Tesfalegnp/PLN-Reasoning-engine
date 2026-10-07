;; ==============================================================================
;; agri-pln-metta: Simple Truth Value (STV) Module
;; ==============================================================================
;; STV represents uncertainty in Probabilistic Logic Networks (PLN) using two values:
;;   - Strength (s in [0.0, 1.0]): Probability / degree of truth of the proposition
;;   - Confidence (c in [0.0, 1.0]): Epistemic certainty / amount of evidence supporting it
;; ==============================================================================

;; Basic numerical helper functions
(= (min $a $b) (if (< $a $b) $a $b))
(= (max $a $b) (if (> $a $b) $a $b))
(= (clamp $v $lo $hi) (min $hi (max $lo $v)))

;; STV Constructors and Getters
(= (stv-create $s $c)
   (stv (clamp $s 0.0 1.0) (clamp $c 0.0 1.0)))

(= (stv-s (stv $s $c)) $s)
(= (stv-c (stv $s $c)) $c)

;; Validation: Check if truth value numbers are valid floats within [0.0, 1.0]
(= (stv-valid (stv $s $c))
   (and (and (>= $s 0.0) (<= $s 1.0))
        (and (>= $c 0.0) (<= $c 1.0))))

;; Weight of Evidence conversions
;; In PLN, confidence c relates to evidence weight w via: c = w / (w + k), w = k * c / (1 - c)
;; Default personality parameter k = 1.0
(= (stv-weight (stv $s $c))
   (/ $c (+ (- 1.0 (clamp $c 0.0 0.9999)) 0.0001)))

(= (weight-to-conf $w)
   (/ (max 0.0 $w) (+ (max 0.0 $w) 1.0)))

;; Format STV for human-readable output
(= (stv-display (stv $s $c))
   (STV (Strength $s) (Confidence $c)))
