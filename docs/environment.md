# Runtime Environment & Dependency Specifications

**Project**: Probabilistic Logic Network (PLN) Reasoning System in MeTTa  
**Generated On**: October 6, 2026  
**Auditor**: Antigravity MeTTa/PLN Engineering System  

---

## 1. Operating System Details

```bash
$ uname -a
Linux hope-laptop 7.0.0-34-generic #34-Ubuntu SMP PREEMPT_DYNAMIC Wed Sep  2 14:29:37 UTC 2026 x86_64 GNU/Linux
```

- **Distribution**: Ubuntu Linux x86_64
- **Host Architecture**: `x86_64`
# MASTER FINALIZATION PROMPT — COMPLETE PHASES 6 THROUGH 14

The previous Phase 6 audit produced a strong implementation and reports **PASS**, but I do NOT want to stop at Phase 6.

Now continue the project systematically through **PHASE 14**, using the existing implementation as the starting point.

The final objective is to deliver a **fully integrated, tested, reproducible, mentor-ready PLN + MeTTa + Hyperon + Forward Chaining + Backward Chaining + Python + Streamlit project**.

Do NOT restart the project.

Do NOT unnecessarily redesign working components.

Do NOT add features merely for appearance.

Do NOT declare completion until every phase below has been actually executed and verified.

The final project must be technically defensible in front of a mentor/evaluator.

---

# GLOBAL RULES FOR PHASES 6–14

## RULE 1 — ACTUAL EXECUTION ONLY

Never claim that something works because:

- code looks correct
- pytest passes partially
- an implementation resembles official code
- a README says it works
- a previous report says it works

Actually execute it.

If something fails:

```text
FAILED
Reason
Evidence
Impact
Fix
Retest result
```

Never hide failures.

---

# RULE 2 — OFFICIAL SOURCE REMAINS THE REFERENCE

Continue using the actual current official repositories:

- https://github.com/trueagi-io
- https://github.com/trueagi-io/hyperon-experimental
- https://github.com/trueagi-io/chaining
- https://github.com/trueagi-io/chaining/tree/main/experimental/backward-chaining
- https://github.com/trueagi-io/chaining/tree/main/experimental/forward-chaining
- https://github.com/trueagi-io/pln

Do not blindly copy them.

Use them to:

1. understand semantics
2. compare implementation
3. identify differences
4. justify project-specific extensions
5. correct mistakes

---

# RULE 3 — CORE REASONING MUST REMAIN MEttA-NATIVE

The architecture must remain:

```text
                STREAMLIT
                    |
                    v
             PYTHON INTERFACE
                    |
                    v
              HYPERON / MeTTa
                    |
          +---------+---------+
          |         |         |
          v         v         v
         PLN       BC        FC
          |         |         |
          +---------+---------+
                    |
                    v
             RESULT / PROOF
```

Python is the integration/orchestration layer.

Python must NOT become a replacement for:

- PLN deduction
- PLN induction
- PLN abduction
- PLN revision
- forward chaining
- backward chaining

If Python code currently performs semantic reasoning independently, identify it and refactor it.

---

# RULE 4 — SAME KNOWLEDGE BASE

Forward and backward chaining must operate on the same logical domain knowledge.

The main demonstration domain must be:

```text
Coffee Agriculture / Coffee Plant Disease Reasoning
```

The same:

```text
metta/kb/coffee_agriculture.metta
```

must support both:

```text
Forward Chaining
Backward Chaining
PLN reasoning
```

---

# RULE 5 — DO NOT FAKE RESULTS

All mathematical outputs, derivations, proof trees, confidence values, and demonstrations must come from actual execution.

Never hard-code:

```text
if query == "CoffeeLeafRust":
    return expected_result
```

Never create fake proof trees.

Never create fake test output.

---

# PHASE 6 — OFFICIAL SOURCE AUDIT AND CORRECTNESS VALIDATION

The previous Phase 6 report already performed much of this work.

Now independently verify the existing results before building further phases.

