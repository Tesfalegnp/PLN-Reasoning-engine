# 5–10 Minute Mentor Presentation Script

**Project**: Probabilistic Logic Network (PLN) Reasoning System in MeTTa  
**Domain**: Coffee Agriculture & Agronomic Plant Pathology  

---

## Presentation Sequence

### Step 1: Explain the Architecture (1 minute)
- **Point**: "Our system implements Probabilistic Logic Networks natively in MeTTa using the official TrueAGI Hyperon 0.2.10 engine. Python is strictly an integration bridge; all reasoning logic, truth-value calculations, and proof trees execute in MeTTa."
- **Visual**: Show architecture diagram in `README.md`.

### Step 2: Show the Simple Truth Value (STV) Model (30 seconds)
- **Point**: "Unlike fuzzy logic or heuristic confidence scores, PLN models uncertainty as a second-order beta distribution characterized by probability strength $s \in [0, 1]$ and confidence $c \in [0, 1)$. Confidence translates to evidence weight via $w = c / (1 - c)$."
- **Reference**: `metta/core/pln_tv.metta`.

### Step 3: Run Native MeTTa PLN Deduction (1 minute)
- **Point**: "Let's run `examples/pln_demo.metta` directly in the MeTTa CLI binary without Python."
- **Action**: Run `.venv-metta/bin/metta examples/pln_demo.metta`.
- **Highlight**: Point out `(stv 0.7200 0.4590)` derived from premises $(0.90, 0.85)$ and $(0.80, 0.75)$.

### Step 4: Run Coffee Disease Forward Chaining (1 minute)
- **Point**: "Now in Streamlit at `http://localhost:8501`, we select Forward Chaining. Given a seed field observation that `CoffeePlant01` has `OrangeRustPustules` $(s=0.88, c=0.85)$, our engine steps forward through agronomic rules."
- **Action**: Click 'Run Forward Chaining'.
- **Result**: Derives both the disease `CoffeeLeafRust` and the treatment protocol `CopperFungicideSpray`.

### Step 5: Run Coffee Disease Backward Chaining (1 minute)
- **Point**: "Now let's verify goal-directed diagnosis. Suppose an agronomist asks: 'Does CoffeePlant01 require CopperFungicideSpray?'"
- **Action**: In Backward Chaining mode, execute `(RequiresTreatment CoffeePlant01 CopperFungicideSpray)`.
- **Result**: Derives the treatment with $s=0.7715, c=0.4525$ in under $70\text{ ms}$.

### Step 6: Show the Recursive Proof Trace (1 minute)
- **Point**: "Crucially, the answer is explainable. The engine didn't just return a number; it synthesized a complete proof tree in MeTTa."
- **Visual**: Show the proof tree expanding from goal $\to$ Modus Ponens $\to$ subgoals $\to$ field observation fact.

### Step 7: Demonstrate Conflicting Evidence Handling (1 minute)
- **Point**: "In real farming, scouts often disagree. Scout A reports visible rust pustules $(s=0.85, c=0.75)$, while Scout B reports clean foliage $(s=0.20, c=0.70)$. Classical logic breaks, but PLN Revision pools evidence weights ($w_1 = 3.0, w_2 = 2.33$). The result is a balanced probability ($s=0.5656$) and higher confidence ($c=0.8421$)."
- **Action**: Adjust sliders in the 'Conflicting Evidence Resolution' tab and show real-time MeTTa calculation.

### Step 8: Demonstrate Python Integration Boundaries (1 minute)
- **Point**: "Notice that `src/pln_engine/runner.py` only manages the Hyperon environment, and `parser.py` only converts ASTs. No semantic reasoning was implemented in Python."
- **Reference**: `src/pln_engine/runner.py`.

### Step 9: Show Interactive Streamlit Features (30 seconds)
- **Point**: "The Streamlit UI supports Backward Chaining, Forward Chaining, Evidence Revision, and an interactive MeTTa REPL."

### Step 10: Run the Full Automated Test Suite (1 minute)
- **Action**: Run `./run_tests.sh`.
- **Highlight**: "50 out of 50 unit, semantic, negative, and integration tests pass cleanly in 54 seconds."
- **Conclusion**: "The system is fully implemented, mathematically sound, native to MeTTa, and completely reproducible."
