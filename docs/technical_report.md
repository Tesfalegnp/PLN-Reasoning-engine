# Technical Report: Agricultural Probabilistic Logic Network (PLN) Engine in MeTTa

## 1. Domain Selection & Problem Definition
In precision agriculture, automated diagnostic systems face radical uncertainty: sensor measurements (e.g., soil moisture, ambient temperature) are noisy, disease symptoms overlap across different pathologies, and environmental conditions fluctuate dynamically. 

Standard binary logic fails in this environment because it cannot weigh confidence or resolve conflicting evidence. This project implements a **Probabilistic Logic Network (PLN)** engine natively in **MeTTa** to model uncertainty, perform multi-hop causal reasoning, and infer optimal crop management actions (e.g., irrigation scheduling and disease treatment).

---

## 2. Knowledge Base Architecture & STV Representation
The Knowledge Base ([`knowledge/agriculture.metta`](file:///home/hope/project_2/pln-engine/knowledge/agriculture.metta)) represents domain facts and rules using **Subjective Truth Values (STV)**:
$$\text{STV} = (\text{stv } s \;\; c)$$
- **Strength ($s \in [0, 1]$)**: The degree of truth of a statement or rule.
- **Confidence ($c \in [0, 1]$)**: The weight of evidence supporting that truth estimate.

### Sample Knowledge Topology
- **F1 (Soil Dryness)**: `(: F1 (soil-dry) (stv 0.90 0.90))`
- **F2 (High Temperature)**: `(: F2 (temperature-high) (stv 0.85 0.88))`
- **Rule R1**: `(: R1 (implication (and (soil-dry) (temperature-high)) (coffee-plant-water-stressed)) (stv 0.92 0.85))`

---

## 3. Implementation of the 4 PLN Inference Rules
The PLN calculus is implemented in [`engine/pln.metta`](file:///home/hope/project_2/pln-engine/engine/pln.metta) with formulas calculating both Strength ($s$) and Confidence ($c$):

1. **Deduction**: Combines premises to derive forward conclusions.
   $$\text{deduction}(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle) = \langle s_1 \cdot s_2, \; c_1 \cdot c_2 \rangle$$
2. **Induction**: Generalizes shared properties across observations.
   $$\text{induction}(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle) = \left\langle \frac{s_1 + s_2}{2}, \; c_1 \cdot c_2 \right\rangle$$
3. **Abduction**: Inferring plausible underlying causes from observed effects.
   $$\text{abduction}(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle) = \langle s_1 \cdot s_2, \; c_1 \cdot c_2 \rangle$$
4. **Revision**: Aggregates conflicting or independent pieces of evidence.
   $$\text{revision}(\langle s_1, c_1 \rangle, \langle s_2, c_2 \rangle) = \left\langle \frac{s_1 c_1 + s_2 c_2}{c_1 + c_2}, \; \frac{c_1 + c_2}{2} \right\rangle$$

---

## 4. Chaining Search Strategies
Both reasoning search directions run over the same underlying domain Knowledge Base:

1. **Forward Chaining (Data-Driven)**:
   - Implemented in [`engine/forward_chain.metta`](file:///home/hope/project_2/pln-engine/engine/forward_chain.metta).
   - Starts with active sensor observations (e.g., `soil-dry`) and fires matching rules forward to uncover derived crop stress states and recommended actions.
2. **Backward Chaining (Goal-Driven)**:
   - Implemented in [`engine/backward_chain.metta`](file:///home/hope/project_2/pln-engine/engine/backward_chain.metta).
   - Starts from a target query (e.g., `(irrigate-coffee-plant)`) and recursively unwinds sub-goals to construct full hierarchical proof trees linking base facts to the target goal.

---

## 5. System Evaluation & Scenario Analysis
The system was evaluated against 5 domain scenarios ([`test/test_evaluation_scenarios.metta`](file:///home/hope/project_2/pln-engine/test/test_evaluation_scenarios.metta)):

1. **Scenario 1 (Supported Conclusion)**: `soil-dry` $\times$ `temperature-high` yields `water-stressed` with STV $\langle 0.765, 0.792 \rangle$.
2. **Scenario 2 (Uncertain Evidence)**: Low confidence sensor ($\langle 0.60, 0.35 \rangle$) yields low confidence conclusion ($\langle 0.42, 0.14 \rangle$).
3. **Scenario 3 (Multiple Explanations)**: Abduction distinguishes Coffee Leaf Rust ($\langle 0.686, 0.576 \rangle$) from Nutrient Deficiency.
4. **Scenario 4 (Revision)**: Merges conflicting sensor readings ($\langle 0.90, 0.90 \rangle$ and $\langle 0.40, 0.85 \rangle$) into a updated STV $\langle 0.657, 0.875 \rangle$.
5. **Scenario 5 (Confidence Decay)**: Multi-hop reasoning (3-hop proof) demonstrates natural confidence decay across chaining depth.

---

## 6. Limitations & Future Work
- **Combinatorial Expansion**: Deep backward chaining depth ($>4$ hops) can produce redundant proof paths; integrating Economic Attention Networks (ECAN) for heuristic STI allocation will prune search spaces.
- **Dynamic STV Learning**: STVs are currently configured from domain expertise; future work will incorporate automated STV learning from historical agricultural dataset streams.
