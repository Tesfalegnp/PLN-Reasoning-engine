;; ==============================================================================
;; Test Suite: Backward Chaining Inference
;; ==============================================================================

!(register-module! ../knowledge)
!(register-module! ../pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)
!(import! &self pln:abduction)
!(import! &self pln:revision)
!(import! &self pln:forward)
!(import! &self pln:backward)

;; Test 1: Backward Premise Search for Goal Disease
!(let (GoalPremiseTemplate (TargetDisease $dis) $susc $cond $sym $treat)
      (backward-find-premises &self CoffeeLeafRust)
   (assertEqual (== $dis CoffeeLeafRust) True))

;; Test 2: Goal Verification with Complete Supporting Evidence
!(let (BackwardProofTree (Goal $g) (GoalStatus $status) (GoalSTV (stv $s $c)) $verified $missing $path)
      (backward-verify-goal-complete &self Coffee CoffeeLeafRust HighHumidity OrangeLeafSpots)
   (assertEqual (and (== $status VerifiedSupported) (and (> $s 0.70) (> $c 0.70))) True))

;; Test 3: Goal Verification with Incomplete Evidence (Missing Condition)
!(let (BackwardProofTree (Goal $g) (GoalStatus $status) (GoalSTV (stv $s $c)) $verified $missing $interp $path)
      (backward-verify-goal-incomplete &self Coffee CoffeeLeafRust OrangeLeafSpots)
   (assertEqual (and (== $status PartiallySupportedIncompleteEvidence) (< $c 0.50)) True))

;; Test 4: Same Knowledge Base Invariant for Forward and Backward Chaining
!(let* (($fwd_tree (forward-infer-diagnosis &self Coffee HighHumidity OrangeLeafSpots))
        ($bwd_tree (backward-verify-goal-complete &self Coffee CoffeeLeafRust HighHumidity OrangeLeafSpots))
        ((ForwardDiagnosis $c1 (InferredDisease $d1) $ev1 (STV (stv $sf $cf)) $p1 $i1) $fwd_tree)
        ((BackwardProofTree (Goal $g2) (GoalStatus $s2) (GoalSTV (stv $sb $cb)) $v2 $m2 $p2) $bwd_tree))
   (assertEqual (and (== $d1 CoffeeLeafRust) (and (> $sf 0.70) (> $sb 0.70))) True))
