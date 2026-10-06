# System Architecture Specification

## 1. Architectural Overview

The **Coffee Agriculture PLN Reasoning System** adheres strictly to the principle that **core probabilistic reasoning executes entirely in native MeTTa**, with Python and Streamlit serving solely as integration, orchestration, parsing, and user demonstration layers.

```
+-------------------------------------------------------------------------+
|                  STREAMLIT USER DEMONSTRATION UI                        |
|   (Interactive Diagnosis, Forward Chaining, Evidence Revision, Traces)  |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                    PYTHON INTEGRATION LAYER                             |
|   src/pln_engine/                                                       |
|     ├── runner.py   (Initializes Hyperon Environment, loads MeTTa)      |
|     ├── parser.py   (Parses MeTTa AST, extracts ProofNode hierarchy)    |
|     └── models.py   (Dataclasses: TruthValue, Statement, QueryResult)   |
|   * ZERO semantic reasoning in Python. Strictly an orchestration bridge.|
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                       HYPERON / MeTTa RUNTIME                           |
|                        (Hyperon C-Engine 0.2.10)                        |
+-------------------------------------------------------------------------+
       |                                                    |
       v                                                    v
+-----------------------------+              +----------------------------+
|   AGRICULTURAL KNOWLEDGE    |              |      MeTTa PLN ENGINE      |
|  coffee_agriculture.metta   |              |   metta/core/pln_tv.metta  |
|  - Coffee plants & diseases |              |   metta/core/pln_formulas  |
|  - Symptoms & environmental |              +----------------------------+
|  - Causal rules with STVs   |                             |
+-----------------------------+                             v
               \                                            /
                +---------------------+--------------------+
                                      |
                                      v
                    +------------------------------------+
                    |        MeTTa CHAINING ENGINE       |
                    |   metta/chaining/nat.metta (Peano) |
                    |   metta/rules/agriculture_rules    |
                    |   /                             \  |
                    v                                 v  |
         Backward Chaining (bc.metta)      Forward Chaining (fc.metta)
         - Goal-directed diagnosis         - Data-driven progression
         - Implication-first ordering      - Step-bounded derivation
         - Proof Tree AST synthesis        - Theorem accumulation
                    \                                 /
                     +-------------------------------+
                                      |
                                      v
                      (Proof (⊢ $Concl $TV) $ProofTree)
```

---

## 2. Component Responsibilities

### 2.1 Native MeTTa Layer (`metta/`)
All logical inference and probabilistic arithmetic occur inside the Hyperon interpreter:
1. `metta/core/pln_tv.metta`: Simple Truth Value representation `(stv strength confidence)`, numerical clamps, and weight-of-evidence conversions ($w = \frac{c}{1 - c}, c = \frac{w}{w + 1}$).
2. `metta/core/pln_formulas.metta`: Official TrueAGI PLN formulas:
   - Deduction: $s = s_1 s_2, c = (s_1 s_2)(c_1 c_2)$.
   - Modus Ponens: $s = s_P s_{imp} + 0.02(1 - s_P), c = (s_P s_{imp})(c_P c_{imp})$.
   - Revision: Exact pooled evidence weighting.
   - Induction & Abduction formulas.
3. `metta/chaining/nat.metta`: Peano natural numbers (`Z`, `S $k`) bounding search depth to guarantee termination over cyclic graphs.
4. `metta/rules/agriculture_rules.metta`: Declarative inference rulebase (`rb`) for deduction, modus ponens, and cultivar similarity symmetry.
5. `metta/chaining/bc.metta`: Goal-directed backward chainer returning structured proof trees `(Proof (⊢ $concl $tv) (Rule $rule $sub1 $sub2))`.
6. `metta/chaining/fc.metta`: Forward chainer accumulating derived theorems from seed premises.
7. `metta/kb/coffee_agriculture.metta`: Shared domain knowledge base used identically by both BC and FC.

### 2.2 Python Integration Layer (`src/pln_engine/`)
Python is strictly a runtime bridge:
- `runner.py`: Wraps `hyperon.Environment.custom_env`, loads MeTTa modules into the runner space, invokes queries via `runner.run()`, and returns raw AST atoms.
- `parser.py`: Pure AST parser converting string representations of Hyperon expression atoms into strongly-typed Python dataclasses.
- `models.py`: Immutable data models representing results for downstream presentation.

### 2.3 User Interface Layer (`streamlit_app/`)
Streamlit provides a clean, reactive dashboard rendering:
- Real-time goal-directed diagnosis with interactive depth controls.
- Step-by-step forward symptom progression.
- Conflicting evidence resolution slider demonstrations.
- Side-by-side Forward vs. Backward comparison over identical agronomic queries.

---

## 3. Backward Chaining Search Ordering

In backward chaining, solving a goal $Q$ via Modus Ponens $P, (P \to Q) \vdash Q$ requires matching two subgoals. 
If an unbound subgoal $P$ is solved first, MeTTa explores all combinations in the knowledge base, causing combinatorial slowdown.
Our backward chainer implements **implication-first matching**:
```metta
(= (bc (⊢ $concl $tv) (S $k))
   (let* (((rule mp $p (→ $p $concl) $concl) (rb))
          ((Proof (⊢ (→ $p $concl) $tvImp) $subImp) (bc (⊢ (→ $p $concl) $tvImp) $k))
          ((Proof (⊢ $p $tvP) $subP) (bc (⊢ $p $tvP) $k))
          ($tv (Truth_Apply_Rule2 mp $tvP $tvImp)))
     (Proof (⊢ $concl $tv) (Rule mp $subP $subImp))))
```
Matching `(→ $p $concl)` first binds `$p` directly to the specific premise associated with goal `$concl`, making subgoal resolution direct, deterministic, and instant (<70ms).
