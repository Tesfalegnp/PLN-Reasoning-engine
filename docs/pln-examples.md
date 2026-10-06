# Probabilistic Logic Network (PLN) Operations & Execution Guide

This document specifies the four core PLN operations required by the project:
1. **Deduction**
2. **Induction**
3. **Abduction**
4. **Revision**

Every example in this document contains **actual verified execution outputs** from the official TrueAGI Hyperon `0.2.10` runtime produced by running:
```bash
.venv-metta/bin/metta examples/pln_demo.metta
```

---

## 1. Standalone Demo Script Execution Output

Running the standalone demonstration script:
```bash
$ .venv-metta/bin/metta examples/pln_demo.metta
```
Yields the exact MeTTa evaluation stream:
```lisp
["=== 1. PLN DEDUCTION ==="]
["Premise 1: OrangeRustPustules -> CoffeeLeafRust (stv 0.90 0.85)"]
["Premise 2: CoffeeLeafRust -> CopperFungicideSpray (stv 0.80 0.75)"]
["Inferred: OrangeRustPustules -> CopperFungicideSpray"]
[(stv 0.7200000000000001 0.459)]

["=== 2. PLN INDUCTION ==="]
["Premise 1: ArabicaBourbon -> SusceptibleToRust (stv 0.80 0.70)"]
["Premise 2: ArabicaBourbon -> PrematureBerryDrop (stv 0.85 0.75)"]
["Inferred: SusceptibleToRust -> PrematureBerryDrop"]
[(stv 0.68 0.30855661192739836)]

["=== 3. PLN ABDUCTION ==="]
["Premise 1: CoffeeLeafRust -> Defoliation (stv 0.85 0.75)"]
["Premise 2: NitrogenDeficiency -> Defoliation (stv 0.80 0.70)"]
["Inferred: CoffeeLeafRust -> NitrogenDeficiency"]
[(stv 0.68 0.30855661192739836)]

["=== 4. PLN REVISION (CONFLICTING EVIDENCE) ==="]
["Evidence A (Scout A: Rust Symptoms Present): (stv 0.85 0.75)"]
["Evidence B (Scout B: Rust Symptoms Absent):  (stv 0.20 0.70)"]
["Fused Evidence State:"]
[(stv 0.565625 0.8421052631578947)]
```

---

## 2. Operation 1: PLN Deduction

### Conceptual Overview
Deduction infers a transitive connection between propositions:
$$\text{Given: } P \to Q \ (\text{stv } s_1\ c_1) \quad \text{and} \quad Q \to R \ (\text{stv } s_2\ c_2)$$
$$\text{Infer: } P \to R \ (\text{stv } s\ c)$$

### Mathematical Formulation
1. **Operational Chaining Formula** (when intermediate priors are unconditioned):
   $$s = s_1 \cdot s_2, \quad c = (s_1 \cdot s_2) \cdot (c_1 \cdot c_2)$$
2. **Full Second-Order Probability Formula** (`lib_pln.metta` page 74):
   $$s = (PQs \cdot QRs) + \frac{(1 - PQs)(Rs - Qs \cdot QRs)}{1 - Qs}, \quad c = (PQs \cdot QRs) \cdot (PQc \cdot QRc)$$
   guarded by conditional probability consistency:
   $$\frac{\max(0, Ps + Qs - 1)}{Ps} \le PQs \le \frac{Qs}{Ps}$$

### MeTTa Execution
```metta
!(Truth_Deduction (stv 0.90 0.85) (stv 0.80 0.75))
```

### Actual Hyperon 0.2.10 Output
```lisp
[(stv 0.7200000000000001 0.459)]
```

### Agronomic Interpretation
- Premise 1: "If CoffeePlant has OrangeRustPustules, it is AfflictedWith CoffeeLeafRust" ($s=0.90, c=0.85$).
- Premise 2: "If CoffeePlant is AfflictedWith CoffeeLeafRust, it RequiresTreatment CopperFungicideSpray" ($s=0.80, c=0.75$).
- Derived: "If CoffeePlant has OrangeRustPustules, it RequiresTreatment CopperFungicideSpray" ($s=0.7200, c=0.4590$).
- Notice that uncertainty compounds: confidence drops from $0.85$ and $0.75$ down to $0.4590$ across the transitive link.

---

## 3. Operation 2: PLN Induction

### Conceptual Overview
Induction generalizes a connection between two predicates $A$ and $C$ that share a common subject $B$:
$$\text{Given: } B \to A \ (\text{stv } s_{BA}\ c_{BA}) \quad \text{and} \quad B \to C \ (\text{stv } s_{BC}\ c_{BC})$$
$$\text{Infer: } A \to C \ (\text{stv } s\ c)$$

