# Official Source Audit and Architecture Comparison Report

**Repository Under Audit**: `trueagi-io/hyperon-experimental`, `trueagi-io/chaining`, `trueagi-io/pln`  
**Auditor**: Antigravity MeTTa/PLN Engineering System  
**Date**: October 6, 2026  
**Status**: Rigorous Source Audit & Alignment Completed  

---

## 1. Executive Summary

This document presents a component-by-component audit comparing our MeTTa Probabilistic Logic Network (PLN) implementation against the authoritative TrueAGI repositories:
1. `trueagi-io/hyperon-experimental` (Language runtime, module system, evaluation engine)
2. `trueagi-io/chaining` (`experimental/backward-chaining`, `experimental/forward-chaining`, `experimental/common`)
3. `trueagi-io/pln` (`lib_pln.metta`, `examples/Smokes.metta`, `examples/FlyingRaven.metta`)

The purpose is to identify exact alignments, justified domain adaptations, and any simplified approximations, ensuring mathematical and semantic fidelity.

---

## 2. Comprehensive Component Comparison Table

| Component | Official TrueAGI Implementation | Our Project Implementation | Equivalent? | Difference & Rationale | Required Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Runtime Engine** | `hyperon` CPython wheel + Rust core (`0.2.10`) | `hyperon==0.2.10` running in isolated Python 3.12 (`.venv-metta`) | **Yes** | None. Exact official TrueAGI binary release used. | Verified via `hyperon.__version__`. |
| **Truth Value Representation** | `(STV s c)` where $s \in [0, 1]$ is probability and $c \in [0, 1)$ is confidence mode of beta distribution | `(stv s c)` where $s \in [0, 1]$ and $c \in [0, 1)$ | **Yes (Isomorphic)** | `lib_pln.metta` uses lowercase `(stv s c)`, while `chaining/TruthValue.metta` uses uppercase `(STV s c)`. Both wrap the same second-order probability pair $(s, c)$. | Retain canonical `(stv s c)` as in `lib_pln.metta` and support `(STV s c)`. |
| **Weight of Evidence** | $c = \frac{cnt}{cnt + k}$, $cnt = \frac{c \cdot k}{1 - c}$ with lookahead $k=1.0$ (Jeffreys prior mode) | `Truth_c2w` ($w = \frac{c}{1 - c}$) and `Truth_w2c` ($c = \frac{w}{w + 1}$) | **Yes** | Exact mathematical identity for lookahead $k=1.0$. | Validated across range $c \in [0, 0.9999]$. |
| **PLN Deduction (Full)** | 5-argument formula taking priors $P, Q, R$ and conditionals $P \to Q, Q \to R$ with consistency bounds: $s = PQs \cdot QRs + \frac{(1 - PQs)(Rs - Qs \cdot QRs)}{1 - Qs}$, $c = (PQs \cdot QRs)(PQc \cdot QRc)$ | Previously 2-argument simplified product ($s = s_1 s_2$). Updated to include both the full 5-argument formula from `lib_pln.metta` and operational 2-argument rule. | **Audited & Enhanced** | 5-argument formula requires global prior tracking. Chaining engines use 2-premise operational rules. Both are now provided. | Implemented full 5-arg formula and rigorous 2-arg deduction in `pln_formulas.metta`. |
| **PLN Modus Ponens** | `lib_pln.metta`: $s = Ps \cdot PQs + 0.02(1 - Ps)$, $c = (Ps \cdot PQs)(Pc \cdot PQc)$ | Previously assumed base rate 0. Updated to official base rate formula $s = s_P s_{imp} + 0.02(1 - s_P)$. | **Yes** | Official TrueAGI formula incorporates $P(Q \mid \neg P) = 0.02$ base rate to prevent underestimation when $P$ has non-zero uncertainty. | Updated `Truth_ModusPonens` in `pln_formulas.metta`. |
| **PLN Revision** | Pools independent evidence: $w_{total} = w_1 + w_2$, $s = \frac{s_1 w_1 + s_2 w_2}{w_{total}}$, $c = \frac{w_{total}}{w_{total} + 1}$ | Exact implementation: `Truth_Revision` using `Truth_c2w` and `Truth_w2c`. | **Yes** | Mathematically identical to `lib_pln.metta`. | Verified with test cases including conflicting evidence. |
| **PLN Induction & Abduction** | Appendix A PLN formulas in `lib_pln.metta` taking 5 arguments $(sA, sB, sC, sBA, sBC)$. | Provided both full 5-argument formula and operational 2-argument rules with confidence derived via `Truth_w2c`. | **Yes** | Exact adherence to `lib_pln.metta`. | Implemented in `pln_formulas.metta`. |
| **Depth Bounding** | Peano arithmetic: `(: Nat Type)`, `Z`, `(S $k)`, `fromNumber`, `fromNat` | Exact implementation: `metta/chaining/nat.metta`. | **Yes** | Identical to `chaining/experimental/common/Num.metta`. | Verified recursion termination on cyclic rules. |
| **Backward Chaining Engine** | `bc-xp.metta`: Unifies goal against rule head, recursively proves premises, builds proof structure. | `bc.metta`: Unifies goal against rule base, recursively solves subgoals, synthesizes structured `(Proof (⊢ concl tv) (Rule ...))` tree. | **Yes** | Added explicit `Proof` tree emission for explanation/DAG rendering in Streamlit. | Verified on 1-step, multi-step, missing, cyclic, and conflicting goals. |
| **Forward Chaining Engine** | `fc-xp.metta`: Step-bounded derivation matching premise against rule base, generating new facts. | `fc.metta`: Step-bounded derivation matching premise against rule base, generating `(Derivation (⊢ concl tv) ...)`. | **Yes** | Added premise preservation and structured derivation trace. | Verified on single-step, multi-step, and agriculture disease derivation. |
| **Rule Base Representation** | `(⊢ premise1 premise2 conclusion)` or curried rules | Declarative `(rule id premise1 premise2 concl)` generator `(rb)` | **Equivalent** | Using an explicit rule identifier allows the backward chainer to label each proof step (`ded`, `mp`, `sim_sym`, `and_intro`). | Clean declarative interface preserved. |
| **Domain Knowledge Base** | Synthetic examples (`Smokes.metta`, `FlyingRaven.metta`) | Realistic **Coffee Agriculture Disease Reasoning** (`coffee_agriculture.metta`) | **Domain Adaptation** | Custom agricultural domain requested by user, modeled with botanical precision (Coffee Leaf Rust, Berry Disease, Nutrient Deficiency). | Compatible with both FC and BC simultaneously. |
| **Python Integration** | `from hyperon import MeTTa` | `PLNRunner` wrapping `hyperon.MeTTa` with `Environment.custom_env` | **Yes** | Python strictly manages lifecycle and parses ASTs; zero semantic reasoning is performed in Python. | Verified architecture boundary. |

