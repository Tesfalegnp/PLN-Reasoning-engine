# PLN Reasoning Engine (MeTTa)

An Agricultural Probabilistic Logic Networks (PLN) Reasoning Engine implemented natively in **MeTTa**.

## 📄 Project Documentation & Assignment Reference

- **Google Doc Reference**: [PLN Assignment Specification Document](https://docs.google.com/document/d/1cRyR6_VnUUaCqpUK_zMV-wEJRtUPpCzXUz8wXynibrw/edit?usp=sharing)
- **Technical Report**: [`docs/technical_report.md`](file:///home/hope/project_2/pln-engine/docs/technical_report.md)

---

## 🏗️ Project Architecture

```
pln-engine/
├── docs/
│   └── technical_report.md          # Comprehensive technical report
├── engine/
│   ├── pln.metta                    # Core PLN formulas (deduction, induction, abduction, revision)
│   ├── forward_chain.metta          # Forward chaining inference engine
│   └── backward_chain.metta         # Backward chaining proof generator
├── knowledge/
│   ├── agriculture.metta            # Domain facts with Subjective Truth Values (STVs)
│   └── rule.metta                   # Agricultural inference rules
├── test/
│   ├── test_fact_stv.metta          # Fact & STV lookup tests
│   ├── test_deduction.metta         # Deduction & rule-chaining tests
│   ├── test_revision.metta          # Revision formula tests
│   ├── test_forward_chaining.metta  # Forward chaining tests
│   ├── test_backward_chaining.metta # Backward chaining proof tests
│   ├── test_full_scenario.metta     # Full scenario integration tests
│   ├── test_evaluation_scenarios.metta # 5 PDF evaluation scenarios
│   └── test_agriculture.metta       # Master integration test suite
├── app.py                           # Interactive Desktop GUI Dashboard
└── README.md                        # Quick start guide & documentation
```

---

## ✨ Features

- **PLN Truth Values (STVs)**: Formulated with strength and confidence `(stv strength confidence)`.
- **Four PLN Calculus Operations**: Deduction, Induction, Abduction, and Revision.
- **Bidirectional Reasoning**: Data-driven Forward Chaining and Goal-driven Backward Chaining proof tree generation.
- **Agricultural Domain KB**: Soil dryness, temperature, crop stress, resource availability, and disease detection.

---

## 🧪 Running Tests

Run any test suite using MeTTa:

```bash
# Run the evaluation scenarios matching PDF requirements
metta test/test_evaluation_scenarios.metta

# Run the master test suite
metta test/test_agriculture.metta
```

---

## 🖥️ Running the Interactive Dashboard

Launch the GUI dashboard:

```bash
python app.py
```
