# Agricultural PLN Reasoning System

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Hyperon](https://img.shields.io/badge/Hyperon-0.2.10-green.svg)](https://github.com/trueagi-io/hyperon-experimental)
[![Tests](https://img.shields.io/badge/pytest-50%20passed-brightgreen.svg)]()
[![Domain](https://img.shields.io/badge/Domain-Coffee%20Agriculture-brown.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-1.65.0-red.svg)](https://streamlit.io/)

A complete, professional, reproducible **Probabilistic Logic Network (PLN)** reasoning system implemented natively in **MeTTa** (OpenCog Hyperon), with Python integration and an interactive Streamlit demonstration interface focused exclusively on **Coffee Plant Agriculture Disease Diagnosis and Management**.

> *"I implemented a MeTTa-native Probabilistic Logic Network for coffee agriculture that represents uncertain agricultural knowledge with Simple Truth Values, performs deduction, induction, abduction and revision, and uses both forward and backward chaining to reason about coffee plant diseases, with Python and Streamlit used only to provide the final interactive demonstration."*

---

## 🏛 System Architecture

The architecture enforces a strict decoupling: **core logical and probabilistic reasoning executes entirely in native MeTTa**, while Python and Streamlit serve strictly as an orchestration, parsing, and interactive visualization layer:

```
┌─────────────────────────────────────────────────────────────┐
│                 Streamlit Web Demonstration                 │
│   • Goal-Directed BC    • Data-Driven FC    • PLN Revision  │
│   • Coffee Disease Diagnosis & Treatment Protocols          │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    Python Integration Layer                 │
│   • PLNRunner (Runner State)      • Expression AST Parser   │
│   • Dataclass Models (TruthValue, ProofNode, QueryResult)   │
│   * ZERO semantic reasoning in Python. Pure bridge.         │
└──────────────────────────────┬──────────────────────────────┘
                               │ from hyperon import MeTTa
┌──────────────────────────────▼──────────────────────────────┐
│              Core Native MeTTa Reasoning Engine              │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │     pln_tv.metta      │       │  pln_formulas.metta   │  │
│  │ (stv s c), clamp, /safe│      │ Deduction, MP, Revision│ │
│  └───────────────────────┘       └───────────────────────┘  │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │       nat.metta       │       │ agriculture_rules.metta│ │
│  │ Peano Bounded Depth   │       │ ded, mp, sim_sym      │  │
│  └───────────────────────┘       └───────────────────────┘  │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │        bc.metta       │       │        fc.metta       │  │
│  │ Goal-Directed BC +    │       │ Step-Bounded Forward  │  │
│  │ Recursive Proof Trees │       │ Chainer Derivations   │  │
│  └───────────────────────┘       └───────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Coffee Agriculture Knowledge Base           │  │
│  │             metta/kb/coffee_agriculture.metta         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## ☕ Coffee Agriculture Domain & Pathology

The system models expert coffee agronomy (*Coffea arabica*):
1. **Fungal Pathologies**:
   - **Coffee Leaf Rust (*Hemileia vastatrix*)**: Elicited by `OrangeRustPustules` $(s=0.88, c=0.85)$, favored by `HighHumidity` and `DenseShadedCanopy`. Requires `CopperFungicideSpray` and `CanopyPruning`.
   - **Coffee Berry Disease (*Colletotrichum kahawae*)**: Manifests as `DarkBerryLesions` under `HeavyRainfall`. Requires `TargetedBerryFungicide`.
2. **Nutritional Disorders**:
   - **Nitrogen Deficiency**: Manifests as `YellowLeafChlorosis` in `AcidicLeachedSoil`. Requires `NitrogenFertilizer`.
3. **Single Shared Knowledge Base**:
   - The **same** file (`metta/kb/coffee_agriculture.metta`) powers both **Backward Chaining** (querying treatment or disease goals) and **Forward Chaining** (data-driven symptom progression).
4. **Conflicting Field Scout Evidence**:
   - Scout A (Agronomist) confirms rust symptoms: $(stv\ 0.85\ 0.75)$.
   - Scout B (Field Assistant) reports symptoms absent: $(stv\ 0.20\ 0.70)$.
   - **PLN Revision** pools evidence weights ($w_1 = 3.0, w_2 = 2.33, w_{total} = 5.33$), yielding a balanced probability ($s=0.5656$) and elevated confidence ($c=0.8421$).

---

## 🔬 Four Agricultural PLN Operations

| Operation | Mathematical Formula | Agricultural MeTTa Input | MeTTa Execution Output |
| :--- | :--- | :--- | :--- |
| **Deduction** | $s = s_1 s_2, \quad c = (s_1 s_2)(c_1 c_2)$ | `!(Truth_Deduction (stv 0.90 0.85) (stv 0.80 0.75))` | `(stv 0.7200 0.4590)` |
| **Induction** | $s = s_{BA} s_{BC}, \quad c = \text{w2c}(s_{BC} c_{BC} c_{BA})$ | `!(Truth_Induction (stv 0.80 0.70) (stv 0.85 0.75))` | `(stv 0.6800 0.3086)` |
| **Abduction** | $s = s_{AB} s_{CB}, \quad c = \text{w2c}(s_{AB} c_{AB} c_{CB})$ | `!(Truth_Abduction (stv 0.85 0.75) (stv 0.80 0.70))` | `(stv 0.6800 0.3086)` |
| **Revision** | $w = w_1 + w_2, \quad s = \frac{s_1 w_1 + s_2 w_2}{w}, \quad c = \text{w2c}(w)$ | `!(Truth_Revision (stv 0.85 0.75) (stv 0.20 0.70))` | `(stv 0.5656 0.8421)` |

---

## 📁 Repository Directory Structure

```
pln_engin_project/
├── metta/                             # 100% Native MeTTa Logic & Rules
│   ├── main.metta                     # Unified master loading module
│   ├── core/
│   │   ├── pln_tv.metta               # Truth values: (stv s c), conversions, clamps
│   │   └── pln_formulas.metta         # Deduction, MP, Revision, Induction, Abduction
│   ├── chaining/
│   │   ├── nat.metta                  # Peano natural numbers (Z, S k) for bounded depth
│   │   ├── bc.metta                   # Goal-directed backward chainer + proof trees
│   │   └── fc.metta                   # Step-bounded forward chainer
│   ├── rules/
│   │   ├── agriculture_rules.metta    # Inference rules: ded, mp, sim_sym
│   │   └── rules.metta                # Alias to agriculture rules
│   ├── kb/
│   │   └── coffee_agriculture.metta   # Dedicated Coffee Agriculture Knowledge Base
│   └── tests/
│       └── test_pln_core.metta        # Native MeTTa test suite
├── examples/
│   ├── agriculture_pln_demo.metta     # 4 PLN operations CLI demo
│   ├── agriculture_forward.metta      # Forward chaining CLI demo
│   ├── agriculture_backward.metta     # Backward chaining CLI demo
│   ├── agriculture_revision.metta     # Conflicting evidence CLI demo
│   └── pln_demo.metta                 # Canonical demo script
├── src/
│   └── pln_engine/                    # Python Integration Layer
│       ├── __init__.py
│       ├── models.py                  # TruthValue, Statement, ProofNode, QueryResult
│       ├── parser.py                  # Pure AST parser converting Hyperon atoms
│       └── runner.py                  # Hyperon runner orchestrator
├── streamlit_app/
│   └── app.py                         # Interactive Streamlit Demo UI
├── tests/                             # Automated Pytest Suite (50 tests)
│   ├── test_pln_core.py               # PLN mathematical formulas & boundaries
│   ├── test_forward_chaining.py       # Forward chaining Tests 1-9 on coffee KB
│   ├── test_backward_chaining.py      # Backward chaining Cases A-G on coffee KB
│   ├── test_coffee_agriculture.py     # Real agronomic pathways (Rust, Berry, Chlorosis)
│   ├── test_agriculture_conflicting_evidence.py # Evidence pooling & revision
│   ├── test_negative_and_edge_cases.py# Controls, missing facts, cyclic graphs
│   ├── test_parser.py                 # AST expression and proof tree parser
│   └── test_python_metta_integration.py # Python/Hyperon bridge verification
├── docs/
│   ├── agriculture-domain.md          # Full agronomy ontology and pathology specs
│   ├── architecture.md                # System architecture and flow diagrams
│   ├── official-audit.md              # TrueAGI source comparison table
│   ├── reasoning-trace.md             # Proof AST structure and explainability
│   ├── evaluation.md                  # Test metrics and benchmark results
│   ├── demo-guide.md                  # Evaluator step-by-step reproduction guide
│   ├── mentor-demo-script.md          # 5-10 minute presentation script
│   ├── environment.md                 # Pinned system specifications and freeze
│   ├── technical-report.md            # Comprehensive 20-section technical report
│   └── final-validation-report.md     # Final validation report and checklist
├── run_tests.sh                       # One-command verification script
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Linux / macOS / WSL
- Python 3.12 (for `hyperon` C-extension compatibility)
- `uv` package manager (recommended) or standard `pip`

### Step 1: Provision Isolated Environment
```bash
# Provision Python 3.12 virtual environment using uv
uv python install 3.12
uv venv .venv-metta --python 3.12
source .venv-metta/bin/activate

# Install dependencies
uv pip install -p .venv-metta hyperon streamlit pytest
```

### Step 2: Run Full Automated Verification Suite
```bash
./run_tests.sh
```
Output:
```text
====================================================================
Coffee Agriculture PLN Reasoning System — Verification Suite
====================================================================
...
======================== 50 passed in 95.86s (0:01:35) =========================
ALL TESTS PASSED! System is 100% verified and reproducible.
```

### Step 3: Run Direct MeTTa CLI Demos
Verify that reasoning executes 100% natively in the official MeTTa interpreter without Python:
```bash
.venv-metta/bin/metta examples/agriculture_pln_demo.metta
.venv-metta/bin/metta examples/agriculture_forward.metta
.venv-metta/bin/metta examples/agriculture_backward.metta
.venv-metta/bin/metta examples/agriculture_revision.metta
```

### Step 4: Launch Interactive Streamlit Demonstration
```bash
.venv-metta/bin/streamlit run streamlit_app/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.
