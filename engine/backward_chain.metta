;; ============================================================
;; BACKWARD CHAINING ENGINE
;;
;; Goal-driven reasoning:
;;
;; QUERY → find rule producing QUERY → prove each premise
;;       → return proof tree
;;
;; NOTE: No type declarations — MeTTa 0.2.10 prevents full
;; reduction when (: fn (-> ...)) is present.
;;
;; $space is passed in by the caller so that match targets the
;; space where facts and rules actually live.
;; ============================================================


;; Peano naturals --------------------------------------------------
(= (fromNumber $n)
    (if (<= $n 0) Z (S (fromNumber (- $n 1)))))


;; Base case — goal is a known fact (at depth 0) -------------------
(= (bc $goal $space Z)
    (match $space
        (: $fid $goal $tv)
        (proof $fid $goal $tv)))

;; Base case at any depth — facts are provable regardless of
;; remaining depth budget.  Without this, multi-hop proofs fail
;; when a sub-goal is a direct fact but depth > 0. -----------------
(= (bc $goal $space (S $k))
    (match $space
        (: $fid $goal $tv)
        (proof $fid $goal $tv)))

;; Recursive case — find a rule whose conclusion = goal,
;; then recursively prove each premise. ----------------------------
(= (bc $goal $space (S $k))
    (match $space
        (: $rid (rule $p1 $p2 $goal $rtv))
        (let $proof1 (bc $p1 $space $k)
            (let $proof2 (bc $p2 $space $k)
                (proof $rid $proof1 $proof2 $goal $rtv)))))


;; Public query ----------------------------------------------------
(= (backward-query $goal $space $depth)
    (bc $goal $space $depth))