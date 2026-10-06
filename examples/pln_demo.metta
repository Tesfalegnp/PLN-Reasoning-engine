;; ====================================================================
;; Agricultural PLN Demonstration Script — All 4 Core Operations
;; Domain: Coffee Plant Pathology & Agronomic Reasoning
;; Executed natively in MeTTa (Hyperon 0.2.10)
;; ====================================================================

!(import! &self metta:core:pln_tv)
!(import! &self metta:core:pln_formulas)

! "=== 1. PLN DEDUCTION (COFFEE LEAF RUST TREATMENT) ==="
! "Premise 1: OrangeRustPustules -> CoffeeLeafRust (stv 0.90 0.85)"
! "Premise 2: CoffeeLeafRust -> CopperFungicideSpray (stv 0.80 0.75)"
! "Inferred: OrangeRustPustules -> CopperFungicideSpray"
!(Truth_Deduction (stv 0.90 0.85) (stv 0.80 0.75))

! "=== 2. PLN INDUCTION (VARIETAL SUSCEPTIBILITY GENERALIZATION) ==="
! "Premise 1: ArabicaBourbon -> SusceptibleToRust (stv 0.80 0.70)"
! "Premise 2: ArabicaBourbon -> PrematureBerryDrop (stv 0.85 0.75)"
! "Inferred: SusceptibleToRust -> PrematureBerryDrop"
!(Truth_Induction (stv 0.80 0.70) (stv 0.85 0.75))

! "=== 3. PLN ABDUCTION (DIFFERENTIAL DIAGNOSIS OF DEFOLIATION) ==="
! "Premise 1: CoffeeLeafRust -> PrematureLeafDrop (stv 0.85 0.75)"
! "Premise 2: NitrogenDeficiency -> PrematureLeafDrop (stv 0.80 0.70)"
! "Inferred Hypothesis: CoffeeLeafRust <-> NitrogenDeficiency overlap"
!(Truth_Abduction (stv 0.85 0.75) (stv 0.80 0.70))

! "=== 4. PLN REVISION (CONFLICTING FIELD SCOUT EVIDENCE) ==="
! "Evidence A (Field Scout A: Rust Pustules Present): (stv 0.85 0.75)"
! "Evidence B (Field Scout B: Rust Pustules Absent):  (stv 0.20 0.70)"
! "Fused Evidence State (Synthesized Belief via Evidence Pooling):"
!(Truth_Revision (stv 0.85 0.75) (stv 0.20 0.70))
