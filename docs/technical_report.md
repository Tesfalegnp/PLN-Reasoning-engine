# Technical Report: Agricultural Probabilistic Logic Network (agri-pln-metta)

**Project Title:** `agri-pln-metta`  
**Core Framework:** OpenCog Hyperon / MeTTa (Meta Type Talk)  
**Domain:** Agricultural Pathology, Agronomy, and Integrated Pest Management (IPM)  
**Primary Engine Language:** MeTTa  

---

## 1. Executive Summary & Domain Motivation

Agricultural decision-making occurs under severe environmental, biological, and observational uncertainty:
1. **Incomplete Observations:** Farmers frequently observe foliar symptoms (e.g., yellowing leaves, orange pustules) without real-time microclimate sensors or laboratory diagnostics.
2. **Multiple Competing Causes:** Identical phenotypic symptoms can arise from divergent etiologies (e.g., *YellowLeaves* caused by fungal rust, soil-borne root rot, or nitrogen deficiency).
3. **Noisy, Multi-Source Evidence:** Scouting reports, satellite weather data, and laboratory PCR assays possess differing degrees of reliability and epistemic certainty.

To address these challenges, **`agri-pln-metta`** implements a domain-specific **Probabilistic Logic Network (PLN)** mini-reasoning engine directly in **MeTTa**. The engine represents interconnected agricultural knowledge (crops, pathogens, symptoms, edaphic/microclimatic triggers, and IPM treatments) using **Simple Truth Values (STVs)**. It provides native implementations of the four fundamental PLN inference operations (**Deduction, Induction, Abduction, Revision**), multi-hop causal chaining, forward data-driven inference, and goal-driven backward chaining over a single unified AtomSpace.

---

## 2. Knowledge Representation & Simple Truth Values (STV)

### 2.1 STV Formalism
In PLN, propositions carry a Simple Truth Value $(s, c)$ where:
- **Strength ($s \in [0.0, 1.0]$):** Estimated probability of the proposition, $P(A)$ or conditional probability $P(B|A)$.
- **Confidence ($c \in [0.0, 1.0]$):** Epistemic reliability based on total evidence weight $w$:
  $$w = k \cdot \frac{c}{1.0 - c}, \quad c = \frac{w}{w + k} \quad (k = 1.0)$$

### 2.2 Relational AtomSpace Schema
The agricultural domain is modeled as an interconnected hypergraph in MeTTa:
- **Crops:** `(Crop Coffee)`, `(Susceptible Coffee CoffeeLeafRust (stv 0.85 0.90))`
- **Pathogens & Disorders:** `(Disease CoffeeLeafRust)`, `(PriorDisease CoffeeLeafRust (stv 0.30 0.85))`
- **Causal Links:** `(Relation causes CoffeeLeafRust OrangeLeafSpots (stv 0.90 0.85))`
- **Environmental Triggers:** `(Relation increases-risk HighHumidity CoffeeLeafRust (stv 0.85 0.80))`
- **Inter-Condition Links:** `(Relation promotes PoorDrainage WaterloggedSoil (stv 0.90 0.85))`
- **IPM Interventions:** `(Relation effective-treatment CopperFungicide CoffeeLeafRust (stv 0.88 0.85))`

---

## 3. Core PLN Inference Operations in MeTTa

### 3.1 Probabilistic Deduction ($A \to B, B \to C \vdash A \to C$)
Transitive forward chaining across causal and risk links. As chains grow longer, confidence decays gracefully:
$$s = s_1 \cdot s_2, \quad c = c_1 \cdot c_2 \cdot \max(0.1, s_1)$$
*Example:* `HighHumidity` $\to$ `CoffeeLeafRust` $(0.85, 0.80)$ combined with `CoffeeLeafRust` $\to$ `OrangeLeafSpots` $(0.90, 0.85)$ yields deduced link `HighHumidity` $\to$ `OrangeLeafSpots` with STV $(0.765, 0.578)$.

### 3.2 Probabilistic Induction (Observational & Bayesian Generalization)
1. **Sample Count Induction:** Generalizes rules from multi-farm surveys ($P$ positive out of $N$ total plots, personality parameter $k=2.0$):
   $$s = \frac{P}{N}, \quad c = \frac{N}{N + k}$$
   *Example:* 18 positive rust cases out of 20 surveyed farms with high humidity induces risk rule with STV $(0.90, 0.909)$.
