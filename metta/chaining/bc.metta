;; ====================================================================
;; PLN Backward Chainer with Proof Tree Generation
;; ====================================================================

;; Rule truth function dispatchers
(= (Truth_Apply_Rule2 ded $tv1 $tv2) (Truth_Deduction $tv1 $tv2))
(= (Truth_Apply_Rule2 mp $tv1 $tv2) (Truth_ModusPonens $tv1 $tv2))
(= (Truth_Apply_Rule2 and_intro $tv1 $tv2) (Truth_Intersection $tv1 $tv2))

(= (Truth_Apply_Rule1 sim_sym $tv1) $tv1)
(= (Truth_Apply_Rule1 not_intro $tv1) (Truth_Negation $tv1))

;; --------------------------------------------------------------------
;; Backward Chainer: returns (Proof (⊢ $concl $tv) $proofTree)
;; --------------------------------------------------------------------

;; 1. Base Case: Direct match in Knowledge Base at any search depth
(= (bc (⊢ $concl $tv) $depth)
   (let (⊢ $concl $tv) (kb)
     (Proof (⊢ $concl $tv) (Fact $concl))))

;; 2. Recursive Step: Modus Ponens (Targeted Implication-First Ordering)
;; For goal $q: match (→ $p $q) first to instantiate $p, then solve subgoal $p
(= (bc (⊢ $concl $tv) (S $k))
   (let* (((rule mp $p (→ $p $concl) $concl) (rb))
          ((Proof (⊢ (→ $p $concl) $tvImp) $subImp) (bc (⊢ (→ $p $concl) $tvImp) $k))
          ((Proof (⊢ $p $tvP) $subP) (bc (⊢ $p $tvP) $k))
          ($tv (Truth_Apply_Rule2 mp $tvP $tvImp)))
     (Proof (⊢ $concl $tv) (Rule mp $subP $subImp))))

;; 3. Recursive Step: Deduction (Inheritance Transitivity)
(= (bc (⊢ (Inheritance $x $z) $tv) (S $k))
   (let* (((rule ded (Inheritance $x $y) (Inheritance $y $z) (Inheritance $x $z)) (rb))
          ((Proof (⊢ (Inheritance $x $y) $tv1) $sub1) (bc (⊢ (Inheritance $x $y) $tv1) $k))
          ((Proof (⊢ (Inheritance $y $z) $tv2) $sub2) (bc (⊢ (Inheritance $y $z) $tv2) $k))
          ($tv (Truth_Apply_Rule2 ded $tv1 $tv2)))
     (Proof (⊢ (Inheritance $x $z) $tv) (Rule ded $sub1 $sub2))))

;; 4. Recursive Step: Deduction (Implication Transitivity)
(= (bc (⊢ (→ $x $z) $tv) (S $k))
   (let* (((rule ded (→ $x $y) (→ $y $z) (→ $x $z)) (rb))
          ((Proof (⊢ (→ $x $y) $tv1) $sub1) (bc (⊢ (→ $x $y) $tv1) $k))
          ((Proof (⊢ (→ $y $z) $tv2) $sub2) (bc (⊢ (→ $y $z) $tv2) $k))
          ($tv (Truth_Apply_Rule2 ded $tv1 $tv2)))
     (Proof (⊢ (→ $x $z) $tv) (Rule ded $sub1 $sub2))))

;; 5. Recursive Step: Unary Rules (from rb1 generator)
(= (bc (⊢ $concl $tv) (S $k))
   (let* (((rule1 $ruleName $p1 $concl) (rb1))
          ((Proof (⊢ $p1 $tv1) $sub1) (bc (⊢ $p1 $tv1) $k))
          ($tv (Truth_Apply_Rule1 $ruleName $tv1)))
     (Proof (⊢ $concl $tv) (Rule $ruleName $sub1))))