### Mathematical Formulation
From `lib_pln.metta` (PLN book Appendix A):
$$s = s_{BA} \cdot s_{BC}$$
$$w = s_{BC} \cdot c_{BC} \cdot c_{BA}, \quad c = \text{Truth\_w2c}(w) = \frac{w}{w + 1}$$

### MeTTa Execution
```metta
!(Truth_Induction (stv 0.80 0.70) (stv 0.85 0.75))
```

### Actual Hyperon 0.2.10 Output
```lisp
[(stv 0.68 0.30855661192739836)]
```

### Agronomic Interpretation
- Premise 1: "ArabicaBourbon plants exhibit HighRustSusceptibility" ($s=0.80, c=0.70$).
- Premise 2: "ArabicaBourbon plants exhibit PrematureBerryDrop under heavy rain" ($s=0.85, c=0.75$).
- Inferred: "Plants with HighRustSusceptibility also exhibit PrematureBerryDrop" ($s=0.6800, c=0.3086$).
- The confidence is lower ($c=0.3086$) because induction is an inherently speculative hypothesis-generating rule.

---

## 4. Operation 3: PLN Abduction

### Conceptual Overview
Abduction reasons backwards from an observed effect $B$ to a common plausible explanation:
$$\text{Given: } A \to B \ (\text{stv } s_{AB}\ c_{AB}) \quad \text{and} \quad C \to B \ (\text{stv } s_{CB}\ c_{CB})$$
$$\text{Infer: } A \to C \ (\text{stv } s\ c)$$

### Mathematical Formulation
From `lib_pln.metta` (PLN book Appendix A):
$$s = s_{AB} \cdot s_{CB}$$
$$w = s_{AB} \cdot c_{AB} \cdot c_{CB}, \quad c = \text{Truth\_w2c}(w) = \frac{w}{w + 1}$$

### MeTTa Execution
```metta
!(Truth_Abduction (stv 0.85 0.75) (stv 0.80 0.70))
```

### Actual Hyperon 0.2.10 Output
```lisp
[(stv 0.68 0.30855661192739836)]
```

### Agronomic Interpretation
- Premise 1: "Severe Leaf Rust causes CanopyDefoliation" ($s=0.85, c=0.75$).
- Premise 2: "Extreme Nitrogen Deficiency causes CanopyDefoliation" ($s=0.80, c=0.70$).
- Inferred: "CanopyDefoliation allows abducing that Nitrogen Deficiency correlates with Leaf Rust vulnerability" ($s=0.6800, c=0.3086$).

---

## 5. Operation 4: PLN Revision (Conflicting Evidence)

### Conceptual Overview
Revision combines two independent lines of evidence for the **exact same statement**:
$$\text{Given: } H \ (\text{stv } s_1\ c_1) \quad \text{and} \quad H \ (\text{stv } s_2\ c_2)$$
$$\text{Infer: } H \ (\text{stv } s_{rev}\ c_{rev})$$

### Mathematical Formulation
From `lib_pln.metta`:
$$w_1 = \frac{c_1}{1 - c_1}, \quad w_2 = \frac{c_2}{1 - c_2}, \quad w_{total} = w_1 + w_2$$
$$s_{rev} = \frac{s_1 w_1 + s_2 w_2}{w_{total}}, \quad c_{rev} = \frac{w_{total}}{w_{total} + 1}$$

### MeTTa Execution (Conflicting Evidence Scenario)
```metta
;; Field Scout A: Observed distinct orange pustules on lower leaves
;; Field Scout B: Inspected upper canopy, reported leaves mostly healthy
!(Truth_Revision (stv 0.85 0.75) (stv 0.20 0.70))
```

### Actual Hyperon 0.2.10 Output
```lisp
[(stv 0.565625 0.8421052631578947)]
```

### Agronomic Interpretation
1. **Weight of Evidence**:
   - Scout A: $w_1 = \frac{0.75}{1 - 0.75} = 3.0$
   - Scout B: $w_2 = \frac{0.70}{1 - 0.70} = 2.3333$
   - Total accumulated evidence weight: $w_{total} = 5.3333$
2. **Strength Balance**:
   - $s_{rev} = \frac{0.85 \times 3.0 + 0.20 \times 2.3333}{5.3333} = 0.5656$
   - The contradictory reports pull the probability into the ambiguous mid-range ($56.56\%$).
3. **Confidence Elevation**:
   - $c_{rev} = \frac{5.3333}{5.3333 + 1} = 0.8421$
   - Although the scouts disagree, our certainty about the *amount of information collected* has increased! Confidence $0.8421$ strictly exceeds both individual confidences ($0.75$ and $0.70$).
   - The system does NOT blindly overwrite facts; it weights and fuses them mathematically.
