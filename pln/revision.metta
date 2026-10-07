;; ==============================================================================
;; agri-pln-metta: Probabilistic Revision Module
;; ==============================================================================
;; Implements evidence accumulation and belief revision:
;;   Combines independent evidence sources supporting or refuting the same proposition.
;;
;; Key properties:
;;   - Reinforcing evidence (consistent strengths) yields higher combined confidence.
;;   - Conflicting evidence moves combined strength to the evidence-weighted center.
;;   - Programmatically updates beliefs without hard-coded results.
;; ==============================================================================

!(import! &self stv)
!(import! &self formulas)

;; Direct STV revision function
(= (pln-revise (stv $s1 $c1) (stv $s2 $c2))
   (formula-revision (stv $s1 $c1) (stv $s2 $c2)))

;; Revision of two named evidence sources (e.g. Field Scouting vs Lab Test)
(= (revise-evidence-sources $proposition $source1 (stv $s1 $c1) $source2 (stv $s2 $c2))
   (let* (($revised_tv (formula-revision (stv $s1 $c1) (stv $s2 $c2)))
          ($w1 (stv-weight (stv $s1 $c1)))
          ($w2 (stv-weight (stv $s2 $c2))))
     (RevisionResult
       (Proposition $proposition)
       (CombinedSTV $revised_tv)
       (EvidenceSources
         (Source1 $source1 (STV (stv $s1 $c1)) (Weight $w1))
         (Source2 $source2 (STV (stv $s2 $c2)) (Weight $w2)))
       (Inference PLNRevision)
       (Interpretation
         (if (> (stv-c $revised_tv) (max $c1 $c2))
             "Confidence increased through multi-source evidence fusion"
             "Evidence revised")))))

;; Sequential 3-source revision
(= (revise-three-sources $proposition $s1 $c1 $s2 $c2 $s3 $c3)
   (let* (($tv12 (formula-revision (stv $s1 $c1) (stv $s2 $c2)))
          ($tv123 (formula-revision $tv12 (stv $s3 $c3))))
     (ThreeWayRevisionResult
       (Proposition $proposition)
       (FinalSTV $tv123)
       (IntermediateSTV $tv12))))
