;; ============================================================
;; Test Case 5: Backward Chaining Proof Engine
;; ============================================================

!(register-module! ../knowledge)
!(register-module! ../engine)

!(import! &self knowledge:agriculture)
!(import! &self knowledge:rule)
!(import! &self engine:pln)
!(import! &self engine:backward_chain)

!(println! "---- TEST 7: Backward Chaining to (irrigate-coffee-plant) ----")
!(backward-query (irrigate-coffee-plant) &self (fromNumber 3))
