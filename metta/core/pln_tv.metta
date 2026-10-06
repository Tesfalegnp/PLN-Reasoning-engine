;; ====================================================================
;; PLN Truth Value Definitions and Conversions
;; ====================================================================

(: TruthValue Type)
(: stv (-> Number Number TruthValue))

;; Numeric utilities
(: min (-> Number Number Number))
(= (min $a $b) (if (< $a $b) $a $b))

(: max (-> Number Number Number))
(= (max $a $b) (if (> $a $b) $a $b))

;; Clamps a value into [min, max]
(: clamp (-> Number Number Number Number))
(= (clamp $v $min $max)
   (min $max (max $v $min)))

;; Safe division guarding against division by zero
(: /safe (-> Number Number Number))
(= (/safe $a $b)
   (if (> $b 0.000001)
       (/ $a $b)
       0.0))

;; Weight of evidence conversions (Jeffreys prior / count parameter)
;; c = w / (w + 1)  <=>  w = c / (1 - c)
(: Truth_c2w (-> Number Number))
(= (Truth_c2w $c)
   (/safe $c (- 1.0 (min $c 0.999999))))

(: Truth_w2c (-> Number Number))
(= (Truth_w2c $w)
   (/safe $w (+ $w 1.0)))

;; PLN Negation: s' = 1 - s, c' = c
(: Truth_Negation (-> TruthValue TruthValue))
(= (Truth_Negation (stv $s $c))
   (stv (- 1.0 $s) $c))

;; PLN Conjunction / Independent Intersection: s = s1 * s2, c = c1 * c2
(: Truth_Intersection (-> TruthValue TruthValue TruthValue))
(= (Truth_Intersection (stv $s1 $c1) (stv $s2 $c2))
   (let* (($s (clamp (* $s1 $s2) 0.0 1.0))
          ($c (clamp (* $c1 $c2) 0.0 1.0)))
     (stv $s $c)))

;; PLN Disjunction / Independent Union: s = 1 - (1 - s1)*(1 - s2)
(: Truth_Union (-> TruthValue TruthValue TruthValue))
(= (Truth_Union (stv $s1 $c1) (stv $s2 $c2))
   (let* (($s (clamp (- 1.0 (* (- 1.0 $s1) (- 1.0 $s2))) 0.0 1.0))
          ($c (clamp (* $c1 $c2) 0.0 1.0)))
     (stv $s $c)))
