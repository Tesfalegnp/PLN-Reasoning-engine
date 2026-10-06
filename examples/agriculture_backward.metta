;; ====================================================================
;; Agricultural Backward Chaining Demonstration
;; Domain: Goal-Directed Diagnostic & Therapeutic Proof Search
;; Executed natively in MeTTa (Hyperon 0.2.10)
;; ====================================================================

!(import! &self metta:core:pln_tv)
!(import! &self metta:core:pln_formulas)
!(import! &self metta:chaining:nat)
!(import! &self metta:rules:agriculture_rules)
!(import! &self metta:kb:coffee_agriculture)
!(import! &self metta:chaining:bc)

! "=== AGRICULTURAL BACKWARD CHAINING ==="
! "Query Goal: Does CoffeePlant01 require CopperFungicideSpray?"
! "Searching backward for agronomic proof tree (depth = 2)..."

;; Run backward chaining query
!(bc (⊢ (RequiresTreatment CoffeePlant01 CopperFungicideSpray) $tv) (S (S Z)))
