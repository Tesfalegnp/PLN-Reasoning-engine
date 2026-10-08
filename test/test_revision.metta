;; ============================================================
;; Test Case 3: PLN Revision Formula
;; ============================================================

!(register-module! ../knowledge)
!(register-module! ../engine)

!(import! &self engine:pln)

!(println! "---- TEST 5: PLN Revision Formula ----")
!(revision (stv-value 0.70 0.50) (stv-value 0.90 0.80))
