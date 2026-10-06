# Technical Report: Probabilistic Logic Network (PLN) Reasoning in MeTTa

**Project**: Native MeTTa Probabilistic Logic Network Engine with Chaining & UI  
**Domain**: Coffee Agriculture & Agronomic Plant Pathology  
**Engine**: TrueAGI Hyperon 0.2.10  
**Date**: October 6, 2026  
**Auditor**: Antigravity MeTTa/PLN Engineering System  

---

## 1. Introduction

Probabilistic Logic Networks (PLN) provide a unified mathematical framework for uncertain, non-monotonic, and multi-step inference in symbolic knowledge graphs. While classical first-order logic struggles with incomplete or conflicting field observations, PLN explicitly tracks both the estimated probability (*strength*) and the amount of evidence (*confidence*).

This project implements a fully MeTTa-native PLN reasoning engine executed inside the official **OpenCog Hyperon 0.2.10** runtime. The system features bounded Backward Chaining, step-bounded Forward Chaining, conflicting evidence fusion via PLN Revision, a clean Python orchestration bridge, and an interactive Streamlit demonstration UI centered on **Coffee Agriculture and Disease Diagnosis**.

---

## 2. Problem Definition

In agricultural field operations, plant pathology decisions must be made under substantial uncertainty:
- Visual scouts may report ambiguous symptoms (e.g., partial leaf discoloration).
- Multiple observers or automated IoT sensors may disagree.
- Multi-step diagnostic chains compound observational and causal uncertainty.

Classical deductive logic fails because a single conflicting premise causes explosive inconsistency. Machine learning classifiers provide point predictions but lack causal explainability and proof traces. PLN solves both issues by propagating continuous second-order truth values across declarative rules while emitting transparent, verifiable proof DAGs.

---

## 3. Knowledge Representation in MeTTa

All propositions, facts, and rules are represented as native S-expressions (Atomese ASTs):
- **Grounded Fact**: `(⊢ <Proposition> (stv <Strength> <Confidence>))`
- **Taxonomic Inheritance**: `(Inheritance <Entity> <Concept>)`
- **Causal / Diagnostic Implication**: `(→ <Premise> <Consequent>)`
- **Observational Predicate**: `(HasSymptom <Plant> <Symptom>)`
- **Environmental Risk Factor**: `(EnvironmentalRisk <Plant> <Factor>)`
- **Prescribed Treatment**: `(RequiresTreatment <Plant> <Intervention>)`

---

## 4. PLN Mathematical Model

PLN models uncertainty using second-order probability distributions over truth values. Rather than relying on scalar fuzzy weights or heuristic certainty factors, PLN associates every proposition with a beta distribution characterized by:
- Expected mean/mode probability: **Strength** $s \in [0, 1]$.
- Equivalent weight of evidence count: $w \in [0, \infty)$.
- Normalized degree of certainty: **Confidence** $c \in [0, 1)$.

---

## 5. Truth Values & Conversions

Confidence is related to evidence weight $w$ via the Jeffreys prior lookahead formula ($k=1.0$):
$$c = \frac{w}{w + 1} \iff w = \frac{c}{1 - c}$$
In `metta/core/pln_tv.metta`:
```metta
(: Truth_c2w (-> Number Number))
(= (Truth_c2w $c) (/safe $c (- 1.0 (min $c 0.999999))))

(: Truth_w2c (-> Number Number))
(= (Truth_w2c $w) (/safe $w (+ $w 1.0)))
```
Truth value bounds are strictly enforced: $s \in [0.0, 1.0]$, $c \in [0.0, 0.999999]$.

---

## 6. Deduction

Deduction infers $P \to R$ from $P \to Q$ and $Q \to R$:
$$s = s_1 \cdot s_2, \quad c = (s_1 \cdot s_2) \cdot (c_1 \cdot c_2)$$
The system also implements the full 5-argument formula from `lib_pln.metta` incorporating marginal priors and conditional probability consistency checks.

---

## 7. Induction

Induction generalizes a connection between two predicates sharing a subject:
$$B \to A \ (\text{stv } s_{BA}\ c_{BA}), \quad B \to C \ (\text{stv } s_{BC}\ c_{BC}) \implies A \to C$$
$$s = s_{BA} \cdot s_{BC}, \quad w = s_{BC} \cdot c_{BC} \cdot c_{BA}, \quad c = \text{Truth\_w2c}(w)$$

---

## 8. Abduction

Abduction hypothesizes an explanation from shared consequents:
$$A \to B \ (\text{stv } s_{AB}\ c_{AB}), \quad C \to B \ (\text{stv } s_{CB}\ c_{CB}) \implies A \to C$$
$$s = s_{AB} \cdot s_{CB}, \quad w = s_{AB} \cdot c_{AB} \cdot c_{CB}, \quad c = \text{Truth\_w2c}(w)$$

---

## 9. Revision (Evidence Fusion & Conflict Resolution)

When multiple independent observers assess the same hypothesis $H$, PLN calculates the pooled evidence weight $w_{total} = w_1 + w_2$:
$$s_{rev} = \frac{s_1 w_1 + s_2 w_2}{w_1 + w_2}, \quad c_{rev} = \frac{w_{total}}{w_{total} + 1}$$
Conflicting evidence pulls $s$ towards the weighted mean while strictly increasing confidence $c_{rev} > \max(c_1, c_2)$.

---

## 10. Forward Chaining Engine

Implemented in `metta/chaining/fc.metta`:
- Takes an initial premise atom and a Peano natural number step bound `(S $k)`.
- Matches premises against binary rules (`rb`) and unary rules (`rb1`).
- Evaluates the corresponding PLN truth function.
- Accumulates reachable derived theorems into the output set.
- Guaranteed to terminate in finite steps.

