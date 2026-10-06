;; ====================================================================
;; Peano Natural Numbers for Chaining Depth Bounding
;; ====================================================================

(: Nat Type)
(: Z Nat)
(: S (-> Nat Nat))

;; Convert Number to Peano Nat
(: fromNumber (-> Number Nat))
(= (fromNumber $n)
   (if (<= $n 0)
       Z
       (S (fromNumber (- $n 1)))))

;; Convert Peano Nat to Number
(: fromNat (-> Nat Number))
(= (fromNat Z) 0)
(= (fromNat (S $k)) (+ 1 (fromNat $k)))
