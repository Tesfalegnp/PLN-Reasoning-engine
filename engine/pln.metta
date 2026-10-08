;; ============================================================
;; MINI PLN CORE
;;
;; This file contains the basic truth-value operations used by
;; the agricultural reasoning engine.
;;
;; STV = (strength confidence)
;;
;; NOTE: Type declarations `(: fn (-> ...))` are intentionally
;; omitted.  In MeTTa 0.2.10, they prevent the runtime from
;; fully reducing arithmetic and let-bindings inside function
;; bodies.
;; ============================================================


;; STV constructor -------------------------------------------------
(= (stv $s $c) (stv-value $s $c))

;; Accessors -------------------------------------------------------
(= (strength  (stv-value $s $c)) $s)
(= (confidence (stv-value $s $c)) $c)


;; ============================================================
;; SIMPLE PLN DEDUCTION
;; ============================================================
;;
;; new strength    = s1 * s2
;; new confidence  = c1 * c2
;; ============================================================

(= (deduction (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value (* $s1 $s2) (* $c1 $c2)))


;; ============================================================
;; INDUCTION
;; ============================================================
;;
;; s = avg(s1, s2),  c = c1 * c2
;; ============================================================

(= (induction (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value (/ (+ $s1 $s2) 2) (* $c1 $c2)))


;; ============================================================
;; ABDUCTION
;; ============================================================
;;
;; s = s1 * s2,  c = c1 * c2
;; ============================================================

(= (abduction (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value (* $s1 $s2) (* $c1 $c2)))


;; ============================================================
;; REVISION
;; ============================================================
;;
;; Confidence-weighted averaging of two independent
;; pieces of evidence.
;; ============================================================

(= (revision (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value
        (/ (+ (* $s1 $c1) (* $s2 $c2))
           (+ $c1 $c2))
        (/ (+ $c1 $c2) 2)))