---

## 11. Backward Chaining Engine

Implemented in `metta/chaining/bc.metta`:
- Begins with a target hypothesis atom and search depth bound.
- Employs **goal-directed implication lookup** to bind intermediate variables without combinatorial branching.
- Recursively proves subgoals, grounding them in knowledge base facts.
- Synthesizes transparent proof trees: `(Proof (⊢ <Concl> <TV>) (Rule <Name> <SubProof1> <SubProof2>))`.
- Bounded depth prevents infinite recursion on cyclic rules ($A \to B, B \to A$).

---

## 12. Coffee Agriculture Knowledge Base

Defined in `metta/kb/coffee_agriculture.metta`:
- Primary demonstration domain centered on coffee pathology (*Coffea arabica*).
- Pathogens modeled: Coffee Leaf Rust (*Hemileia vastatrix*), Coffee Berry Disease (*Colletotrichum kahawae*), Nitrogen Chlorosis.
- Environmental risks: HighHumidity, HeavyRainfall, DenseShadedCanopy.
- Treatment protocols: CopperFungicideSpray, TargetedBerryFungicide, NitrogenFertilizer, CanopyPruning.
- Unified representation: powers **both** Forward Chaining and Backward Chaining without modification.

---

## 13. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Streamlit Web Demonstration                 │
│   • Goal-Directed BC    • Data-Driven FC    • PLN Revision  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    Python Integration Layer                 │
│   • PLNRunner (Runner State)      • Expression AST Parser   │
│   • Dataclass Models (TruthValue, ProofNode, QueryResult)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ from hyperon import MeTTa
┌──────────────────────────────▼──────────────────────────────┐
│              Core Native MeTTa Reasoning Engine              │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │     pln_tv.metta      │       │  pln_formulas.metta   │  │
│  └───────────────────────┘       └───────────────────────┘  │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │       nat.metta       │       │      rules.metta      │  │
│  └───────────────────────┘       └───────────────────────┘  │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │        bc.metta       │       │        fc.metta       │  │
│  └───────────────────────┘       └───────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     coffee_agriculture.metta (Primary Expert KB)      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 14. Python Integration Layer

Located in `src/pln_engine/`:
- `models.py`: Strongly typed dataclasses (`TruthValue`, `Statement`, `ProofNode`, `DerivationResult`, `QueryResult`).
- `parser.py`: Pure AST parser converting Hyperon `ExpressionAtom` objects into Python dataclasses.
- `runner.py`: Orchestrates `hyperon.MeTTa(env_builder=custom_env(...))` instances, loads MeTTa code, and passes queries.
- **Strict Compliance**: Zero semantic reasoning is implemented in Python; all mathematical formulas and search algorithms execute in MeTTa.

---

## 15. Streamlit Interface

Located in `streamlit_app/app.py`:
- Serves interactive demo on port `8501`.
- Modes:
  1. Backward Chaining diagnosis with explainable resolution traces.
  2. Forward Chaining symptom progression.
  3. Conflicting Evidence Resolution tool (PLN Revision).
  4. Interactive MeTTa REPL for arbitrary expression evaluation.
- All actions execute live inside official Hyperon 0.2.10.

---

## 16. Experimental Results

1. **Coffee Leaf Rust Treatment Query**:
   - Query: `(RequiresTreatment CoffeePlant01 CopperFungicideSpray)`
   - Derived STV: $(s=0.7715, c=0.4525)$
   - Execution Time: $\sim 65\text{ ms}$
   - Proof Tree: 2 sequential Modus Ponens applications connecting symptom $\to$ rust $\to$ fungicide.
2. **Conflicting Evidence Scenario**:
   - Scout A ($s=0.85, c=0.75$) vs. Scout B ($s=0.20, c=0.70$)
   - Fused STV: $(s=0.5656, c=0.8421)$
   - Demonstrates balanced probability and elevated confidence.

---

## 17. Test Results

Comprehensive automated test suite executed via `./run_tests.sh`:
- **50 / 50 Tests Passed (100%)** in $54.27\text{ seconds}$.
- Coverage spans:
  - Truth value bounds and weight conversions.
  - Deduction, Induction, Abduction, and Revision.
  - Forward chaining semantics (Tests 1–9).
  - Backward chaining semantics (Cases A–G).
  - Coffee agriculture domain pathways.
  - Negative cases (missing facts, cycles, unknown entities, depth cutoffs).
  - Python-MeTTa integration pipelines and serialization.

---

## 18. Limitations

1. **Host Environment**: System Python 3.14 lacks prebuilt wheels on PyPI; isolated Python 3.12 is required.
2. **Search Depth Scale**: Depth limit is bounded to $k \le 4$ in interactive mode to maintain sub-second response times on broad knowledge bases.
3. **Priors in Chaining**: Operational chaining assumes unconditioned base-rate defaults rather than maintaining global joint probability distributions over all atoms.

---

## 19. Official Implementation Comparison

Documented in detail in `docs/official-audit.md`:
- Engine: Official `hyperon==0.2.10` runtime.
- Truth Values: Exactly matches `lib_pln.metta` and `TruthValue.metta`.
- Rules: Uses explicit `(rule <name> ...)` tags to construct readable proof DAGs.
- Domain: Grounded in real coffee plant pathology rather than synthetic toy problems.

---

## 20. Conclusion

The project delivers an authentic, reproducible, mentor-ready Probabilistic Logic Network reasoning system. Core reasoning, truth-value formulas, and proof tree generation are 100% native MeTTa. Python and Streamlit serve strictly as integration and demonstration layers. All 50 semantic and integration tests pass, and the system is fully documented and reproducible.