Inspect:

```text
docs/official-audit.md
docs/pln-examples.md
docs/final-validation-report.md
```

Verify the actual implementation of:

```text
metta/core/pln_tv.metta
metta/core/pln_formulas.metta

metta/chaining/nat.metta
metta/chaining/bc.metta
metta/chaining/fc.metta

metta/rules/rules.metta

metta/kb/coffee_agriculture.metta
```

Verify:

- STV representation
- strength range
- confidence range
- weight-of-evidence conversion
- deduction
- induction
- abduction
- revision
- negation
- conjunction/intersection
- modus ponens
- depth-bounded reasoning
- proof generation
- cycle termination

If the previous Phase 6 report contains an unsupported claim, correct it.

Do not simply trust:

```text
29/29 passed
PASS
```

Verify the underlying tests.

---

# PHASE 7 — COMPLETE AND VERIFY PLN ENGINE

Now make the PLN implementation fully coherent and demonstrable.

## 7.1 Truth Values

Verify:

```text
(stv strength confidence)
```

with:

```text
0 <= strength <= 1
0 <= confidence < 1
```

unless the official implementation proves otherwise.

Test:

```text
0
1
0.5
boundary values
invalid values
```

Verify weight conversions:

```text
w = c / (1-c)

c = w / (w+1)
```

Test numerical consistency.

---

## 7.2 Deduction

Verify actual deduction behavior.

Demonstrate:

```text
A -> B
B -> C
---------
A -> C
```

with STVs.

Show:

```text
premise 1
premise 2
formula
result
```

Do not simplify formulas unless the official source supports the simplification.

---

## 7.3 Induction

Demonstrate a real shared-subject induction example.

Document:

```text
Input
Formula
Execution
Output
Interpretation
```

---

## 7.4 Abduction

Demonstrate a real shared-conclusion abduction example.

Document:

```text
Input
Formula
Execution
Output
Interpretation
```

---

## 7.5 Revision

Demonstrate conflicting evidence:

```text
Evidence A
strength = 0.85
confidence = 0.75

Evidence B
strength = 0.20
confidence = 0.70
```

Run actual revision.

Record exact output.

Explain why the resulting STV changes.

---

## 7.6 Create a PLN Demonstration Script

Create:

```text
examples/pln_demo.metta
```

It must execute all four operations:

```text
Deduction
Induction
Abduction
Revision
```

The script must print clearly labeled results.

Run:

```bash
.venv-metta/bin/metta examples/pln_demo.metta
```

Record the actual output in:

```text
docs/pln-examples.md
```

---

# PHASE 8 — COMPLETE FORWARD CHAINING

Audit and improve:

```text
metta/chaining/fc.metta
```

It must genuinely perform data-driven reasoning.

Required flow:

```text
Known facts
    ↓
Match rules
    ↓
Evaluate premises
    ↓
Apply PLN truth-value formula
    ↓
Generate conclusion
    ↓
Add derived knowledge
    ↓
Continue
```

Test:

### Test 1

Direct fact.

### Test 2

One-step derivation.

### Test 3

Two-step derivation.

Example:

```text
HasSymptom
    ↓
AfflictedWith CoffeeLeafRust
    ↓
RequiresTreatment CopperFungicideSpray
```

### Test 4

Multiple rules.

### Test 5

Unavailable premise.

### Test 6

Duplicate derivation.

### Test 7

Cycle:

```text
A -> B
B -> A
```

### Test 8

Depth limit.

### Test 9

Truth-value propagation.

The result must depend on the actual premises.

Create:

```text
tests/test_forward_chaining_semantics.py
```

---

# PHASE 9 — COMPLETE BACKWARD CHAINING

Audit:

```text
metta/chaining/bc.metta
```

The flow must be:

```text
Goal
 ↓
Find applicable rule
 ↓
Generate subgoals
 ↓
Recursively solve subgoals
 ↓
Combine STVs
 ↓
Construct proof tree
 ↓
Return result
```

