
;; ====================================================================
;; Agricultural PLN Revision Demonstration
;; Domain: Conflicting Field Scout Evidence Resolution
;; Executed natively in MeTTa (Hyperon 0.2.10)
;; ====================================================================

!(import! &self metta:core:pln_tv)
!(import! &self metta:core:pln_formulas)

! "=== AGRICULTURAL CONFLICTING EVIDENCE REVISION ==="
! "Observation Source A (Agronomist Scout A): Rust pustules confirmed present"
! "  STV: (stv 0.85 0.75) -> High belief, solid confidence"
! "Observation Source B (Field Assistant B): Rust pustules unconfirmed/absent"
! "  STV: (stv 0.20 0.70) -> Low belief, moderate confidence"

! "Computing fused belief via PLN Truth_Revision formula..."
!(Truth_Revision (stv 0.85 0.75) (stv 0.20 0.70))
