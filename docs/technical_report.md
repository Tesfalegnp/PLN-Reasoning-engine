# Comprehensive Technical Report: Agricultural Probabilistic Logic Network (PLN) Reasoning Engine in MeTTa

---

## Executive Summary

This project implements a domain-specific **Probabilistic Logic Network (PLN)** reasoning engine natively in **MeTTa 0.2.10** for precision agriculture. Real-world agricultural decision-making operates under radical uncertainty—ambient weather conditions fluctuate, sensor measurements are noisy, and crop disease symptoms overlap. Classical binary logic engines fail in these environments because they cannot quantify evidence weight or aggregate conflicting information.

Our engine solves this problem by combining formal logic rules with evidential probability theory. The system incorporates:
1. **Subjective Truth Values (STVs)** representing both Strength ($s$) and Confidence ($c$).
2. **Four PLN Calculus Operations**: Deduction, Induction, Abduction, and Revision.
3. **Bidirectional Search Engines**: Data-driven Forward Chaining and Goal-driven Backward Chaining proof tree generation.
4. **Interactive Streamlit Dashboard**: A Python-driven interactive visualization interface.
5. **Rigorous Scenario Evaluation**: Verification across 5 realistic domain scenarios.

---

## 1. Domain Selection & Problem Definition

### 1.1 Why Agriculture?
Agriculture presents a classic domain of **imperfect information**:
- **Soil Moisture & Microclimate Sensors**: Prone to calibration drift or transient interference.
- **Visual Symptoms**: Leaf spots or wilting can stem from water stress, nutrient deficiency, or fungal pathogens (e.g., Coffee Leaf Rust).
- **Intervention Risks**: Irrigating when water is unavailable or applying pesticides unnecessarily incurs financial and environmental costs.

### 1.2 System Objective
The primary objective of this engine is to ingest real-world observations, apply multi-hop probabilistic rule chains, and output actionable farming decisions (e.g., `(irrigate-coffee-plant)`) attached to calculated, rigorous truth values $\langle s, c \rangle$.

---

## 2. Project Architecture & Directory Structure

The repository is organized into modular directories separating core logic, domain knowledge, test suites, documentation, and user interfaces:

```
pln-engine/
├── docs/
│   └── technical_report.md      # Comprehensive technical documentation & report
├── engine/
│   ├── pln.metta                # Core PLN truth-value operations & formulas
│   ├── forward_chain.metta      # Data-driven forward chaining engine
│   └── backward_chain.metta     # Goal-driven backward chaining & proof tree engine
├── knowledge/
│   ├── agriculture.metta        # Domain facts with STVs
│   └── rule.metta               # Agricultural inference rules
├── test/
│   ├── test_fact_stv.metta      # Fact & STV lookup tests
│   ├── test_deduction.metta     # Deduction & rule-chaining tests
│   ├── test_revision.metta      # Revision formula tests
│   ├── test_forward_chaining.metta  # Forward chaining tests
│   ├── test_backward_chaining.metta # Backward chaining proof tests
│   ├── test_full_scenario.metta     # Full scenario integration tests
│   ├── test_evaluation_scenarios.metta # 5 PDF evaluation scenarios
│   └── test_agriculture.metta   # Master test suite
├── app.py                       # Interactive Desktop GUI Dashboard
├── README.md                    # System instructions & quick start guide
└── test_case.txt                # Sample query definitions
```

---

## 3. Knowledge Base Construction & STV Representation

### 3.1 Subjective Truth Values (STV)
In PLN, every logical atom or rule is assigned a **Simple Truth Value**:
$$\text{STV} = (\text{stv } s \;\; c)$$

- **Strength ($s \in [0.0, 1.0]$)**: The estimated probability or degree of truth of the statement.
- **Confidence ($c \in [0.0, 1.0]$)**: The weight of evidence backing the estimate, where $c \rightarrow 1.0$ indicates absolute certainty.

### 3.2 Domain Knowledge Base ([`knowledge/agriculture.metta`](file:///home/hope/project_2/pln-engine/knowledge/agriculture.metta))
Facts are structured into logical groups:

#### Weather & Environmental Facts
```metta
(: F1 (soil-dry)          (stv 0.90 0.90))
(: F2 (temperature-high)  (stv 0.85 0.88))
(: F3 (rainfall-low)      (stv 0.80 0.82))
```

#### Crop Condition Observations
```metta
(: F4 (coffee-plant-water-stressed) (stv 0.70 0.65))
(: F5 (coffee-leaves-wilting)       (stv 0.75 0.70))
```

