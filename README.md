# 🌾 agri-pln-metta: Domain-Specific Agricultural Probabilistic Logic Network Reasoning Engine

[![Language](https://img.shields.io/badge/Language-MeTTa-blue.svg)](https://wiki.opencog.org/w/MeTTa)
[![Framework](https://img.shields.io/badge/Framework-OpenCog%20Hyperon-orange.svg)](https://opencog.org/)
[![UI](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-9%20Passed%2C%200%20Failed-brightgreen.svg)](tests/)

**`agri-pln-metta`** is a mini **Probabilistic Logic Network (PLN)** reasoning engine implemented natively in **MeTTa** (Meta Type Talk) for OpenCog Hyperon, specifically engineered for the agricultural domain.

The system performs probabilistic, symbolic, and causal reasoning over interconnected agronomic knowledge—diagnosing crop diseases, evaluating environmental microclimatic risks, handling incomplete and conflicting evidence, and prescribing Integrated Pest Management (IPM) interventions.

---

## 📖 Table of Contents
1. [Why Agriculture & Probabilistic Reasoning?](#-why-agriculture--probabilistic-reasoning)
2. [Core PLN Foundations](#-core-pln-foundations)
3. [Knowledge Representation & AtomSpace Architecture](#-knowledge-representation--atomspace-architecture)
4. [PLN Inference Operations](#-pln-inference-operations)
   - [Simple Truth Values (STV)](#1-simple-truth-values-stv)
   - [Deduction](#2-deduction)
   - [Induction](#3-induction)
   - [Abduction](#4-abduction)
   - [Revision](#5-revision)
   - [Multi-Step Chaining](#6-multi-step-chaining)
   - [Forward & Backward Chaining](#7-forward--backward-chaining)
5. [Project Architecture](#-project-architecture)
6. [Installation & Requirements](#-installation--requirements)
7. [Running the Streamlit UI](#-running-the-streamlit-ui)
8. [Running the Demonstration](#-running-the-demonstration)
9. [Running Automated Tests](#-running-automated-tests)
10. [CLI Usage & Example Queries](#-cli-usage--example-queries)
11. [The 7 Required Evaluation Scenarios](#-the-7-required-evaluation-scenarios)
12. [Assumptions, Limitations & Future Work](#-assumptions-limitations--future-work)

---

## 🌾 Why Agriculture & Probabilistic Reasoning?

Agricultural systems operate in dynamic, open-world environments characterized by uncertainty:
- **Imperfect Observability:** Field scouts observe foliar symptoms (e.g. leaf spots, wilting) without continuous laboratory assays.
- **Etiological Equifinality:** Multiple divergent pathogens or nutrient deficiencies cause indistinguishable visual symptoms (e.g., *YellowLeaves* caused by *CoffeeLeafRust*, *RootRot*, or *NitrogenDeficiency*).
- **Noisy & Multi-Source Evidence:** Scouting reports, satellite humidity forecasts, and PCR tests carry differing levels of epistemic certainty.

Traditional rule engines fail because they treat rules as crisp boolean logic. **`agri-pln-metta`** uses Probabilistic Logic Networks (PLN) to assign **Strength** and **Confidence** to every agronomic link, enabling principled belief revision, diagnostic abduction, and multi-hop uncertainty propagation.

---

## 🧠 Core PLN Foundations

In Probabilistic Logic Networks, propositions and relational links carry a **Simple Truth Value (STV)**:
$$\text{STV} = (s, c)$$
- **Strength ($s \in [0.0, 1.0]$):** The estimated probability of the statement, $P(A)$ or conditional probability $P(B|A)$.
- **Confidence ($c \in [0.0, 1.0]$):** Epistemic reliability based on the total weight of supporting evidence $w$:
  $$w = k \cdot \frac{c}{1.0 - c}, \quad c = \frac{w}{w + k} \quad (k = 1.0)$$

---

## 🌐 Knowledge Representation & AtomSpace Architecture

The agricultural knowledge base (`knowledge/`) is organized into modular sub-spaces unified into a single AtomSpace:

- **Crops (`crops.metta`):** `Coffee`, `Maize`, `Wheat`, `Teff`, `Tomato`, `Potato`, `Barley`. Includes botanical families and crop-disease susceptibilities `(Susceptible Coffee CoffeeLeafRust (stv 0.85 0.90))`.
- **Diseases & Pathogens (`diseases.metta`):** `CoffeeLeafRust`, `CoffeeBerryDisease`, `BrownEyeSpot`, `MaizeRust`, `LateBlight`, `RootRot`, `NitrogenDeficiency`, with baseline priors `(PriorDisease CoffeeLeafRust (stv 0.30 0.85))`.
- **Symptoms (`symptoms.metta`):** `OrangeLeafSpots`, `YellowLeaves`, `BrownPustules`, `WaterSoakedLesions`, `WhitePowderyPatches`, `Wilting`, `StuntedGrowth`. Links: `(Relation causes CoffeeLeafRust OrangeLeafSpots (stv 0.90 0.85))`.
- **Environmental Conditions (`conditions.metta`):** `HighHumidity`, `ExcessMoisture`, `PoorDrainage`, `WaterloggedSoil`, `DenseCanopyShade`. Links: `(Relation increases-risk HighHumidity CoffeeLeafRust (stv 0.85 0.80))`.
- **Treatments & Interventions (`treatments.metta`):** `CopperFungicide`, `SystemicFungicide`, `ImproveDrainage`, `CanopyPruning`, `BalancedNPKFertilization`, `ResistantCultivar`.

Both **Forward Chaining** and **Backward Chaining** operate over the **same unified knowledge base**.

---

## ⚡ PLN Inference Operations

### 1. Simple Truth Values (STV)
Defined in `pln/stv.metta` with getters, constructors, boundary clamping ($[0.0, 1.0]$), and evidence weight conversion.

### 2. Deduction
Implements syllogistic forward propagation ($A \to B, B \to C \vdash A \to C$):
$$s = s_1 \cdot s_2, \quad c = c_1 \cdot c_2 \cdot \max(0.1, s_1)$$
Confidence decays gracefully across the chain to reflect transitive uncertainty.

### 3. Induction
1. **Sample Count Induction:** Generalizes rules from multi-farm surveys:
   $$s = \frac{P}{N}, \quad c = \frac{N}{N + k}$$
2. **Bayesian Inverse Induction:** Derives causal strength $P(B|A)$ from diagnostic indicator $P(A|B)$ and marginal priors.

### 4. Abduction
Implements diagnostic reasoning from observed effect $B$ to candidate disease cause $A$:
$$s = \frac{s_{obs} \cdot s_{rule} \cdot s_{pri}}{s_{rule} \cdot s_{pri} + (1 - s_{rule})(1 - s_{pri})}, \quad c = c_{rule} \cdot c_{obs} \cdot c_{pri} \cdot 0.85$$
When multiple diseases match a symptom, abduction outputs all candidate hypotheses with their respective calculated STVs.

### 5. Revision
Combines independent evidence streams ($E_1, E_2$) for proposition $X$:
$$w_1 = \frac{c_1}{1 - c_1}, \quad w_2 = \frac{c_2}{1 - c_2}, \quad w_{tot} = w_1 + w_2$$
$$s_{rev} = \frac{w_1 s_1 + w_2 s_2}{w_{tot}}, \quad c_{rev} = \frac{w_{tot}}{w_{tot} + 1.0}$$
- **Agreeing Evidence:** Boosts overall confidence ($c_{rev} > \max(c_1, c_2)$).
- **Conflicting Evidence:** Moves strength to the evidence-weighted center while reflecting total evidence weight.

### 6. Multi-Step Chaining
Evaluates $N$-hop causal paths ($A \to B \to C \to D$) with full step logging and progressive uncertainty decay.

### 7. Forward & Backward Chaining
- **Forward Chaining (`pln/forward.metta`):** Data-driven: Observations (`Coffee` + `HighHumidity` + `OrangeLeafSpots`) $\to$ Disease Risk $\to$ Disease Diagnosis $\to$ Actionable IPM Treatments.
- **Backward Chaining (`pln/backward.metta`):** Goal-driven: Goal hypothesis $\to$ backward search for supporting premises in KB $\to$ verify observed vs missing evidence $\to$ construct proof tree with uncertainty penalty.

---

## 📁 Project Architecture

```
agri-pln-metta/
├── README.md                      # Comprehensive project documentation
├── LICENSE                        # MIT License
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Packaging metadata
├── runner.py                      # Automated test suite runner
├── cli.py                         # Interactive and scripted CLI
├── app.py                         # Streamlit interactive UI dashboard
├── engine_bridge.py               # Python-MeTTa bridge & parser
├── demo.metta                     # Full interactive MeTTa demonstration
│
├── knowledge/                     # Agricultural Knowledge Substrate
│   ├── crops.metta                # Crops, botanical taxonomy, susceptibilities
│   ├── diseases.metta             # Fungal, bacterial, abiotic diseases & priors
│   ├── symptoms.metta             # Foliar & fruit symptoms & causal links
│   ├── conditions.metta           # Environmental conditions & risk rules
│   ├── treatments.metta           # Curative, cultural & preventive IPM actions
│   └── agriculture_kb.metta       # Unified AtomSpace loader & accessors
│
├── pln/                           # Core Probabilistic Logic Network Engine
│   ├── stv.metta                  # STV structure, getters, validator, weights
│   ├── formulas.metta             # PLN algebraic update formulas
│   ├── deduction.metta            # Probabilistic deduction rules
│   ├── induction.metta            # Observational & Bayesian induction
│   ├── abduction.metta            # Diagnostic abduction & differential diagnosis
│   ├── revision.metta             # Multi-source belief revision & fusion
│   ├── chaining.metta             # Multi-hop causal path reasoner
│   ├── forward.metta              # Data-driven forward chaining pipeline
│   └── backward.metta             # Goal-driven backward chaining engine
│
├── queries/                       # High-Level Agricultural Queries & Scenarios
│   ├── diagnosis.metta            # Diagnostic & differential queries
│   ├── risk.metta                 # Environmental risk forecasting queries
│   ├── treatment.metta            # IPM treatment package selectors
│   └── scenarios.metta            # The 7 required evaluation scenarios
│
├── tests/                         # Automated Unit & Integration Test Suites
│   ├── test_stv.metta             # STV unit tests
│   ├── test_deduction.metta       # Deduction unit tests
│   ├── test_induction.metta       # Induction unit tests
│   ├── test_abduction.metta       # Abduction unit tests
│   ├── test_revision.metta        # Revision unit tests
│   ├── test_chaining.metta        # Multi-hop chaining unit tests
│   ├── test_forward.metta         # Forward chaining unit tests
│   ├── test_backward.metta        # Backward chaining unit tests
│   └── test_edge_cases.metta      # Edge cases, unknown entities & cycles
│
└── docs/
    └── technical_report.md        # Formal technical report
```

---

## 🛠️ Installation & Requirements

### Prerequisites
- Python 3.10+
- OpenCog Hyperon MeTTa (`hyperon>=0.2.10`)
- Streamlit (`streamlit>=1.30.0`)

### Installation
```bash
git clone https://github.com/Tesfalegnp/PLN-Reasoning-Core.git
cd PLN-Reasoning-Core
pip install -r requirements.txt
```

---

## 🖥️ Running the Streamlit UI

Launch the interactive web demonstration dashboard:

```bash
streamlit run app.py
```

The UI provides:
1. **Interactive Field Reasoner:** Select crops, microclimates, and foliar symptoms to trigger forward/backward PLN inference.
2. **Differential Diagnosis Explorer:** Side-by-side comparison of candidate etiologies for ambiguous symptoms.
3. **Belief Revision Lab:** Sliders to fuse scouting and lab PCR evidence dynamically.
4. **Multi-Hop Causal Explorer:** Visualizer for 3-hop causal chains.
5. **1-Click Demo Scenarios:** Instant pre-configured evaluation scenarios.

---

## 🚀 Running the Demonstration

To run the complete interactive MeTTa demonstration script directly:

```bash
metta demo.metta
```
Or via the Python wrapper:
```bash
python3 cli.py demo
```

---

## 🧪 Running Automated Tests

Run all 9 MeTTa test suites using the automated test runner:

```bash
python3 runner.py
```

### Expected Output:
```
================================================================================
 agri-pln-metta: Automated Test Runner
 MeTTa Runtime: /home/hope/Projects/pln_engin_project/.venv-metta/bin/metta
 Workspace Root: /path/to/agri-pln-metta
================================================================================
 [PASS] tests/test_abduction.metta (2.30s)
 [PASS] tests/test_backward.metta (4.14s)
 [PASS] tests/test_chaining.metta (1.23s)
 [PASS] tests/test_deduction.metta (0.87s)
 [PASS] tests/test_edge_cases.metta (1.23s)
 [PASS] tests/test_forward.metta (4.94s)
 [PASS] tests/test_induction.metta (0.67s)
 [PASS] tests/test_revision.metta (1.60s)
 [PASS] tests/test_stv.metta (0.42s)
================================================================================
Summary: 9 passed, 0 failed out of 9 total test suites.
================================================================================
All test suites passed successfully!
```

---

## 💻 CLI Usage & Example Queries

The CLI tool (`cli.py`) supports interactive queries:

### 1. Forward Chaining Diagnosis & Treatment
```bash
python3 cli.py forward --crop Coffee --condition HighHumidity --symptom OrangeLeafSpots
```

### 2. Goal Verification via Backward Chaining
```bash
python3 cli.py backward --crop Coffee --disease CoffeeLeafRust --condition HighHumidity --symptom OrangeLeafSpots
```

### 3. Multi-Source Evidence Revision
```bash
python3 cli.py revise --prop CoffeeLeafRust --s1 0.85 --c1 0.70 --s2 0.95 --c2 0.90
```

### 4. Execute All 7 Evaluation Scenarios
```bash
python3 cli.py scenarios
```

---

## 📋 The 7 Required Evaluation Scenarios

### Scenario 1: Strongly Supported Conclusion (Deduction)
- **Input:** `HighHumidity` increases risk of `CoffeeLeafRust`; `CoffeeLeafRust` causes `OrangeLeafSpots`.
- **Output:** Deduced link `HighHumidity` $\to$ `OrangeLeafSpots` with calculated STV $(0.765, 0.578)$.

### Scenario 2: Incomplete / Uncertain Evidence
- **Input:** `Coffee` + `OrangeLeafSpots` observed, but humidity condition is unobserved.
- **Output:** Backward reasoner verifies symptoms but flags `HighHumidity` as unobserved, penalizing goal confidence to $(0.635, 0.279)$.

### Scenario 3: Multiple Plausible Explanations (Differential Diagnosis)
- **Input:** `Coffee` leaves turning yellow (`YellowLeaves`).
- **Output:** Returns multiple competing candidate etiologies (`CoffeeLeafRust`, `RootRot`, `BrownEyeSpot`, `NitrogenDeficiency`) with distinct STVs.

### Scenario 4: New / Conflicting Evidence (Revision)
- **Reinforcing:** Field scouting $(0.85, 0.70)$ + Laboratory PCR $(0.95, 0.90) \implies (0.929, 0.919)$ (confidence increases).
- **Conflicting:** Visual symptoms $(0.90, 0.80)$ vs Negative microscopy $(0.10, 0.80) \implies (0.50, 0.888)$ (strength shifts to neutral midpoint).

### Scenario 5: Multi-Step Causal Inference (3-Hop Path)
- **Path:** `PoorDrainage` $\to$ `WaterloggedSoil` $\to$ `RootRot` $\to$ `Wilting`.
- **Output:** Complete 3-step proof path logged with computed STV $(0.673, 0.438)$.

### Scenario 6: Data-Driven Forward Chaining
- **Input:** `Coffee` + `HighHumidity` + `OrangeLeafSpots`.
- **Output:** Derives disease diagnosis (`CoffeeLeafRust`, STV $(0.737, 0.738)$) and actionable IPM prescriptions (`CopperFungicide`, `CanopyPruning`, `SystemicFungicide`).

### Scenario 7: Goal-Driven Backward Chaining
- **Target Goal:** `(VerifyDisease CoffeeLeafRust)` with complete observations.
- **Output:** Complete backward proof tree verifying all premises with zero missing evidence.

---

## ⚠️ Assumptions, Limitations & Future Work

1. **Simplified STV Formulation:** Uses standard PLN Simple Truth Values $(s, c)$. Second-order probability density distributions (Beta distributions) are not modeled.
2. **Deterministic Priors:** Priors are static baseline regional estimates; future work can integrate dynamic GIS/seasonal weather APIs.
3. **Continuous Learning:** Future extensions will integrate online weight updates from post-harvest farmer feedback.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