2. **Bayesian Inverse Induction:** Computes $P(B|A)$ from $P(A|B)$ and marginal priors:
   $$s = \frac{s_{inv} \cdot s_B}{s_A}, \quad c = c_{inv} \cdot c_A \cdot c_B$$

### 3.3 Probabilistic Abduction ($A \to B, B \vdash A$)
Diagnostic hypothesis generation from observed symptom $B$ to candidate disease cause $A$:
$$s = \frac{s_{obs} \cdot s_{rule} \cdot s_{pri}}{s_{rule} \cdot s_{pri} + (1 - s_{rule})(1 - s_{pri})}, \quad c = c_{rule} \cdot c_{obs} \cdot c_{pri} \cdot 0.85$$
*Feature:* Automatically enumerates all candidate etiologies when symptoms are ambiguous (e.g. *YellowLeaves*), assigning each a distinct STV based on crop susceptibility and pathogen priors.

### 3.4 Probabilistic Revision (Evidence Fusion & Conflict Resolution)
Combines independent evidence streams $E_1(s_1, c_1)$ and $E_2(s_2, c_2)$ for the same proposition:
$$w_1 = \frac{c_1}{1 - c_1}, \quad w_2 = \frac{c_2}{1 - c_2}, \quad w_{tot} = w_1 + w_2$$
$$s_{rev} = \frac{w_1 s_1 + w_2 s_2}{w_{tot}}, \quad c_{rev} = \frac{w_{tot}}{w_{tot} + 1.0}$$
- **Reinforcing Evidence:** Field scouting $(0.85, 0.70)$ + Lab PCR $(0.95, 0.90) \implies (0.929, 0.919)$ (confidence increases).
- **Conflicting Evidence:** Visual rust $(0.90, 0.80)$ vs Negative microscopy $(0.10, 0.80) \implies (0.50, 0.888)$ (strength balances to neutral midpoint).

---

## 4. Search Engines: Forward Chaining, Backward Chaining & Multi-Hop Paths

Both forward and backward search operate on the **exact same underlying AtomSpace** (`&agriculture-kb`).

```
                              Agricultural Knowledge Substrate (&agriculture-kb)
                                   /                                        \
              Forward Chaining (Data-Driven)                     Backward Chaining (Goal-Driven)
        [Observed Facts]                                       [Target Goal Hypothesis]
               |                                                          |
        Deduce Environmental Risk                               Search Supporting Premises in KB
               |                                                          |
        Abduce & Revise Disease Diagnosis                       Verify Observed vs Missing Evidence
               |                                                          |
        Deduce Actionable IPM Treatments                        Construct Proof Tree + Penalize Uncertainty
```

- **Forward Chaining (`pln:forward`):**
  Given observations `Coffee` + `HighHumidity` + `OrangeLeafSpots`, the engine matches premises forward:
  1. Computes environmental disease risk.
  2. Abduces disease diagnosis from symptoms and fuses with environmental risk via revision.
  3. Derives curative chemical/biological treatments (`CopperFungicide`, `SystemicFungicide`) and preventive canopy management actions (`CanopyPruning`).
- **Backward Chaining (`pln:backward`):**
  Given a goal `(VerifyDisease CoffeeLeafRust)`, searches backward for required premises, verifies observed evidence, identifies unobserved factors (e.g., missing humidity data), and penalizes overall confidence while returning the full proof tree.
- **Multi-Hop Chaining (`pln:chaining`):**
  Evaluates 3-hop and 4-hop causal chains (e.g., `PoorDrainage` $\to$ `WaterloggedSoil` $\to$ `RootRot` $\to$ `Wilting`) with progressive uncertainty propagation.

---

## 5. Evaluation Scenarios & Experimental Results