#### Resource Availability & Diagnostics
```metta
(: F6 (water-available)                 (stv 0.95 0.90))
(: F7 (farmer-can-irrigate)             (stv 0.90 0.85))
(: F8 (coffee-leaves-have-orange-spots) (stv 0.88 0.80))
(: F9 (leaf-rust-favorable-humidity)    (stv 0.78 0.72))
```

### 3.3 Domain Inference Rules ([`knowledge/rule.metta`](file:///home/hope/project_2/pln-engine/knowledge/rule.metta))
Rules capture causal connections between environment, stress, and management actions:

```metta
(: R1 (implication (and (soil-dry) (temperature-high)) (coffee-plant-water-stressed)) (stv 0.92 0.85))
(: R2 (implication (and (coffee-plant-water-stressed) (water-available)) (irrigation-recommended)) (stv 0.90 0.82))
(: R3 (implication (and (irrigation-recommended) (farmer-can-irrigate)) (irrigate-coffee-plant)) (stv 0.95 0.88))
(: R4 (implication (and (coffee-leaves-have-orange-spots) (leaf-rust-favorable-humidity)) (coffee-leaf-rust-suspected)) (stv 0.85 0.78))
```

---

## 4. Core PLN Calculus Implementation ([`engine/pln.metta`](file:///home/hope/project_2/pln-engine/engine/pln.metta))

The engine implements four fundamental mathematical operations of PLN calculus:

### 4.1 Deduction
Used to combine rule premises and step through causal chains:
$$\text{deduction}\Big(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle\Big) = \langle s_1 \cdot s_2, \;\; c_1 \cdot c_2 \rangle$$

```metta
(= (deduction (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value (* $s1 $s2) (* $c1 $c2)))
```

### 4.2 Induction
Generalizes shared properties or overlapping evidence across observations:
$$\text{induction}\Big(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle\Big) = \left\langle \frac{s_1 + s_2}{2}, \;\; c_1 \cdot c_2 \right\rangle$$

```metta
(= (induction (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value (/ (+ $s1 $s2) 2) (* $c1 $c2)))
```

### 4.3 Abduction
Infers plausible underlying causes given observed symptoms:
$$\text{abduction}\Big(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle\Big) = \langle s_1 \cdot s_2, \;\; c_1 \cdot c_2 \rangle$$

```metta
(= (abduction (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value (* $s1 $s2) (* $c1 $c2)))
```

### 4.4 Revision
Aggregates independent or conflicting streams of evidence (e.g. merging two separate soil sensors):
$$\text{revision}\Big(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle\Big) = \left\langle \frac{s_1 c_1 + s_2 c_2}{c_1 + c_2}, \;\; \frac{c_1 + c_2}{2} \right\rangle$$

```metta
(= (revision (stv-value $s1 $c1) (stv-value $s2 $c2))
    (stv-value
        (/ (+ (* $s1 $c1) (* $s2 $c2))
           (+ $c1 $c2))
        (/ (+ $c1 $c2) 2)))
```

---

## 5. Bidirectional Chaining Engines