Test:

### A — Direct fact

```text
Socrates -> Human
```

### B — One rule

```text
Human -> Mortal
```

### C — Multi-step

```text
Socrates
 -> Human
 -> Mortal
```

### D — Missing fact

Expected:

```text
No proof
```

### E — Multiple proofs

Verify all available proofs or explicitly document selected-proof behavior.

### F — Cycles

```text
A -> B
B -> A
```

Depth bounds must terminate.

### G — Truth-value propagation

Derived STV must depend on actual premises.

Create:

```text
tests/test_backward_chaining_semantics.py
```

---

# PHASE 10 — COFFEE AGRICULTURE DOMAIN

Make:

```text
metta/kb/coffee_agriculture.metta
```

the primary demonstration knowledge base.

Keep it small, explainable, and technically meaningful.

Include entities such as:

```text
CoffeePlant01
CoffeeLeafRust
CoffeeBerryDisease
NutrientDeficiency
```

Symptoms such as:

```text
OrangeRustPustules
DarkBerryLesions
YellowLeafChlorosis
```

Environmental evidence such as:

```text
HighHumidity
HeavyRainfall
DenseShadedCanopy
```

Treatment relationships where justified.

Do not invent unsupported biological facts.

Clearly distinguish:

```text
Domain knowledge
```

from:

```text
PLN inference
```

---

## 10.1 Coffee Forward Scenario

Demonstrate:

```text
Observed symptom
        ↓
Disease inference
        ↓
Treatment recommendation
```

Example:

```text
CoffeePlant01
hasSymptom
OrangeRustPustules
```

then derive:

```text
AfflictedWith
CoffeeLeafRust
```

then:

```text
RequiresTreatment
CopperFungicideSpray
```

Use actual STV propagation.

---

## 10.2 Coffee Backward Scenario

Start with:

```text
RequiresTreatment CoffeePlant01 CopperFungicideSpray
```

Then show:

```text
Goal
 ↓
Required disease
 ↓
Required symptom
 ↓
Observed evidence
```

Display the proof tree.

---

## 10.3 Conflicting Evidence

Use two evidence sources.

For example:

```text
ScoutA:
Rust symptom observed
STV = (0.85, 0.75)

ScoutB:
Rust symptom uncertain/not observed
STV = (0.20, 0.70)
```

Apply revision.

Do not overwrite evidence.

Show:

```text
Before revision
After revision
```

---

# PHASE 11 — REASONING TRACE AND EXPLAINABILITY

The final system must explain WHY it reached a conclusion.

Create a reusable reasoning trace structure.

Example:

```text
QUERY
  |
  v
Goal:
RequiresTreatment(CoffeePlant01, CopperFungicideSpray)

RULE MATCH
  |
  v
Rule:
CoffeeLeafRust -> CopperFungicideSpray

SUBGOAL
  |
  v
AfflictedWith(CoffeePlant01, CoffeeLeafRust)

RULE MATCH
  |
  v
Rule:
OrangeRustPustules -> CoffeeLeafRust

FACT
  |
  v
HasSymptom(CoffeePlant01, OrangeRustPustules)

STV:
(0.88, 0.85)

FINAL RESULT:
RequiresTreatment(...)
STV:
(actual execution result)
```

The trace must come from the real proof structure.

Do not fabricate it in Python.

Create:

```text
docs/reasoning-trace.md
```

and test trace parsing.

---

# PHASE 12 — PYTHON INTEGRATION

Audit:

```text
src/pln_engine/
```

Required files:

```text
models.py
parser.py
runner.py
__init__.py
```

Python responsibilities:

```text
Initialize Hyperon
Load MeTTa
Execute MeTTa
Receive results
Parse AST/proof structures
Format results
Expose methods to UI
```

Python must NOT calculate PLN semantics independently.

Inspect every function.

If a function duplicates MeTTa semantics, remove or refactor it.

Create integration tests:

```text
tests/test_python_metta_integration.py
```

Test:

