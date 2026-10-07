;; ==============================================================================
;; agri-pln-metta: Multi-Step Chaining Module
;; ==============================================================================
;; Implements multi-hop causal and probabilistic inference across arbitrary path lengths
;; (e.g. A -> B -> C -> D), propagating uncertainty across each hop and recording
;; full explanatory proof paths.
;; ==============================================================================

!(import! &self stv)
!(import! &self formulas)
!(import! &self deduction)

;; 2-hop Causal Chain: A -> B -> C
(= (chain-2-hop $space $r1 $a $b $r2 $c)
   (match $space (Relation $r1 $a $b (stv $s1 $c1))
     (match $space (Relation $r2 $b $c (stv $s2 $c2))
       (let $tv_ccln (formula-deduction (stv $s1 $c1) (stv $s2 $c2))
         (ChainProof
           (HopCount 2)
           (Start $a)
           (End $c)
           (STV $tv_ccln)
           (Path ($a -> $b -> $c))
           (Steps
             (Step1 ($r1 $a $b) (STV (stv $s1 $c1)))
             (Step2 ($r2 $b $c) (STV (stv $s2 $c2)))))))))

;; 3-hop Causal Chain: A -> B -> C -> D
;; Example: PoorDrainage -> WaterloggedSoil -> RootRot -> Wilting
(= (chain-3-hop $space $r1 $a $b $r2 $c $r3 $d)
   (match $space (Relation $r1 $a $b (stv $s1 $c1))
     (match $space (Relation $r2 $b $c (stv $s2 $c2))
       (match $space (Relation $r3 $c $d (stv $s3 $c3))
         (let* (($tv12 (formula-deduction (stv $s1 $c1) (stv $s2 $c2)))
                ($tv123 (formula-deduction $tv12 (stv $s3 $c3))))
           (ChainProof
             (HopCount 3)
             (Start $a)
             (End $d)
             (STV $tv123)
             (Path ($a -> $b -> $c -> $d))
             (Steps
               (Step1 ($r1 $a $b) (STV (stv $s1 $c1)))
               (Step2 ($r2 $b $c) (STV (stv $s2 $c2)))
               (Step3 ($r3 $c $d) (STV (stv $s3 $c3))))))))))

;; 4-hop Causal Chain: A -> B -> C -> D -> E
;; Example: DenseCanopyShade -> HighHumidity -> CoffeeLeafRust -> OrangeLeafSpots -> CopperFungicide
(= (chain-4-hop $space $r1 $a $b $r2 $c $r3 $d $r4 $e)
   (match $space (Relation $r1 $a $b (stv $s1 $c1))
     (match $space (Relation $r2 $b $c (stv $s2 $c2))
       (match $space (Relation $r3 $c $d (stv $s3 $c3))
         (match $space (Relation $r4 $e $c (stv $s4 $c4))
           (let* (($tv12 (formula-deduction (stv $s1 $c1) (stv $s2 $c2)))
                  ($tv123 (formula-deduction $tv12 (stv $s3 $c3)))
                  ($tv_final (formula-deduction $tv123 (stv $s4 $c4))))
             (ChainProof
               (HopCount 4)
               (Start $a)
               (End $e)
               (STV $tv_final)
               (Path ($a -> $b -> $c -> $d -> $e))
               (Steps
                 (Step1 ($r1 $a $b) (STV (stv $s1 $c1)))
                 (Step2 ($r2 $b $c) (STV (stv $s2 $c2)))
                 (Step3 ($r3 $c $d) (STV (stv $s3 $c3)))
                 (Step4 ($r4 $e $c) (STV (stv $s4 $c4)))))))))))
