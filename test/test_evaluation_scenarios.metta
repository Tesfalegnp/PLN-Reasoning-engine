;; ============================================================
;; Evaluation Scenarios (PLN Assignment PDF Section 5)
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


;; ------------------------------------------------------------
;; SCENARIO 1: Evidence supports a direct conclusion
;; ------------------------------------------------------------
!(println! "==== SCENARIO 1: Evidence Supports Conclusion ====")
!(let $a (fact-stv (soil-dry))
    (let $b (fact-stv (temperature-high))
        (deduction $a $b)))


;; ------------------------------------------------------------
;; SCENARIO 2: Incomplete or uncertain evidence (Low confidence)
;; ------------------------------------------------------------
!(println! "==== SCENARIO 2: Incomplete / Uncertain Evidence ====")
!(let $uncertain-sensor (stv-value 0.60 0.35)
    (let $low-conf-rule (stv-value 0.70 0.40)
        (deduction $uncertain-sensor $low-conf-rule)))


;; ------------------------------------------------------------
;; SCENARIO 3: Multiple explanations (Abduction / Induction)
;; ------------------------------------------------------------
!(println! "==== SCENARIO 3: Multiple Explanations (Abduction) ====")
!(println! "Hypothesis A (Leaf Rust):")
!(let $obs (fact-stv (coffee-leaves-have-orange-spots))
    (let $env (fact-stv (leaf-rust-favorable-humidity))
        (abduction $obs $env)))

!(println! "Hypothesis B (Nutrient Deficiency):")
!(let $obs (fact-stv (coffee-leaves-wilting))
    (let $env (fact-stv (soil-dry))
        (induction $obs $env)))


;; ------------------------------------------------------------
;; SCENARIO 4: New or conflicting evidence (Revision)
;; ------------------------------------------------------------
!(println! "==== SCENARIO 4: Revision of Conflicting Beliefs ====")
!(println! "Field Sensor 1 (Soil Dry):")
!(fact-stv (soil-dry))
!(println! "Field Sensor 2 (Conflicting/New Reading):")
!(stv-value 0.40 0.85)
!(println! "Revised STV:")
!(revision (fact-stv (soil-dry)) (stv-value 0.40 0.85))


;; ------------------------------------------------------------
;; SCENARIO 5: Multi-step inference with confidence decay
;; ------------------------------------------------------------
!(println! "==== SCENARIO 5: Multi-Step Chaining Confidence Decay ====")
!(backward-query (irrigate-coffee-plant) &self (fromNumber 3))
