;; ============================================================
;; Test Case 6: Full Agricultural Scenario Integration
;; ============================================================

!(register-module! ../knowledge)
!(register-module! ../engine)

!(import! &self knowledge:agriculture)
!(import! &self knowledge:rule)
!(import! &self engine:pln)
!(import! &self engine:forward_chain)
!(import! &self engine:backward_chain)

(= (fact-stv $fact)
    (match &self
        (: $id $fact (stv $s $c))
        (stv-value $s $c)))

!(println! "---- TEST 8: Full Agricultural Scenario ----")

!(println! "  Step 1: Deduction (soil-dry × temperature-high)")
!(let $a (fact-stv (soil-dry))
    (let $b (fact-stv (temperature-high))
        (deduction $a $b)))

!(println! "  Step 2: Chained Deduction (with water-available)")
!(let $ab (let $a (fact-stv (soil-dry))
              (let $b (fact-stv (temperature-high))
                  (deduction $a $b)))
    (let $c (fact-stv (water-available))
        (deduction $ab $c)))

!(println! "  Step 3: Backward Proof for (irrigate-coffee-plant)")
!(backward-query (irrigate-coffee-plant) &self (fromNumber 3))
