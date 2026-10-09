# PLN Reasoning Engine for Agriculture (MeTTa)

An Agricultural Probabilistic Logic Networks (PLN) Reasoning Engine implemented natively in **MeTTa**, designed to represent agricultural knowledge, reason under uncertainty, and generate conclusions from facts and inference rules.

## 📄 Project Documentation and Assignment Reference

* **Google Docs – PLN Assignment Specification:** [Open Assignment Specification](https://docs.google.com/document/d/1cRyR6_VnUUaCqpUK_zMV-wEJRtUPpCzXUz8wXynibrw/edit?usp=sharing)
* **Technical Report:** [`docs/technical_report.md`](docs/technical_report.md)

The assignment specification provides the reference for the project's requirements and evaluation scenarios. The technical report documents the system's design, implementation, reasoning methods, and agricultural application.

## 🌱 Project Overview

The PLN Reasoning Engine applies Probabilistic Logic Networks concepts to agricultural knowledge. It represents facts with **Subjective Truth Values (STVs)** and uses inference rules to derive conclusions or generate possible explanations.

The system is implemented using MeTTa and includes core reasoning operations, forward chaining, backward chaining, an agricultural knowledge base, test scenarios, and an interactive Python desktop dashboard.

The agricultural domain includes concepts related to soil moisture, temperature, rainfall, coffee plant water stress, irrigation, and possible coffee leaf rust.

## 🏗️ Project Architecture

```text
pln-engine/
├── docs/
│   └── technical_report.md
│
├── engine/
│   ├── pln.metta
│   ├── forward_chain.metta
│   └── backward_chain.metta
│
├── knowledge/
│   ├── agriculture.metta
│   └── rule.metta
│
├── test/
│   ├── test_fact_stv.metta
│   ├── test_deduction.metta
│   ├── test_revision.metta
│   ├── test_forward_chaining.metta
│   ├── test_backward_chaining.metta
│   ├── test_full_scenario.metta
│   ├── test_evaluation_scenarios.metta
│   └── test_agriculture.metta
│
├── app.py
└── README.md
```

### Directory and File Descriptions

**`engine/` — Reasoning Engine**

* `pln.metta`: Defines the core truth-value operations: deduction, induction, abduction, and revision.
* `forward_chain.metta`: Defines forward-chaining logic for exploring conclusions from available facts and inference rules.
* `backward_chain.metta`: Defines backward-chaining logic for examining whether a target conclusion can be supported by available rules and premises.

**`knowledge/` — Agricultural Knowledge Base**

* `agriculture.metta`: Contains agricultural facts and their associated Subjective Truth Values.
* `rule.metta`: Contains inference rules connecting premises to possible conclusions.

**`test/` — Testing and Evaluation**

Contains tests for truth-value lookup, individual reasoning operations, forward and backward chaining, integrated reasoning scenarios, and the agricultural evaluation scenarios.

**`app.py` — Interactive Dashboard**

Provides a desktop interface for interacting with the reasoning engine, selecting reasoning operations, and inspecting their results.

**`docs/technical_report.md` — Technical Documentation**

Provides a more detailed description of the project's implementation and reasoning approach.

## ✨ Main Features

### 1. Subjective Truth Values (STVs)

Each fact can be associated with a Subjective Truth Value represented as:

```metta
(stv strength confidence)
```

* **Strength:** Represents the degree to which a proposition is considered true.
* **Confidence:** Represents the confidence associated with that strength estimate.

For example:

```metta
(: F1 (soil-dry) (stv 0.90 0.90))
```

This represents the agricultural fact `soil-dry` with strength `0.90` and confidence `0.90`.

### 2. Four PLN Reasoning Operations

The core reasoning operations are defined in `engine/pln.metta`.

* **Deduction:** Derives a conclusion using the truth values of supporting premises.
* **Induction:** Estimates a broader relationship from the truth values of related observations.
* **Abduction:** Evaluates a possible explanation for an observed fact.
* **Revision:** Combines two truth-value estimates for the same proposition to produce an updated estimate.

These operations allow the engine to work with uncertain agricultural knowledge instead of treating every fact as simply true or false.

### 3. Forward Chaining

Forward chaining starts from known facts and explores rules whose premises can be supported by those facts. It is intended to help identify conclusions that follow from the available agricultural knowledge.

### 4. Backward Chaining

Backward chaining starts from a target goal and examines rules and premises that could support it. This provides a goal-directed way to explore the reasoning behind a possible conclusion.

### 5. Agricultural Knowledge Representation

The knowledge base represents agricultural conditions and observations, including:

* Soil dryness
* High temperature
* Low rainfall
* Coffee plant water stress
* Coffee leaf wilting
* Water availability
* Farmer irrigation capability
* Orange spots on coffee leaves
* Humidity conditions favorable to leaf rust

These facts are connected through the inference rules defined in `knowledge/rule.metta`.

### 6. Interactive Desktop Dashboard

The Python dashboard provides an interface for running the reasoning engine without manually entering every MeTTa query.

The dashboard can be used to inspect facts, select reasoning operations, and review the resulting outputs. The exact functionality available depends on the current implementation in `app.py`.

## ⚙️ Requirements

The project requires:

* Python 3
* MeTTa / Hyperon runtime
* The Python `hyperon` package providing the MeTTa runtime
* A terminal for running tests and commands
* Tkinter, if it is used by the desktop dashboard and is not already installed

Confirm that MeTTa is available in your environment before running the test files.

Check Python:

```bash
python3 --version
```

Check MeTTa:

```bash
metta --version
```

If your environment uses a virtual environment, activate it before running the dashboard or tests.

## 🚀 Getting Started

### 1. Open the Project Directory

Navigate to the project root:

```bash
cd /path/to/pln-engine
```

Replace `/path/to/pln-engine` with the actual path to your project directory.

### 2. Verify the Project Structure

Check that the required directories and files exist:

```bash
ls
ls engine
ls knowledge
ls test
```

### 3. Verify the Knowledge Base

Review the agricultural facts:

```bash
cat knowledge/agriculture.metta
```

Review the inference rules:

```bash
cat knowledge/rule.metta
```

Review the reasoning operations:

```bash
cat engine/pln.metta
```

## 🧪 Running Tests

Run the tests from the project root so that the relative file paths and imports behave as expected.

### Run Agricultural Evaluation Scenarios

```bash
metta test/test_evaluation_scenarios.metta
```

### Run the Master Integration Test Suite

```bash
metta test/test_agriculture.metta
```

### Test Individual Components

Fact and STV lookup:

```bash
metta test/test_fact_stv.metta
```

Deduction:

```bash
metta test/test_deduction.metta
```

Revision:

```bash
metta test/test_revision.metta
```

Forward chaining:

```bash
metta test/test_forward_chaining.metta
```

Backward chaining:

```bash
metta test/test_backward_chaining.metta
```

Full scenario:

```bash
metta test/test_full_scenario.metta
```

**Note:** These commands run the named test files. Successful execution and correct results should be confirmed from the actual output; listing a test command does not itself establish that the tests pass.

## 🖥️ Running the Interactive Dashboard

From the project root, run:

```bash
python3 app.py
```

If your environment uses `python` rather than `python3`, you can also run:

```bash
python app.py
```

The dashboard is intended to provide a graphical interface to the MeTTa reasoning engine. If it fails to start, check that the required Python packages are installed and that the project files can be found from the current working directory.

## 🔍 Example Agricultural Reasoning Scenario

Consider the following facts in the agricultural knowledge base:

```metta
(: F1 (soil-dry) (stv 0.90 0.90))
(: F2 (temperature-high) (stv 0.85 0.88))
```

An inference rule connects these premises to a possible conclusion:

```metta
(: R1
   (rule
      (soil-dry)
      (temperature-high)
      (coffee-plant-water-stressed)
      (stv 0.92 0.85)))
```

The engine can use the premise truth values and the deduction operation to calculate a candidate truth value for the conclusion. The rule's own truth value is part of the rule's knowledge representation; it should not be assumed to be incorporated into the calculation unless the implementation explicitly applies it.

This scenario illustrates how agricultural observations can be combined to reason about a coffee plant's possible water stress. The resulting conclusion is an inference, not a substitute for field measurements or professional agricultural assessment.

## 🧠 How the Components Work Together

The system's reasoning workflow can be summarized as follows:

1. **Load agricultural facts:** Read the facts and their STVs from the agricultural knowledge base.
2. **Load inference rules:** Read the rules that connect premises with possible conclusions.
3. **Load PLN operations:** Make the defined truth-value operations available to the MeTTa runtime.
4. **Run reasoning:** Apply an operation to selected truth values or explore rules through forward or backward chaining.
5. **Inspect results:** Review the computed truth values, inferred conclusions, or generated proof structure.
6. **Evaluate behavior:** Run the relevant test files and compare their output with the expected evaluation scenarios.

The distinction between truth-value calculations and rule traversal is important: a chaining procedure that explores rules does not necessarily calculate and propagate STVs through every step. That behavior depends on the implemented MeTTa definitions.

## 📚 Technical Notes and Limitations

* The project's core PLN operations use the formulas implemented in `engine/pln.metta`. These should be understood as the project's current implementation rather than assumed to be a complete implementation of every canonical PLN formulation.
* The quality of an inferred conclusion depends on the facts, their STVs, and the rules available in the knowledge base.
* The dashboard should display values obtained from the actual knowledge base and reasoning runtime rather than presenting hardcoded values as calculated results.
* Forward chaining and backward chaining should be evaluated according to their actual implementations and test outputs.
* The project is a reasoning-engine prototype for agricultural knowledge. Its conclusions should be interpreted in the context of the available rules and evidence.

## 🛠️ Troubleshooting

### MeTTa Command Not Found

If the terminal reports that `metta` is not found, verify the MeTTa installation and ensure its executable directory is included in your `PATH`.

```bash
which metta
```

### Python Cannot Import `hyperon`

If the dashboard reports that the `hyperon` module is missing, activate the intended Python environment and install or configure the compatible Hyperon package for that environment.

### Files Cannot Be Found

Run commands from the project root:

```bash
cd /path/to/pln-engine
```

Check that the expected files exist:

```bash
ls engine/pln.metta
ls knowledge/agriculture.metta
ls knowledge/rule.metta
```

### A Test Produces Unexpected Results

Inspect the relevant test file, the corresponding MeTTa definitions, and the knowledge-base entries. Verify the actual output rather than assuming that every operation or chaining method propagates STVs in the same way.

## 🎯 Project Objectives

The project aims to demonstrate how MeTTa can be used to represent uncertain agricultural knowledge, implement probabilistic reasoning operations, connect facts through inference rules, and provide an interface for exploring reasoning results.

It also provides a foundation for testing agricultural reasoning scenarios and extending the knowledge base with additional facts and rules.

## 📌 Conclusion

The PLN Reasoning Engine combines MeTTa-based knowledge representation, truth-value operations, agricultural inference rules, forward and backward reasoning, and an interactive Python dashboard.

By keeping facts, rules, inference logic, and evaluation tests in separate components, the project provides a structured foundation for experimenting with uncertain knowledge and explainable agricultural reasoning.

For implementation details, consult [`docs/technical_report.md`](docs/technical_report.md). For the evaluation requirements, consult the [PLN Assignment Specification Document](https://docs.google.com/document/d/1cRyR6_VnUUaCqpUK_zMV-wEJRtUPpCzXUz8wXynibrw/edit?usp=sharing).
