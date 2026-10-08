;; ============================================================
;; FORWARD CHAINING ENGINE
;;
;; Data-driven reasoning:
;;
;; known facts → match rule premises → derive conclusion
;;            → use conclusion as new premise → continue
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


;; Base case -------------------------------------------------------
(= (fc-step $fact $space Z) $fact)


;; Recursive case --------------------------------------------------
(= (fc-step $premise $space (S $k))
    (match $space
        (: $rid (rule $p1 $p2 $conclusion $rtv))
        (if (== $premise $p1)
            (match $space
                (: $fid $p2 $ftv)
                (fc-step $conclusion $space $k))
            (if (== $premise $p2)
                (match $space
                    (: $fid $p1 $ftv)
                    (fc-step $conclusion $space $k))
                $premise))))


;; Public query ----------------------------------------------------
(= (forward-query $start $space $depth)
    (fc-step $start $space $depth))