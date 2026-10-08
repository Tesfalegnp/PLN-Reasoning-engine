;; ============================================================
;; Agricultural PLN Reasoning Engine — Test Suite
;; MeTTa 0.2.10
;; ============================================================
;;
;; This test imports the real source files and verifies that
;; all PLN operations, forward chaining, and backward chaining
;; work correctly.
;; ============================================================


;; ------------------------------------------------------------
;; IMPORT SOURCE FILES
;; ------------------------------------------------------------

!(register-module! ../knowledge)
!(register-module! ../engine)

!(import! &self knowledge:agriculture)
!(import! &self knowledge:rule)
!(import! &self engine:pln)
!(import! &self engine:forward_chain)
!(import! &self engine:backward_chain)


;; ------------------------------------------------------------
;; HELPER — fact-stv must be defined here because match &self
;; must target the test's own space where facts were imported.
;; ------------------------------------------------------------

(= (fact-stv $fact)
    (match &self
        (: $id $fact (stv $s $c))
        (stv-value $s $c)))


;; ============================================================
;;                       T E S T S
;; ============================================================


;; ---- TEST 1: fact-stv lookup ---------------------------------
!(println! "---- TEST 1: fact-stv lookup ----")
!(fact-stv (soil-dry))


;; ---- TEST 2: deduction (soil-dry × temperature-high) ---------
!(println! "---- TEST 2: deduction ----")
!(let $a (fact-stv (soil-dry))
    (let $b (fact-stv (temperature-high))
        (deduction $a $b)))


;; ---- TEST 3: chained deduction -------------------------------
!(println! "---- TEST 3: chained deduction ----")
!(let $ab (let $a (fact-stv (soil-dry))
              (let $b (fact-stv (temperature-high))
                  (deduction $a $b)))
    (let $c (fact-stv (water-available))
        (deduction $ab $c)))


;; ---- TEST 4: disease deduction -------------------------------
!(println! "---- TEST 4: disease deduction ----")
!(let $a (fact-stv (coffee-leaves-have-orange-spots))
    (let $b (fact-stv (leaf-rust-favorable-humidity))
        (deduction $a $b)))


;; ---- TEST 5: revision ----------------------------------------
!(println! "---- TEST 5: revision ----")
!(revision (stv-value 0.70 0.50) (stv-value 0.90 0.80))


;; ---- TEST 6: forward chaining from soil-dry -------------------
!(println! "---- TEST 6: forward chaining from soil-dry ----")
!(forward-query (soil-dry) &self (fromNumber 3))


;; ---- TEST 7: backward chaining to irrigate-coffee-plant -------
!(println! "---- TEST 7: backward chaining to irrigate-coffee-plant ----")
!(backward-query (irrigate-coffee-plant) &self (fromNumber 3))


;; ---- TEST 8: full scenario ------------------------------------
!(println! "---- TEST 8: full scenario ----")

!(println! "  Step 1: soil-dry × temperature-high")
!(let $a (fact-stv (soil-dry))
    (let $b (fact-stv (temperature-high))
        (deduction $a $b)))

!(println! "  Step 2: chained with water-available")
!(let $ab (let $a (fact-stv (soil-dry))
              (let $b (fact-stv (temperature-high))
                  (deduction $a $b)))
    (let $c (fact-stv (water-available))
        (deduction $ab $c)))

!(println! "  Step 3: backward proof for irrigate-coffee-plant")
!(backward-query (irrigate-coffee-plant) &self (fromNumber 3))