;; ============================================================
;; Test Case 1: Fact & STV Lookup
;; ============================================================

!(register-module! ../knowledge)
!(register-module! ../engine)

!(import! &self knowledge:agriculture)

(= (fact-stv $fact)
    (match &self
        (: $id $fact (stv $s $c))
        (stv-value $s $c)))

!(println! "---- TEST 1: Fact STV Lookup ----")
!(fact-stv (soil-dry))
!(fact-stv (temperature-high))
!(fact-stv (water-available))
