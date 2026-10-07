;; ==============================================================================
;; agri-pln-metta: PLN Mathematical Formulas Module
;; ==============================================================================
;; Implements the core algebraic truth value update formulas for PLN operations:
;;   1. Deduction: Syllogistic forward propagation (A -> B, B -> C |- A -> C)
;;   2. Induction: Generalized rule induction from sample counts or Bayesian inversion
;;   3. Abduction: Diagnostic explanation from observed effects (A -> B, B |- A)
;;   4. Revision: Independent evidence combination (E1, E2 for proposition X)
;;   5. Conjunction: Combining multi-premise evidence
;; ==============================================================================

!(import! &self stv)

;; 1. Probabilistic Deduction Formula
;; Calculates truth value for transitivity A -> C given A -> B and B -> C
(= (formula-deduction (stv $s1 $c1) (stv $s2 $c2))
   (let* (($s (* $s1 $s2))
          ($c (* (* $c1 $c2) (max 0.1 $s1))))
     (stv (clamp $s 0.0 1.0) (clamp $c 0.0 1.0))))

;; 2. Probabilistic Induction Formulas
;; A. Sample count induction (e.g. from farm observations)
(= (formula-induction-samples $pos $total $k)
   (let* (($s (if (<= $total 0.0) 0.0 (/ $pos $total)))
          ($c (if (<= $total 0.0) 0.0 (/ $total (+ $total $k)))))
     (stv (clamp $s 0.0 1.0) (clamp $c 0.0 1.0))))

;; B. Bayesian inverse induction (induce A -> B from B -> A and marginals P(A), P(B))
(= (formula-induction-bayes (stv $s_ba $c_ba) (stv $s_a $c_a) (stv $s_b $c_b))
   (let* (($s (/ (* $s_ba $s_b) (+ $s_a 0.0001)))
          ($c (* (* $c_ba $c_a) $c_b)))
     (stv (clamp $s 0.0 1.0) (clamp $c 0.0 1.0))))

;; 3. Probabilistic Abduction Formula
;; Calculates truth value of cause A given rule A -> B, observed effect B, and prior P(A)
(= (formula-abduction (stv $s_rule $c_rule) (stv $s_obs $c_obs) (stv $s_pri $c_pri))
   (let* (($num (* (* $s_obs $s_rule) $s_pri))
          ($den (+ (* $s_rule $s_pri) (* (- 1.0 $s_rule) (- 1.0 $s_pri))))
          ($s (if (<= $den 0.0) 0.0 (/ $num (+ $den 0.00001))))
          ($c (* (* (* $c_rule $c_obs) $c_pri) 0.85)))
     (stv (clamp $s 0.0 1.0) (clamp $c 0.0 1.0))))

;; Default abduction when prior is unspecified (uses agricultural domain default prior 0.25 0.60)
(= (formula-abduction-default (stv $s_rule $c_rule) (stv $s_obs $c_obs))
   (formula-abduction (stv $s_rule $c_rule) (stv $s_obs $c_obs) (stv 0.25 0.60)))

;; 4. Probabilistic Revision Formula
;; Combines independent evidence streams for the same proposition
(= (formula-revision (stv $s1 $c1) (stv $s2 $c2))
   (let* (($w1 (stv-weight (stv $s1 $c1)))
          ($w2 (stv-weight (stv $s2 $c2)))
          ($wtot (+ $w1 $w2))
          ($s (if (<= $wtot 0.0) 0.0 (/ (+ (* $w1 $s1) (* $w2 $s2)) $wtot)))
          ($c (weight-to-conf $wtot)))
     (stv (clamp $s 0.0 1.0) (clamp $c 0.0 1.0))))

;; 5. Probabilistic Conjunction Formula (Independent Premise Combination)
(= (formula-conjunction (stv $s1 $c1) (stv $s2 $c2))
   (let* (($s (* $s1 $s2))
          ($c (* $c1 $c2)))
     (stv (clamp $s 0.0 1.0) (clamp $c 0.0 1.0))))