```text
Python
 ↓
Hyperon
 ↓
MeTTa
 ↓
PLN/BC/FC
 ↓
Hyperon result
 ↓
Python parser
 ↓
Structured result
```

---

# PHASE 13 — STREAMLIT FINAL APPLICATION

Audit:

```text
streamlit_app/app.py
```

The application must use the real engine.

Do not create fake UI results.

Create a professional but simple interface.

Recommended layout:

```text
================================================
      COFFEE AGRICULTURE PLN REASONER
================================================

Knowledge Base:
[Coffee Agriculture]

Reasoning Mode:
[Backward] [Forward] [PLN Revision] [Raw MeTTa]

Query / Evidence:
[........................................]

Depth:
[1 ---- 4]

[RUN REASONING]

------------------------------------------------
RESULT
------------------------------------------------

Conclusion:
...

Strength:
...

Confidence:
...

------------------------------------------------
REASONING TRACE
------------------------------------------------

...

------------------------------------------------
RULES / PREMISES USED
------------------------------------------------

...

------------------------------------------------
LIMITATIONS / NOTES
------------------------------------------------
...
```

Required modes:

### Mode 1

Backward chaining.

### Mode 2

Forward chaining.

### Mode 3

PLN revision.

### Mode 4

Raw MeTTa query.

Do not allow the UI to bypass the actual engine.

---

# PHASE 14 — FINAL TESTING, DOCUMENTATION, CLEANUP, AND MENTOR RELEASE

This is the final phase.

Do not declare completion until every item is verified.

---

## 14.1 FULL TEST SUITE

Run:

```bash
./run_tests.sh
```

Then:

```bash
PYTHONPATH=. .venv-metta/bin/pytest -v
```

Also execute the important MeTTa files directly:

```bash
.venv-metta/bin/metta examples/pln_demo.metta
```

and appropriate:

```text
MeTTa core tests
FC tests
BC tests
coffee domain tests
```

Record exact results.

---

# 14.2 ENVIRONMENT VERIFICATION

Record actual:

```bash
python3 --version
.venv-metta/bin/python --version
.venv-metta/bin/pip freeze
.venv-metta/bin/streamlit --version
.venv-metta/bin/pytest --version
```

Verify Hyperon version using an actual supported method.

Do NOT invent:

```text
hyperon.__version__
```

if that attribute does not exist.

Use installed package metadata if necessary.

Document the exact environment in:

```text
docs/environment.md
```

---

# 14.3 REPRODUCIBLE SETUP

Create or verify:

```text
requirements.txt
pyproject.toml
run_tests.sh
```

Provide a clean setup procedure:

```bash
git clone ...
cd ...
uv venv --python 3.12 .venv-metta
source .venv-metta/bin/activate
...
./run_tests.sh
.venv-metta/bin/streamlit run streamlit_app/app.py
```

Only include commands that actually work in the current project.

---

# 14.4 README FINALIZATION

Rewrite README based only on verified functionality.

README must contain:

## Project Overview

## Problem

## Architecture

## Why MeTTa / Hyperon

## PLN

## STV

## Deduction

## Induction

## Abduction

## Revision

## Forward Chaining

## Backward Chaining

## Coffee Agriculture Knowledge Base

## Python Integration

## Streamlit Demo

## Installation

## Testing

## Example Queries

## Limitations

## Official References

Do not claim:

```text
100% official implementation
```

if project-specific extensions exist.

Instead clearly distinguish:

```text
Official semantics
```

and:

```text
Project-specific implementation/extensions
```

---

# 14.5 OFFICIAL COMPARISON DOCUMENT

Ensure:

```text
docs/official-audit.md
```

contains a table:

| Component | Official | Project | Equivalent | Difference | Justification |
|---|---|---|---|---|---|

Include:

```text
STV
PLN formulas
Deduction
Induction
Abduction
Revision
Rule representation
Forward chaining
Backward chaining
Depth handling
Proof representation
Python integration
```

---

