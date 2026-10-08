;; ============================================================
;; Test Case 2: PLN Deduction Operations
;; ============================================================

!(register-module! ../knowledge)
!(register-module! ../engine)

!(import! &self knowledge:agriculture)
!(import! &self engine:pln)

(= (fact-stv $fact)
    (match &self
        (: $id $fact (stv $s $c))
        (stv-value $s $c)))

!(println! "---- TEST 2: Simple Deduction (soil-dry × temperature-high) ----")
!(let $a (fact-stv (soil-dry))
    (let $b (fact-stv (temperature-high))
        (deduction $a $b)))

!(println! "---- TEST 3: Chained Deduction (with water-available) ----")
!(let $ab (let $a (fact-stv (soil-dry))
              (let $b (fact-stv (temperature-high))
                  (deduction $a $b)))
    (let $c (fact-stv (water-available))
        (deduction $ab $c)))

!(println! "---- TEST 4: Disease Deduction (orange-spots × humidity) ----")
!(let $a (fact-stv (coffee-leaves-have-orange-spots))
    (let $b (fact-stv (leaf-rust-favorable-humidity))
        (deduction $a $b)))
