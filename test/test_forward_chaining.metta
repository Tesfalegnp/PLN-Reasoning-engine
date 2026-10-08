;; ============================================================
;; Test Case 4: Forward Chaining Engine
;; ============================================================

!(register-module! ../knowledge)
!(register-module! ../engine)

!(import! &self knowledge:agriculture)
!(import! &self knowledge:rule)
!(import! &self engine:pln)
!(import! &self engine:forward_chain)

!(println! "---- TEST 6: Forward Chaining from (soil-dry) ----")
!(forward-query (soil-dry) &self (fromNumber 3))
