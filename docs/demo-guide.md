# Demonstration & Evaluation Guide — Coffee Agriculture PLN Reasoner

This guide provides step-by-step instructions for running and evaluating the MeTTa Probabilistic Logic Network (PLN) reasoning system on coffee agriculture plant pathology.

---

## 1. Quick Environment Setup

```bash
# Enter project directory
cd /home/hope/Projects/pln_engin_project

# Provision isolated Python 3.12 environment using uv
uv python install 3.12
uv venv .venv-metta --python 3.12
source .venv-metta/bin/activate

# Install required dependencies
uv pip install -p .venv-metta hyperon streamlit pytest
```

---

## 2. Running Automated Verification Suite

Execute the single-command regression suite:
```bash
./run_tests.sh
```
Expected output:
```text
====================================================================
Coffee Agriculture PLN Reasoning System — Verification Suite
====================================================================
...
1. Running Native MeTTa Script Verifications...
  ✓ Core MeTTa formulas test passed.
  ✓ 4-operation Agricultural PLN demo executed successfully.
  ✓ Agricultural Forward Chaining executed successfully.
  ✓ Agricultural Backward Chaining executed successfully.
  ✓ Agricultural Conflicting Evidence Revision executed successfully.

2. Running Comprehensive Pytest Suite (Domain, Semantic & Negatives)...
======================== 50 passed in 95.86s (0:01:35) =========================
====================================================================
ALL TESTS PASSED! System is 100% verified and reproducible.
====================================================================
```

---

## 3. Starting the Streamlit Demonstration UI

Launch the expert reasoning dashboard:
```bash
.venv-metta/bin/streamlit run streamlit_app/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 4. Step-by-Step Interactive Demonstrations

### Demo 1: Goal-Directed Diagnosis (Backward Chaining)
1. In the sidebar, select **Reasoning Strategy**: `Backward Chaining (Goal-Directed Diagnosis)`.
2. Ensure **Peano Search Depth** is set to `2`.
3. Choose the preset:
   ```text
   (RequiresTreatment CoffeePlant01 CopperFungicideSpray)
   ```
4. Click **🚀 Execute MeTTa Engine**.
5. **Observed Output**:
   - Status: Goal Proven in $< 100\text{ ms}$.
   - Simple Truth Value: Strength $\approx 0.7715$, Confidence $\approx 0.4525$, Evidence Weight $w \approx 0.83$.
   - **Reasoning Trace card** showing the diagnostic detachment.
   - **MeTTa Proof Tree Structure** displaying the recursive resolution:
     `Fact (HasSymptom CoffeePlant01 OrangeRustPustules)` $\to$ `Rule ded` $\to$ `Rule mp`.

### Demo 2: Data-Driven Symptom Progression (Forward Chaining)
1. Select **Reasoning Strategy**: `Forward Chaining (Data-Driven Progression)`.
2. Choose preset observation:
   ```text
   (HasSymptom CoffeePlant01 OrangeRustPustules)
   ```
3. Set Strength to `0.88`, Confidence to `0.85`, and Depth to `2`.
4. Click **🚀 Run Forward Chaining**.
5. **Observed Output**:
   - Derived 3 distinct facts:
     1. `(HasSymptom CoffeePlant01 OrangeRustPustules)` $(s=0.88, c=0.85)$
     2. `(AfflictedWith CoffeePlant01 CoffeeLeafRust)` $(s=0.8384, c=0.6395)$
     3. `(RequiresTreatment CoffeePlant01 CopperFungicideSpray)` $(s=0.7746, c=0.4341)$

### Demo 3: Conflicting Field Scout Evidence (PLN Revision)
1. Select **Reasoning Strategy**: `Conflicting Evidence Resolution (PLN Revision)`.
2. Adjust the observer sliders:
   - **Scout A (Observed rust symptoms)**: $s_1 = 0.85, c_1 = 0.75$ ($w_1 = 3.00$).
   - **Scout B (Disputes rust symptoms)**: $s_2 = 0.20, c_2 = 0.70$ ($w_2 = 2.33$).
3. **Observed Output**:
   - Pooled Strength $s = 0.5656$ (weighted compromise between observers).
   - Pooled Confidence $c = 0.8421$ ($+0.0921$ higher than the best single scout).
   - Demonstrates that independent evidence accumulation increases confidence even under conflicting hypotheses.

### Demo 4: Compare Forward vs Backward Chaining
1. Select **Reasoning Strategy**: `Compare Forward vs Backward Chaining`.
2. Click **Run Forward Comparison** and **Run Backward Comparison**.
3. **Observed Output**:
   - Both forward data-driven exploration and backward goal-directed search operate over the **same** knowledge base (`coffee_agriculture.metta`) and deduce equivalent treatment recommendations with matching truth value parameters.

---

## 5. Direct Native MeTTa CLI Execution

To verify that the engine runs 100% inside native MeTTa without Python:
```bash
# 1. Four PLN Operations Demo (Deduction, Induction, Abduction, Revision)
.venv-metta/bin/metta examples/agriculture_pln_demo.metta

# 2. Forward Chaining Demo
.venv-metta/bin/metta examples/agriculture_forward.metta

# 3. Backward Chaining Proof Tree Demo
.venv-metta/bin/metta examples/agriculture_backward.metta

# 4. Conflicting Evidence Revision Demo
.venv-metta/bin/metta examples/agriculture_revision.metta
```
