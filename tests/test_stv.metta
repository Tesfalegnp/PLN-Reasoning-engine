;; ==============================================================================
;; Test Suite: Simple Truth Values (STV)
;; ==============================================================================

!(register-module! ../pln)
!(import! &self pln:stv)

;; Test 1: STV Creation
!(assertEqual (stv-create 0.85 0.90) (stv 0.85 0.9))

;; Test 2: STV Clamping (upper and lower bounds)
!(assertEqual (stv-create 1.5 -0.3) (stv 1.0 0.0))

;; Test 3: STV Getters
!(assertEqual (stv-s (stv 0.75 0.80)) 0.75)
!(assertEqual (stv-c (stv 0.75 0.80)) 0.80)

;; Test 4: STV Validation
!(assertEqual (stv-valid (stv 0.50 0.50)) True)

;; Test 5: STV Display Representation
!(assertEqual (stv-display (stv 0.80 0.90)) (STV (Strength 0.8) (Confidence 0.9)))

;; Test 6: Weight of Evidence Conversion
!(assertEqual (> (stv-weight (stv 0.80 0.80)) 3.5) True)
!(assertEqual (< (stv-weight (stv 0.80 0.80)) 4.5) True)
!(assertEqual (> (weight-to-conf 4.0) 0.75) True)
