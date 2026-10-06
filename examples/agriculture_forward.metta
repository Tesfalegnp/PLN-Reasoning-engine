;; ====================================================================
;; Agricultural Forward Chaining Demonstration
;; Domain: Coffee Plant Disease Progression & Treatment Derivation
;; Executed natively in MeTTa (Hyperon 0.2.10)
;; ====================================================================

!(import! &self metta:core:pln_tv)
!(import! &self metta:core:pln_formulas)
!(import! &self metta:chaining:nat)
!(import! &self metta:rules:agriculture_rules)
!(import! &self metta:kb:coffee_agriculture)
!(import! &self metta:chaining:fc)

! "=== AGRICULTURAL FORWARD CHAINING ==="
! "Initial Seed Observation: CoffeePlant01 has OrangeRustPustules"
! "Propagating forward across agricultural rules for 2 steps (depth = 2)..."

;; Run 2-step forward chaining
!(fc (⊢ (HasSymptom CoffeePlant01 OrangeRustPustules) (stv 0.88 0.85)) (S (S Z)))