# 14.6 TECHNICAL REPORT

Create:

```text
docs/technical-report.md
```

Structure:

# 1. Introduction

# 2. Problem Definition

# 3. Knowledge Representation

# 4. PLN Mathematical Model

# 5. Truth Values

# 6. Deduction

# 7. Induction

# 8. Abduction

# 9. Revision

# 10. Forward Chaining

# 11. Backward Chaining

# 12. Coffee Agriculture Knowledge Base

# 13. System Architecture

# 14. Python Integration

# 15. Streamlit Interface

# 16. Experimental Results

# 17. Test Results

# 18. Limitations

# 19. Official Implementation Comparison

# 20. Conclusion

Use actual results.

---

# 14.7 DEMO GUIDE

Create:

```text
docs/demo-guide.md
```

A mentor should be able to run the project by following this document.

Include:

```text
1. Environment setup
2. Start application
3. Select Coffee Agriculture
4. Run Forward Chaining
5. Run Backward Chaining
6. Run Revision
7. Inspect proof tree
8. Run raw MeTTa query
9. Run tests
```

Also provide exact example inputs.

---

# 14.8 MENTOR PRESENTATION SCENARIO

Create:

```text
docs/mentor-demo-script.md
```

Include a short 5–10 minute demonstration.

Suggested sequence:

### Step 1

Explain the architecture.

### Step 2

Show STV.

### Step 3

Run PLN deduction.

### Step 4

Run coffee disease forward chaining.

### Step 5

Run coffee disease backward chaining.

### Step 6

Show conflicting evidence.

### Step 7

Run revision.

### Step 8

Show proof trace.

### Step 9

Show Python integration.

### Step 10

Show Streamlit.

### Step 11

Show tests.

---

# 14.9 CODE QUALITY AUDIT

Inspect the entire repository.

Find:

```text
unused files
duplicate code
temporary scripts
debug prints
fake outputs
dead implementations
unused imports
obsolete experiments
```

Classify:

```text
CORE
TEST
DOCUMENTATION
EXAMPLE
EXPERIMENTAL
OBSOLETE
```

Do not delete research material blindly.

Clean only what is safe.

---

# 14.10 SECURITY / SAFETY / ROBUSTNESS

Verify:

- malformed input does not crash the application
- invalid depth is rejected
- unknown predicates are handled
- unknown entities are handled
- missing proof returns cleanly
- cycles terminate
- raw MeTTa input is handled appropriately
- no credentials/secrets are committed
- no unnecessary network dependency exists during normal execution

---

# 14.11 FINAL PROJECT TREE

Produce a final tree similar to:

```text
pln_engin_project/
│
├── README.md
├── pyproject.toml
├── requirements.txt
├── run_tests.sh
├── .gitignore
│
├── metta/
│   ├── core/
│   │   ├── pln_tv.metta
│   │   └── pln_formulas.metta
│   │
│   ├── chaining/
│   │   ├── nat.metta
│   │   ├── bc.metta
│   │   └── fc.metta
│   │
│   ├── rules/
│   │   └── rules.metta
│   │
│   ├── kb/
│   │   ├── coffee_agriculture.metta
│   │   ├── socrates.metta
│   │   ├── medical.metta
│   │   └── birds.metta
│   │
│   └── tests/
│
├── examples/
│   └── pln_demo.metta
│
├── src/
│   └── pln_engine/
│       ├── __init__.py
│       ├── models.py
│       ├── parser.py
│       └── runner.py
│
├── tests/
│   ├── test_truth_values.py
│   ├── test_pln_operations_audit.py
│   ├── test_backward_chaining.py
│   ├── test_backward_chaining_semantics.py
│   ├── test_forward_chaining.py
│   ├── test_forward_chaining_semantics.py
│   ├── test_coffee_agriculture.py
│   ├── test_negative_and_edge_cases.py
│   ├── test_python_metta_integration.py
│   └── test_parser.py
│
├── streamlit_app/
│   └── app.py
│
└── docs/
    ├── official-audit.md
    ├── pln-examples.md
    ├── reasoning-trace.md
    ├── environment.md
    ├── technical-report.md
    ├── demo-guide.md
    ├── mentor-demo-script.md
    └── final-validation-report.md
```