### 5.1 Forward Chaining (Data-Driven Search)
Defined in [`engine/forward_chain.metta`](file:///home/hope/project_2/pln-engine/engine/forward_chain.metta).

* **Mechanism**: Starts from active facts/observations (e.g. `(soil-dry)`), searches matching rules in the Knowledge Base, applies PLN deduction to calculate the derived truth value, and expands derived conclusions forward.
* **Query Execution**:
  ```metta
  !(forward-query (soil-dry) &self (fromNumber 3))
  ```

### 5.2 Backward Chaining (Goal-Driven Proof Generation)
Defined in [`engine/backward_chain.metta`](file:///home/hope/project_2/pln-engine/engine/backward_chain.metta).

* **Mechanism**: Starts from a target decision goal (e.g. `(irrigate-coffee-plant)`), searches for rules that produce that goal, recurses on required premises, and builds a complete **hierarchical proof tree**.
* **Query Execution**:
  ```metta
  !(backward-query (irrigate-coffee-plant) &self (fromNumber 3))
  ```
* **Sample Proof Output Structure**:
  ```metta
  (proof R3 
      (proof R2 
          (proof R1 
              (proof F1 (soil-dry) (stv-value 0.9 0.9)) 
              (proof F2 (temperature-high) (stv-value 0.85 0.88)) 
              (coffee-plant-water-stressed) (stv-value 0.92 0.85)) 
          (proof F6 (water-available) (stv-value 0.95 0.9)) 
          (irrigation-recommended) (stv-value 0.9 0.82)) 
      (proof F7 (farmer-can-irrigate) (stv-value 0.9 0.85)) 
      (irrigate-coffee-plant) (stv-value 0.95 0.88))
  ```

---

## 6. System Evaluation & Test Scenarios

The engine was evaluated across 5 domain scenarios ([`test/test_evaluation_scenarios.metta`](file:///home/hope/project_2/pln-engine/test/test_evaluation_scenarios.metta)):

### Scenario 1: Supported Conclusion
- **Premises**: `soil-dry` $\langle 0.90, 0.90 \rangle$ and `temperature-high` $\langle 0.85, 0.88 \rangle$.
- **Deduction Output**:
  $$\text{Strength} = 0.90 \times 0.85 = \mathbf{0.765}$$
  $$\text{Confidence} = 0.90 \times 0.88 = \mathbf{0.792}$$
- **Result**: `(stv-value 0.765 0.792)` ✅

### Scenario 2: Incomplete & Uncertain Evidence
- **Premises**: Low-confidence sensor $\langle 0.60, 0.35 \rangle$ and rule $\langle 0.70, 0.40 \rangle$.
- **Result**: `(stv-value 0.42 0.14)` — System correctly reflects low confidence without failing ✅

### Scenario 3: Multiple Explanations (Abduction vs. Induction)
- **Pathology A (Leaf Rust)**: Abduction on orange spots & humidity $\rightarrow \mathbf{\langle 0.6864, 0.576 \rangle}$
- **Pathology B (Nutrient Deficiency)**: Induction on wilting & dry soil $\rightarrow \mathbf{\langle 0.825, 0.630 \rangle}$
- **Result**: System ranks competing diagnostic hypotheses clearly by strength and confidence ✅

### Scenario 4: Belief Revision under Conflicting Sensor Data
- **Sensor 1**: `(soil-dry)` $\langle 0.90, 0.90 \rangle$
- **Sensor 2**: Conflicting reading $\langle 0.40, 0.85 \rangle$
- **Revision Calculation**:
  $$\text{Strength} = \frac{(0.90 \times 0.90) + (0.40 \times 0.85)}{0.90 + 0.85} = \frac{0.81 + 0.34}{1.75} = \mathbf{0.6571}$$
  $$\text{Confidence} = \frac{0.90 + 0.85}{2} = \mathbf{0.875}$$
- **Result**: `(stv-value 0.6571428571428571 0.875)` — Merging reduces strength while boosting total confidence ✅

### Scenario 5: Multi-Step Confidence Decay
- **Chain**: Step 1 ($c=0.792$) $\rightarrow$ Step 2 ($c=0.7128$).
- **Result**: Demonstrates natural, rigorous uncertainty decay over multi-hop reasoning steps ✅

---

## 7. Interactive Streamlit Dashboard ([`FrontEnd.py`](file:///home/hope/project_2/pln-engine/FrontEnd.py))

To make the engine accessible to non-technical domain experts (e.g. agronomists, farmers), an interactive UI dashboard was created with **Streamlit**:

### Key Features
- **Knowledge Base Viewer**: Visualizes all facts, STV values, and inference rules.
- **Interactive PLN Calculator**: Allows users to select facts or custom STVs and execute Deduction, Induction, Abduction, or Revision in real-time.
- **Forward & Backward Chaining Runner**: Runs inference queries and displays output logs and generated proof trees.

### Running the UI
```bash
streamlit run FrontEnd.py
```

---

## 8. Verification & Execution Guide

### 8.1 Prerequisites
- **MeTTa 0.2.10** installed in standard path (`metta` command available).
- **Python 3.10+** with Streamlit installed (for Web UI).

### 8.2 Execution Commands
To run the individual test suites:

```bash
# Fact & STV Lookups
metta test/test_fact_stv.metta

# Deduction Operations
metta test/test_deduction.metta

# Revision Formula
metta test/test_revision.metta

# Forward Chaining Engine
metta test/test_forward_chaining.metta

# Backward Chaining Proof Engine
metta test/test_backward_chaining.metta

# 5 PDF Evaluation Scenarios
metta test/test_evaluation_scenarios.metta

# Master Integration Test Suite
metta test/test_agriculture.metta
```

---

## 9. Limitations & Theoretical Extensions

1. **Combinatorial Explosion**: Deep backward chaining depth ($>4$ hops) can produce exponential branch explosion. 
   - *Fix / Extension*: Implementing **Economic Attention Networks (ECAN)** to assign **Short-Term Importance (STI)** to active concepts and dynamically prune unpromising proof branches.
2. **Automated STV Learning**: STVs are currently initialized based on expert domain knowledge. Integrating real-time machine learning data pipelines will allow automated updating of base STVs from continuous IoT sensor telemetry.

---

## 10. Conclusion

This project successfully demonstrates a domain-specific, native MeTTa implementation of Probabilistic Logic Networks. By combining probabilistic truth values with multi-hop forward and backward chaining, the engine provides mathematically sound, interpretable, and uncertainty-aware decision-making for agricultural management.
