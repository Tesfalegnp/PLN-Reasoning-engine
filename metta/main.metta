;; ====================================================================
;; Agricultural PLN Reasoning System — Master Entrypoint
;; Integrates PLN Core, Agricultural Rules, Chaining, and Knowledge Base
;; ====================================================================

!(import! &self metta:core:pln_tv)
!(import! &self metta:core:pln_formulas)
!(import! &self metta:chaining:nat)
!(import! &self metta:rules:agriculture_rules)
!(import! &self metta:chaining:bc)
!(import! &self metta:chaining:fc)
!(import! &self metta:kb:coffee_agriculture)

;; System verification indicator
! "Agricultural PLN Reasoning System successfully initialized."