---

## 3. Mathematical Audit of PLN Formulas

### 3.1 Simple Truth Value Representation
In PLN:
- A truth value is a pair $(s, c)$, denoted `(stv s c)`.
- $s \in [0, 1]$ represents the mean/mode probability.
- $c \in [0, 1)$ represents confidence. $c = 1.0$ represents infinite evidence ($w \to \infty$), which is impossible for empirical observations. In our implementation, $c$ is strictly bounded by $0.999999$ during weight calculations to avoid division by zero.

### 3.2 Deduction Formula Audit
In `trueagi-io/pln/lib_pln.metta`:
```metta
(= (Truth_Deduction_Full (stv $Ps $Pc) (stv $Qs $Qc) (stv $Rs $Rc) (stv $PQs $PQc) (stv $QRs $QRc))
   (if (and (conditional-probability-consistency $Ps $Qs $PQs)
            (conditional-probability-consistency $Qs $Rs $QRs))
       (stv (if (< 0.9999 $Qs)
                $Rs
                (+ (* $PQs $QRs) (/safe (* (- 1 $PQs) (- $Rs (* $Qs $QRs))) (- 1 $Qs))))
            (* (* $PQs $QRs) (* $PQc $QRc)))
       (stv 1 0)))
```
When marginal probabilities $P, Q, R$ are assumed uniform or unconditioned, the second term vanishes when $P \to Q$ is high, leading to the classical operational chaining approximation $s \approx s_{PQ} \cdot s_{QR}$.
**Resolution**: We provide both:
1. `Truth_Deduction_Full`: The full 5-argument formula directly from `lib_pln.metta`.
2. `Truth_Deduction`: The operational 2-argument chaining formula with confidence propagation $c = (s_1 s_2)(c_1 c_2)$.

### 3.3 Modus Ponens Formula Audit
In `trueagi-io/pln/lib_pln.metta`:
```metta
(= (Truth_ModusPonens (stv $Ps $Pc) (stv $PQs $PQc))
   (stv (+ (* $Ps $PQs) (* 0.02 (- 1 $Ps)))
        (* (* $Ps $PQs) (* $Pc $PQc))))
```
The term $0.02 \cdot (1 - P_s)$ reflects the background probability $P(Q \mid \neg P) = 0.02$.
**Resolution**: Updated `pln_formulas.metta` to include this official $0.02$ base rate factor.

### 3.4 Revision Formula Audit
In `trueagi-io/pln/lib_pln.metta`:
$$w_1 = \frac{c_1}{1 - c_1}, \quad w_2 = \frac{c_2}{1 - c_2}, \quad w = w_1 + w_2$$
$$s = \frac{s_1 w_1 + s_2 w_2}{w}, \quad c = \frac{w}{w + 1}$$
**Resolution**: Our implementation was already mathematically exact and is verified.

---

## 4. Key Findings and Actions Completed

1. **PLN Formulas**: Added full 5-argument formulas (`Truth_Deduction_Full`, `Truth_Induction_Full`, `Truth_Abduction_Full`) to `metta/core/pln_formulas.metta` while refining 2-argument operational formulas with official base-rates.
2. **Domain Knowledge Base**: Built `metta/kb/coffee_agriculture.metta` with realistic plant pathology (Coffee Leaf Rust, Coffee Berry Disease, Nitrogen Chlorosis, environmental triggers, and fungicide/cultural treatments).
3. **Unification of KB**: Verified that the SAME `coffee_agriculture.metta` knowledge base functions identically for both Backward Chaining and Forward Chaining.
4. **Conflicting Evidence**: Implemented and verified conflict resolution using PLN Revision.
5. **Architectural Guardrails**: Confirmed Python layer is strictly an execution bridge; all reasoning logic executes natively in MeTTa.