| Scenario | Objective | Input / Context | Inference Used | Output STV | Result / Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | Supported Conclusion | `HighHumidity` $\to$ `CoffeeLeafRust` $\to$ `OrangeLeafSpots` | Deduction | $(0.765, 0.578)$ | Multi-hop deduction verified with confidence decay |
| **Scenario 2** | Incomplete Evidence | `Coffee` + `OrangeLeafSpots` (Missing humidity) | Backward Chaining | $(0.635, 0.279)$ | Confidence penalized from 0.74 to 0.28; missing condition reported |
| **Scenario 3** | Multiple Explanations | `Coffee` + `YellowLeaves` | Differential Abduction | Distinct STVs | Returns `CoffeeLeafRust`, `RootRot`, `BrownEyeSpot` with STVs |
| **Scenario 4A** | Reinforcing Evidence | Field Scouting $(0.85, 0.70)$ + Lab PCR $(0.95, 0.90)$ | Revision | $(0.929, 0.919)$ | Confidence boosts to 0.919 |
| **Scenario 4B** | Conflicting Evidence | Visual Rust $(0.90, 0.80)$ vs Lab Negative $(0.10, 0.80)$ | Revision | $(0.500, 0.888)$ | Strength shifts to 0.50 neutral balance |
| **Scenario 5** | Multi-Hop Causal Chain | `PoorDrainage` $\to$ `Waterlogged` $\to$ `RootRot` $\to$ `Wilting` | 3-Hop Chain | $(0.673, 0.438)$ | Complete 3-step proof path logged with decaying confidence |
| **Scenario 6** | Forward Chaining | `Coffee` + `HighHumidity` + `OrangeLeafSpots` | Full Forward Chain | $(0.737, 0.738)$ | Derives diagnosis + IPM treatments (`CopperFungicide`, etc.) |
| **Scenario 7** | Backward Chaining | Goal: `CoffeeLeafRust` with complete observations | Backward Proof | $(0.737, 0.738)$ | Complete proof tree with verified premises and zero missing evidence |

---

## 6. Streamlit User Interface Architecture

The Streamlit dashboard (`app.py`) serves as a pure presentation and demonstration layer:
```
Streamlit UI (app.py) -> Engine Bridge (engine_bridge.py) -> Hyperon MeTTa CLI -> Agricultural KB & PLN Modules
```
- No PLN logic is duplicated in Python; all arithmetic and rule matches occur in MeTTa.
- The UI exposes:
  1. **Interactive Field Reasoner:** Forward and backward inference over custom crops, conditions, and symptoms.
  2. **Differential Diagnosis Explorer:** Comparative analysis for ambiguous symptoms.
  3. **Belief Revision Lab:** Sliders for dynamic evidence accumulation and conflict resolution.
  4. **Multi-Hop Causal Explorer:** Step-by-step trace of multi-hop chains with decaying confidence.
  5. **1-Click Evaluation Scenarios:** Instant execution and visualization of all 7 required benchmarks.

---

## 7. Verification and Automated Testing

The automated test suite (`runner.py`) executes 9 dedicated MeTTa test files with 100% pass rate:
- `tests/test_stv.metta`: STV creation, getters, bounding, weight conversion.
- `tests/test_deduction.metta`: Deductive transitivity and confidence decay.
- `tests/test_induction.metta`: Sample counts and Bayesian inverse induction.
- `tests/test_abduction.metta`: Diagnostic explanation and candidate filtering.
- `tests/test_revision.metta`: Reinforcing and conflicting evidence fusion.
- `tests/test_chaining.metta`: 2-hop, 3-hop, and 4-hop causal paths.
- `tests/test_forward.metta`: Data-driven forward pipeline and rule firing.
- `tests/test_backward.metta`: Goal verification and missing evidence detection.
- `tests/test_edge_cases.metta`: Unknown crops/diseases, boundary STVs, empty queries.

**Test Summary:** `9 passed, 0 failed out of 9 total test suites.`

---

## 8. Limitations & Future Extensions

1. **Simplified STV Algebra:** The engine uses standard PLN Simple Truth Values $(s, c)$. It does not currently compute full second-order Beta probability density distributions or intensional/extensional blend parameters.
2. **Contextual Priors:** Priors are currently static baseline estimates per crop/disease; dynamic micro-regional priors based on seasonal GIS data would further enhance precision.
3. **Automated Feedback Loop:** Future work can incorporate automated weight learning through online farmer feedback upon harvest outcome verification.
