;; ==============================================================================
;; Test Suite: Multi-Step Chaining
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)
!(import! &self pln:chaining)

;; Test 1: 2-Hop Causal Chain
;; PoorDrainage -> WaterloggedSoil -> RootRot
!(let (ChainProof (HopCount 2) (Start PoorDrainage) (End RootRot) (STV (stv $s $c)) $path $steps)
      (chain-2-hop &self promotes PoorDrainage WaterloggedSoil increases-risk RootRot)
   (assertEqual (and (> $s 0.75) (> $c 0.55)) True))

;; Test 2: 3-Hop Causal Chain (Scenario 5)
;; PoorDrainage -> WaterloggedSoil -> RootRot -> Wilting
!(let (ChainProof (HopCount 3) (Start PoorDrainage) (End Wilting) (STV (stv $s $c)) $path $steps)
      (chain-3-hop &self promotes PoorDrainage WaterloggedSoil increases-risk RootRot causes Wilting)
   (assertEqual (and (> $s 0.65) (> $c 0.40)) True))

;; Test 3: Progressive Uncertainty Propagation across Hops
!(let* (($p2 (chain-2-hop &self promotes PoorDrainage WaterloggedSoil increases-risk RootRot))
        ((ChainProof $h2 $s2 $e2 (STV (stv $str2 $c2)) $pa2 $st2) $p2)
        ($p3 (chain-3-hop &self promotes PoorDrainage WaterloggedSoil increases-risk RootRot causes Wilting))
        ((ChainProof $h3 $s3 $e3 (STV (stv $str3 $c3)) $pa3 $st3) $p3))
   (assertEqual (< $c3 $c2) True))