The exact tree may differ if there is a technically better organization. Do not create unnecessary duplicate files just to match this example.

---

# FINAL ACCEPTANCE CHECKLIST

Before declaring the project complete, verify ALL:

```text
[ ] Official Hyperon runtime works
[ ] Supported Python environment documented
[ ] Official source repositories inspected
[ ] Official comparison completed
[ ] STV semantics verified
[ ] Strength/confidence validated
[ ] Weight conversion validated
[ ] Deduction verified
[ ] Induction verified
[ ] Abduction verified
[ ] Revision verified
[ ] Modus Ponens verified
[ ] Negation verified
[ ] Intersection verified

[ ] Forward chaining genuinely works
[ ] Backward chaining genuinely works
[ ] Multi-step reasoning works
[ ] Multiple rules work
[ ] Missing proofs handled
[ ] Cycles terminate
[ ] Depth limits work
[ ] Truth values propagate through rules
[ ] Proof trees are real

[ ] Coffee Agriculture KB works
[ ] Same KB supports FC
[ ] Same KB supports BC
[ ] Coffee disease scenario works
[ ] Treatment inference works
[ ] Conflicting evidence works
[ ] Revision works

[ ] Python only orchestrates MeTTa
[ ] Python parser only interprets actual Hyperon results
[ ] Streamlit invokes the real engine
[ ] No hard-coded demo outputs
[ ] Raw MeTTa execution works

[ ] Positive tests pass
[ ] Negative tests pass
[ ] Integration tests pass
[ ] MeTTa tests pass
[ ] Full regression passes

[ ] README matches reality
[ ] Official audit matches reality
[ ] Technical report completed
[ ] Demo guide completed
[ ] Mentor demo script completed
[ ] Environment documented
[ ] Reproduction commands verified
[ ] Repository cleaned
[ ] No secrets committed
[ ] Known limitations documented
```

---

# FINAL VALIDATION REPORT

Update:

```text
docs/final-validation-report.md
```

with the FINAL actual state.

Use this exact structure:

```text
# FINAL PROJECT VALIDATION REPORT

## Overall Status

PASS
PASS WITH LIMITATIONS
FAIL

## Project

PLN + MeTTa + Hyperon Probabilistic Reasoning System

## Environment

Python:
Hyperon:
MeTTa:
Streamlit:
Pytest:
OS:

## Official Sources Audited

...

## Architecture

...

## STV

...

## PLN

Deduction:
Induction:
Abduction:
Revision:

## Forward Chaining

...

## Backward Chaining

...

## Coffee Agriculture Domain

...

## Conflicting Evidence

...

## Proof / Reasoning Trace

...

## Python Integration

...

## Streamlit

...

## Automated Tests

Exact command:
Exact result:

## MeTTa Tests

Exact command:
Exact result:

## Manual Demo

...

## Official Differences

...

## Project-Specific Extensions

...

## Known Limitations

...

## Reproducibility

...

## Files Changed

...

## Final Acceptance Checklist

...

## Final Conclusion

...
```

---

# CRITICAL FINAL RULE

Do not simply create documentation saying these things are complete.

Actually execute them first.

If a requirement is already implemented, verify it and keep it.

If a requirement is partially implemented, fix it.

If a requirement is incorrect, correct it.

If an official behavior cannot be reproduced exactly because the project intentionally uses a domain-specific extension, document that clearly rather than pretending they are identical.

Do not replace MeTTa reasoning with Python.

Do not fabricate tests.

Do not fabricate mathematical outputs.

Do not fabricate official-source comparisons.

Do not stop after creating files.

---

# FINAL EXECUTION ORDER

Follow this exact order:

```text
PHASE 6
Official audit + correctness verification
        ↓
PHASE 7
PLN completion
        ↓
PHASE 8
Forward chaining
        ↓
PHASE 9
Backward chaining
        ↓
PHASE 10
Coffee agriculture domain
        ↓
PHASE 11
Reasoning trace
        ↓
PHASE 12
Python integration
        ↓
PHASE 13
Streamlit integration
        ↓
PHASE 14
Testing + documentation + cleanup + final validation
```

After each phase:

1. implement
2. execute
3. test
4. inspect output
5. fix failures
6. document actual result
7. only then continue

Do not stop for approval between phases.

Continue automatically through Phase 14.

At the very end, provide ONLY a concise final report in this format:

```text
==================================================
FINAL PROJECT STATUS
==================================================

STATUS:
PASS / PASS WITH LIMITATIONS / FAIL

PHASES COMPLETED:
6–14

OFFICIAL SOURCE AUDIT:
...

PLN:
...

FORWARD CHAINING:
...

BACKWARD CHAINING:
...

COFFEE AGRICULTURE:
...

CONFLICTING EVIDENCE:
...

REASONING TRACE:
...

PYTHON INTEGRATION:
...

STREAMLIT:
...

TEST RESULTS:
...

METTA EXECUTION:
...

IMPORTANT DIFFERENCES:
...

KNOWN LIMITATIONS:
...

FILES CREATED / MODIFIED:
...

REPRODUCTION COMMAND:
...

STREAMLIT COMMAND:
...

FINAL MENTOR READINESS:
READY / NOT READY
==================================================
```

The project is considered finished ONLY after the complete Phase 6 → Phase 14 workflow has been executed and the final validation report has been generated from actual evidence.
---

## 2. Python Runtimes

- **System Python**: `Python 3.14.4` (pre-release, unsupported by PyPI C-extension binary wheels).
- **Target Runtime Environment**: `Python 3.12.15` (provisioned via `uv` at `.venv-metta`).

```bash
$ .venv-metta/bin/python --version
Python 3.12.15
```

---

## 3. Core Package Versions

| Package | Version | Verification Method |
| :--- | :--- | :--- |
| **`hyperon`** | `0.2.10` | `.venv-metta/bin/python -c "import hyperon; print(hyperon.__version__)"` |
| **`streamlit`** | `1.65.0` | `.venv-metta/bin/streamlit --version` |
| **`pytest`** | `9.1.1` | `.venv-metta/bin/pytest --version` |
| **`uv`** | `0.12.23` | System package installer |

---

## 4. Complete Frozen Dependency Graph

Generated from active environment `.venv-metta`:

```text
altair==6.3.0
anyio==4.15.1
attrs==26.1.0
certifi==2026.7.22
charset-normalizer==3.5.2
click==8.5.0
h11==0.16.0
httptools==0.8.0
hyperon==0.2.10
idna==3.20
iniconfig==2.3.0
itsdangerous==2.2.0
Jinja2==3.1.6
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
MarkupSafe==3.0.4
narwhals==2.26.0
numpy==2.5.3
packaging==26.3
pandas==3.0.6
pillow==12.3.0
pluggy==1.6.0
protobuf==7.36.2
pyarrow==25.0.1
pydeck==0.9.3
Pygments==2.21.0
pytest==9.1.1
python-dateutil==2.9.0.post0
python-multipart==0.0.32
referencing==0.37.0
requests==2.34.2
rpds-py==2026.9.1
six==1.17.0
starlette==1.7.0
streamlit==1.65.0
toml==0.10.2
typing_extensions==4.16.0
urllib3==2.8.0
uvicorn==0.54.0
watchdog==6.0.0
websockets==17.2
```

---

## 5. Verification Commands

```bash
# Verify Python version
.venv-metta/bin/python --version

# Verify Hyperon version
.venv-metta/bin/python -c "import hyperon; print(hyperon.__version__)"

# Verify MeTTa CLI
.venv-metta/bin/metta --version

# Run full test regression
./run_tests.sh
```
