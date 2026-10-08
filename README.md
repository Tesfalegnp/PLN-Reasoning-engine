# PLN Reasoning Engine (MeTTa)

An Agricultural Probabilistic Logic Networks (PLN) Reasoning Engine implemented natively in **MeTTa**.

## Project Architecture

```
├── engine/
│   ├── pln.metta             # Core PLN formulas (deduction, revision)
│   ├── forward_chain.metta   # Forward chaining inference engine
│   └── backward_chain.metta  # Backward chaining proof generator
├── knowledge/
│   ├── agriculture.metta     # Domain facts with Subjective Truth Values (STVs)
│   └── rule.metta            # Agricultural inference rules
├── test/
│   └── test_agriculture.metta # Comprehensive test suite
├── FrontEnd.py               # Interactive Streamlit Dashboard UI
```

## Features

- **PLN Truth Values (STVs)**: Formulated with strength and confidence `(stv strength confidence)`.
- **Reasoning Rules**: Deduction, Revision, Forward Chaining, and Backward Proof Generation.
- **Agricultural Domain KB**: Soil dryness, temperature, crop stress, and disease detection.

## Running Tests

Run the test suite using MeTTa:

```bash
metta test/test_agriculture.metta
```

## Running the Dashboard

Launch the interactive UI:

```bash
streamlit run FrontEnd.py
```
