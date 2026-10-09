from hyperon import MeTTa
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import re


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
ENGINE_DIR = BASE_DIR / "engine"

FACT_FILE = KNOWLEDGE_DIR / "agriculture.metta"
RULE_FILE = KNOWLEDGE_DIR / "rule.metta"
PLN_FILE = ENGINE_DIR / "pln.metta"

CHAIN_FILES = [
    ENGINE_DIR / "forward_chain.metta",
    ENGINE_DIR / "backward_chain.metta",
]

NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
ATOM = r"\([A-Za-z0-9_-]+\)"

FACT_PATTERN = re.compile(
    rf"\(:\s*(\S+)\s+"
    rf"({ATOM})\s+"
    rf"\(stv\s+({NUMBER})\s+({NUMBER})\)\s*\)",
    re.MULTILINE,
)

RULE_PATTERN = re.compile(
    rf"\(:\s*(\S+)\s*"
    rf"\(rule\s+"
    rf"({ATOM})\s+"
    rf"({ATOM})\s+"
    rf"({ATOM})\s+"
    rf"\(stv\s+({NUMBER})\s+({NUMBER})\)"
    rf"\)\s*\)",
    re.DOTALL,
)

VALID_ATOM = re.compile(rf"^{ATOM}$")


# ============================================================
# METTA RUNTIME AND SESSION DATA
# ============================================================

mt = MeTTa()

facts = {}
rules = []
derived_facts = {}
reasoning_history = []


# ============================================================
# SOURCE LOADING
# ============================================================

def read_source(path):
    if not path.is_file():
        raise FileNotFoundError(f"Required file not found: {path}")

    return path.read_text(encoding="utf-8")


def execute(code):
    return mt.run(code)


def format_result(result):
    if result is None:
        return "No result returned."

    if isinstance(result, (list, tuple)):
        if not result:
            return "No result returned."

        return "\n".join(format_result(item) for item in result)

    return str(result)


def validate_stv(strength, confidence):
    strength = float(strength)
    confidence = float(confidence)

    if not 0.0 <= strength <= 1.0:
        raise ValueError(
            f"Strength must be between 0 and 1: {strength}"
        )

    if not 0.0 <= confidence <= 1.0:
        raise ValueError(
            f"Confidence must be between 0 and 1: {confidence}"
        )

    return strength, confidence


def stv_text(stv):
    return f"(stv {stv[0]:.6f} {stv[1]:.6f})"


def parse_stv(result):
    text = format_result(result)

    pattern = re.compile(
        rf"\(?(?:stv-value|stv)\s+"
        rf"({NUMBER})\s+({NUMBER})\)?"
    )

    matches = list(pattern.finditer(text))

    if not matches:
        raise ValueError(
            "Could not parse an STV from the MeTTa result.\n"
            f"Raw result:\n{text}"
        )

    strength, confidence = matches[-1].groups()

    return validate_stv(strength, confidence)


def load_project():
    global facts, rules

    fact_source = read_source(FACT_FILE)
    rule_source = read_source(RULE_FILE)
    pln_source = read_source(PLN_FILE)

    execute(fact_source)
    execute(rule_source)
    execute(pln_source)

    for path in CHAIN_FILES:
        execute(read_source(path))

    execute("""
    (= (fact-stv $fact)
        (match &self
            (: $id $fact (stv $s $c))
            (stv-value $s $c)))
    """)

    facts = {}

    for match in FACT_PATTERN.finditer(fact_source):
        fact_id, expression, strength, confidence = match.groups()

        facts[expression] = {
            "id": fact_id,
            "source_stv": validate_stv(strength, confidence),
        }

    rules = []

    for match in RULE_PATTERN.finditer(rule_source):
        (
            rule_id,
            premise1,
            premise2,
            conclusion,
            strength,
            confidence,
        ) = match.groups()

        rules.append({
            "id": rule_id,
            "premise1": premise1,
            "premise2": premise2,
            "conclusion": conclusion,
            "stv": validate_stv(strength, confidence),
        })

    if not facts:
        raise ValueError(
            f"No facts were parsed from {FACT_FILE.name}. "
            "Check the fact syntax."
        )

    if not rules:
        raise ValueError(
            f"No rules were parsed from {RULE_FILE.name}. "
            "Check the rule syntax."
        )


# ============================================================
# FACT AND RULE LOOKUPS
# ============================================================

def query_fact_stv(expression):
    if expression not in facts:
        raise ValueError(
            f"Not an original knowledge-base fact: {expression}"
        )

    result = execute(f"!(fact-stv {expression})")

    return parse_stv(result)


def get_stv(expression, prefer_derived=True):
    if prefer_derived and expression in derived_facts:
        return derived_facts[expression]

    if expression in facts:
        return query_fact_stv(expression)

    if expression in derived_facts:
        return derived_facts[expression]

    raise ValueError(f"No STV is available for {expression}")


def all_expressions():
    expressions = list(facts.keys())

    for rule in rules:
        conclusion = rule["conclusion"]

        if conclusion not in expressions:
            expressions.append(conclusion)

    for expression in derived_facts:
        if expression not in expressions:
            expressions.append(expression)

    return expressions


def get_rule(rule_id):
    for rule in rules:
        if rule["id"] == rule_id:
            return rule

    raise ValueError(f"Rule not found: {rule_id}")


def matching_rule(fact_a, fact_b):
    """
    Find a rule whose two premises match the inputs.

    The order of the selected inputs does not matter.
    No rule is selected from the user's rule selector.
    """

    for rule in rules:
        if (
            rule["premise1"] == fact_a
            and rule["premise2"] == fact_b
        ) or (
            rule["premise1"] == fact_b
            and rule["premise2"] == fact_a
        ):
            return rule

    return None


def rules_for_conclusion(expression):
    return [
        rule for rule in rules
        if rule["conclusion"] == expression
    ]


def refresh_selectors():
    choices = all_expressions()
    rule_ids = [rule["id"] for rule in rules]

    for combo in (
        fact1_combo,
        fact2_combo,
        revision_target_combo,
        evidence_combo,
        goal_combo,
    ):
        current = combo.get()
        combo["values"] = choices

        if current in choices:
            combo.set(current)
        elif choices:
            combo.current(0)
        else:
            combo.set("")

    current_rule = rule_combo.get()
    rule_combo["values"] = rule_ids

    if current_rule in rule_ids:
        rule_combo.set(current_rule)
    elif rule_ids:
        rule_combo.current(0)
    else:
        rule_combo.set("")


# ============================================================
# CALL THE REAL METTA OPERATIONS
# ============================================================

OPERATIONS = {
    "Deduction": "deduction",
    "Induction": "induction",
    "Abduction": "abduction",
    "Revision": "revision",
}


def run_pln_operation(operation, stv1, stv2):
    """
    Execute the operation implemented in engine/pln.metta.
    Python does not reimplement the PLN formulas.
    """

    if operation not in OPERATIONS:
        raise ValueError(f"Unsupported operation: {operation}")

    function_name = OPERATIONS[operation]

    query = (
        f"!( {function_name} "
        f"(stv-value {stv1[0]:.12g} {stv1[1]:.12g}) "
        f"(stv-value {stv2[0]:.12g} {stv2[1]:.12g}) )"
    )

    raw = execute(query)
    result_stv = parse_stv(raw)

    return {
        "operation": operation,
        "query": query,
        "raw": format_result(raw),
        "stv": result_stv,
    }


# ============================================================
# OUTPUT FORMATTING
# ============================================================

def show_output(title, content):
    output.configure(state=tk.NORMAL)
    output.delete("1.0", tk.END)

    output.insert(tk.END, f"{title}\n")
    output.insert(tk.END, "=" * max(12, len(title)) + "\n\n")
    output.insert(tk.END, content.rstrip() + "\n")

    output.configure(state=tk.DISABLED)


def show_error(title, error):
    show_output(
        title,
        f"Operation failed:\n\n{error}\n\n"
        "Check the MeTTa result, selected inputs, "
        "and the rules loaded from rule.metta."
    )


def section(lines, title):
    lines.append("")
    lines.append(title)
    lines.append("-" * len(title))


def row(lines, label, value):
    lines.append(f"{label:<25} | {value}")


def show_stv(lines, label, stv):
    row(lines, label, stv_text(stv))


def rule_details(lines, rule):
    row(lines, "Rule ID", rule["id"])
    row(lines, "Premise 1", rule["premise1"])
    row(lines, "Premise 2", rule["premise2"])
    row(lines, "Conclusion", rule["conclusion"])
    show_stv(lines, "Rule STV", rule["stv"])


def save_derived(expression, stv, description):
    """
    Save a derived result for use by later GUI operations.
    Source files are not modified.
    """

    derived_facts[expression] = stv

    reasoning_history.append({
        "expression": expression,
        "stv": stv,
        "description": description,
    })


# ============================================================
# DEDUCTION AND INDUCTION
# AUTOMATIC RULE SELECTION
# ============================================================

def run_selected_operation():
    operation = operation_var.get()
    fact_a = fact1_combo.get().strip()
    fact_b = fact2_combo.get().strip()
    selected_rule_id = rule_combo.get().strip()

    if not fact_a or not fact_b:
        show_output(
            "PLN OPERATION",
            "Select both input facts or conclusions."
        )
        return

    try:
        lines = []

        section(lines, "STEP 1 — SELECTED OPERATION")
        row(lines, "Operation", operation)
        row(lines, "MeTTa function", OPERATIONS[operation])

        # ----------------------------------------------------
        # DEDUCTION AND INDUCTION
        # Automatically match a rule from the two premises.
        # ----------------------------------------------------

        if operation in ("Deduction", "Induction"):

            stv_a = get_stv(fact_a)
            stv_b = get_stv(fact_b)

            section(lines, "STEP 2 — FIRST INPUT")
            row(lines, "Fact / conclusion", fact_a)
            show_stv(lines, "Input STV", stv_a)

            section(lines, "STEP 3 — SECOND INPUT")
            row(lines, "Fact / conclusion", fact_b)
            show_stv(lines, "Input STV", stv_b)

            # AUTOMATIC RULE MATCHING
            rule = matching_rule(fact_a, fact_b)

            section(lines, "STEP 4 — AUTOMATIC RULE SELECTION")

            if rule is None:
                raise ValueError(
                    f"No matching rule was found for:\n"
                    f"  Input 1: {fact_a}\n"
                    f"  Input 2: {fact_b}\n\n"
                    "The two inputs must match the premises of "
                    "a rule loaded from knowledge/rule.metta.\n"
                    "The rule selector is not used for deduction "
                    "or induction."
                )

            rule_details(lines, rule)

            row(
                lines,
                "Rule selection",
                "Automatically matched from input premises",
            )

            # Execute the selected PLN formula in MeTTa.
            result = run_pln_operation(
                operation,
                stv_a,
                stv_b,
            )

            # Use the conclusion of the matched rule.
            derived_expression = rule["conclusion"]

            save_derived(
                derived_expression,
                result["stv"],
                f"{operation} using automatically matched "
                f"rule {rule['id']}",
            )

            section(lines, "STEP 5 — METTA EXECUTION")
            row(lines, "Query", result["query"])
            row(lines, "Raw result", result["raw"])

            section(lines, "STEP 6 — DERIVED CONCLUSION")
            row(lines, "Rule applied", rule["id"])
            row(lines, "Conclusion", derived_expression)
            show_stv(lines, "Conclusion STV", result["stv"])

            if operation == "Deduction":
                row(
                    lines,
                    "Reasoning direction",
                    "Premises → Conclusion",
                )
            else:
                row(
                    lines,
                    "Reasoning direction",
                    "Selected evidence → Generalization",
                )

            lines.append("")
            lines.append(
                "The STV displayed for the conclusion is the result "
                "returned by the selected MeTTa operation."
            )

        # ----------------------------------------------------
        # ABDUCTION
        # The user selects an explanatory rule.
        # ----------------------------------------------------

        elif operation == "Abduction":

            observed = fact_a
            observed_stv = get_stv(observed)

            # For abduction, the rule selector remains available.
            if not selected_rule_id:
                raise ValueError(
                    "Select an explanatory rule for abduction."
                )

            rule = get_rule(selected_rule_id)

            section(lines, "STEP 2 — OBSERVED FACT")
            row(lines, "Observed fact", observed)
            show_stv(lines, "Observed STV", observed_stv)

            section(lines, "STEP 3 — SELECTED EXPLANATORY RULE")
            rule_details(lines, rule)

            if rule["conclusion"] != observed:
                raise ValueError(
                    f"The selected rule {rule['id']} does not "
                    f"conclude the observed fact {observed}.\n\n"
                    f"Rule conclusion: {rule['conclusion']}\n"
                    "Select a rule whose conclusion matches "
                    "the observed fact."
                )

            section(lines, "STEP 4 — RULE PREMISES")

            row(lines, "Possible premise 1", rule["premise1"])
            row(lines, "Possible premise 2", rule["premise2"])

            row(
                lines,
                "Explanation",
                f"{rule['premise1']} AND {rule['premise2']}",
            )

            # Execute the actual MeTTa abduction function.
            result = run_pln_operation(
                "Abduction",
                observed_stv,
                rule["stv"],
            )

            explanation = (
                f"(possible-explanation "
                f"{rule['premise1']} {rule['premise2']})"
            )

            save_derived(
                explanation,
                result["stv"],
                f"Abduction using {rule['id']}",
            )

            section(lines, "STEP 5 — METTA EXECUTION")
            row(lines, "Query", result["query"])
            row(lines, "Raw result", result["raw"])

            section(lines, "STEP 6 — POSSIBLE EXPLANATION")
            row(lines, "Selected rule", rule["id"])
            row(lines, "Premise 1", rule["premise1"])
            row(lines, "Premise 2", rule["premise2"])
            row(lines, "Observed conclusion", observed)
            row(lines, "Explanation expression", explanation)

            show_stv(lines, "Explanation STV", result["stv"])

            row(
                lines,
                "Reasoning direction",
                "Observed conclusion → Possible explanation",
            )

        # ----------------------------------------------------
        # REVISION
        # Keep the existing revision inputs and behavior.
        # ----------------------------------------------------

        elif operation == "Revision":

            existing_stv = get_stv(
                fact_a,
                prefer_derived=False,
            )

            evidence_stv = validate_stv(
                new_evidence_strength_var.get(),
                new_evidence_confidence_var.get(),
            )

            section(lines, "STEP 2 — EXISTING EVIDENCE")
            row(lines, "Existing proposition", fact_a)
            show_stv(lines, "Existing STV", existing_stv)

            section(lines, "STEP 3 — NEW EVIDENCE")
            row(lines, "Evidence source / reference", fact_b)
            show_stv(lines, "New evidence STV", evidence_stv)

            result = run_pln_operation(
                "Revision",
                existing_stv,
                evidence_stv,
            )

            save_derived(
                fact_a,
                result["stv"],
                "Revision of existing evidence",
            )

            section(lines, "STEP 4 — METTA EXECUTION")
            row(lines, "Query", result["query"])
            row(lines, "Raw result", result["raw"])

            section(lines, "STEP 5 — REVISED TRUTH VALUE")
            row(lines, "Revised proposition", fact_a)
            show_stv(lines, "Revised STV", result["stv"])

            row(
                lines,
                "Reasoning direction",
                "Existing evidence + New evidence → Revised STV",
            )

        refresh_selectors()

        show_output(
            f"{operation.upper()} — STEP-BY-STEP TRACE",
            "\n".join(lines),
        )

    except Exception as error:
        show_error(f"{operation.upper()} TRACE", error)


# ============================================================
# DISPLAY ALL KNOWLEDGE-BASE FACTS
# ============================================================

def show_all_facts():
    try:
        lines = []

        for expression, metadata in facts.items():
            stv = query_fact_stv(expression)

            section(lines, metadata["id"])
            row(lines, "Fact", expression)
            show_stv(lines, "Truth value", stv)

        if derived_facts:
            section(lines, "SESSION-DERIVED CONCLUSIONS")

            for expression, stv in derived_facts.items():
                row(lines, "Conclusion", expression)
                show_stv(lines, "Truth value", stv)
                lines.append("")

        show_output(
            "FACTS AND STV VALUES",
            "\n".join(lines),
        )

    except Exception as error:
        show_error("FACTS AND STV VALUES", error)


# ============================================================
# DISPLAY ALL RULES
# ============================================================

def show_all_rules():
    lines = []

    for rule in rules:
        section(lines, rule["id"])
        rule_details(lines, rule)

    show_output(
        "RULES LOADED FROM rule.metta",
        "\n".join(lines),
    )


# ============================================================
# FORWARD CHAINING — RULE-BY-RULE TRACE
# ============================================================

def run_forward():
    start = fact1_combo.get().strip()

    try:
        depth_limit = int(depth_var.get())

        if not start:
            raise ValueError("Select a starting fact.")

        if depth_limit < 0:
            raise ValueError("Depth must be zero or greater.")

        available = {}

        for expression in facts:
            available[expression] = query_fact_stv(expression)

        available.update(derived_facts)

        if start not in available:
            raise ValueError(f"No STV is available for {start}")

        lines = [
            f"Starting fact: {start}",
            f"Starting STV: {stv_text(available[start])}",
            f"Maximum depth: {depth_limit}",
            "",
            "Rules are read from rule.metta.",
            "Operations are executed using pln.metta.",
        ]

        frontier = {start}
        fired_rules = set()

        for depth in range(1, depth_limit + 1):
            section(lines, f"DEPTH {depth}")

            next_frontier = set()

            for rule in rules:
                if rule["id"] in fired_rules:
                    continue

                p1 = rule["premise1"]
                p2 = rule["premise2"]

                if p1 not in frontier and p2 not in frontier:
                    continue

                if p1 not in available or p2 not in available:
                    missing = [
                        p for p in (p1, p2)
                        if p not in available
                    ]

                    lines.append(
                        f"WAIT {rule['id']}: missing "
                        + ", ".join(missing)
                    )
                    continue

                stv1 = available[p1]
                stv2 = available[p2]

                section(lines, f"APPLY {rule['id']}")
                rule_details(lines, rule)

                show_stv(lines, "Premise 1 STV", stv1)
                show_stv(lines, "Premise 2 STV", stv2)

                result = run_pln_operation(
                    "Deduction",
                    stv1,
                    stv2,
                )

                conclusion = rule["conclusion"]
                conclusion_stv = result["stv"]

                row(lines, "MeTTa query", result["query"])
                row(lines, "Raw result", result["raw"])

                if conclusion in available:
                    old_stv = available[conclusion]

                    lines.append("")
                    lines.append("Existing conclusion found.")

                    show_stv(lines, "Previous STV", old_stv)
                    show_stv(
                        lines,
                        "New evidence STV",
                        conclusion_stv,
                    )

                    revision = run_pln_operation(
                        "Revision",
                        old_stv,
                        conclusion_stv,
                    )

                    row(
                        lines,
                        "Revision query",
                        revision["query"],
                    )

                    show_stv(
                        lines,
                        "Revised STV",
                        revision["stv"],
                    )

                    conclusion_stv = revision["stv"]

                available[conclusion] = conclusion_stv
                derived_facts[conclusion] = conclusion_stv

                next_frontier.add(conclusion)

                row(lines, "Derived conclusion", conclusion)
                show_stv(
                    lines,
                    "Conclusion STV",
                    conclusion_stv,
                )

                fired_rules.add(rule["id"])

            if not next_frontier:
                lines.extend([
                    "",
                    "STOP CONDITION",
                    "No new conclusion was derived at this depth.",
                ])
                break

            frontier = next_frontier

        else:
            lines.extend([
                "",
                "STOP CONDITION",
                f"Maximum depth limit ({depth_limit}) reached.",
            ])

        section(lines, "FINAL DERIVED CONCLUSIONS")

        if derived_facts:
            for expression, stv in derived_facts.items():
                row(lines, "Conclusion", expression)
                show_stv(lines, "STV", stv)
                lines.append("")
        else:
            lines.append("No derived conclusions were produced.")

        # Execute the actual forward-chaining function.
        engine_query = (
            f"!(forward-query {start} &self "
            f"(fromNumber {depth_limit}))"
        )

        section(lines, "RESULT FROM forward_chain.metta")
        row(lines, "Query", engine_query)
        lines.append(format_result(execute(engine_query)))

        lines.extend([
            "",
            "STV TRACE NOTE",
            "The rule-by-rule STV calculations above call pln.metta.",
            "The forward-query result is displayed separately from "
            "the Python-generated STV trace.",
        ])

        reasoning_history.append({
            "mode": "forward",
            "start": start,
            "depth": depth_limit,
        })

        show_output(
            "FORWARD CHAINING — FULL TRACE",
            "\n".join(lines),
        )

        refresh_selectors()

    except Exception as error:
        show_error("FORWARD CHAINING", error)


# ============================================================
# BACKWARD CHAINING — DYNAMIC GOAL AND PROOF TRACE
# ============================================================

def prove_goal(goal, available, remaining_depth, visited, lines):
    lines.append("")
    lines.append(
        f"GOAL: {goal} | remaining depth: {remaining_depth}"
    )

    if goal in available:
        stv = available[goal]

        row(lines, "Known fact / conclusion", goal)
        show_stv(lines, "Available STV", stv)

        lines.append(
            "This branch stops: the goal is already known."
        )

        return True, stv

    if remaining_depth <= 0:
        lines.append("STOP: search depth limit reached.")
        return False, None

    if goal in visited:
        lines.append("STOP: cycle detected.")
        return False, None

    # Find candidate rules dynamically from rule.metta.
    candidates = rules_for_conclusion(goal)

    if not candidates:
        lines.append("FAIL: no rule concludes this goal.")
        return False, None

    next_visited = visited | {goal}

    for rule in candidates:
        section(lines, f"TRY RULE {rule['id']}")
        rule_details(lines, rule)

        ok1, stv1 = prove_goal(
            rule["premise1"],
            available,
            remaining_depth - 1,
            next_visited,
            lines,
        )

        if not ok1:
            lines.append(
                "Rule failed: first premise was not proved."
            )
            continue

        ok2, stv2 = prove_goal(
            rule["premise2"],
            available,
            remaining_depth - 1,
            next_visited,
            lines,
        )

        if not ok2:
            lines.append(
                "Rule failed: second premise was not proved."
            )
            continue

        section(
            lines,
            f"CALCULATE CONCLUSION STV — {rule['id']}",
        )

        row(lines, "Premise 1", rule["premise1"])
        show_stv(lines, "Premise 1 STV", stv1)

        row(lines, "Premise 2", rule["premise2"])
        show_stv(lines, "Premise 2 STV", stv2)

        # Calculate using the MeTTa deduction operation.
        result = run_pln_operation(
            "Deduction",
            stv1,
            stv2,
        )

        row(lines, "MeTTa query", result["query"])
        row(lines, "Raw result", result["raw"])

        # Preserve the existing rule-STV combination behavior.
        rule_result = run_pln_operation(
            "Deduction",
            result["stv"],
            rule["stv"],
        )

        row(
            lines,
            "Rule-combination query",
            rule_result["query"],
        )

        show_stv(
            lines,
            "Derived conclusion STV",
            rule_result["stv"],
        )

        available[goal] = rule_result["stv"]
        derived_facts[goal] = rule_result["stv"]

        lines.append(f"PROVED: {goal}")

        return True, rule_result["stv"]

    lines.append(f"FAIL: no candidate rule proved {goal}.")

    return False, None


def run_backward():
    goal = goal_combo.get().strip()

    try:
        depth_limit = int(depth_var.get())

        if not VALID_ATOM.fullmatch(goal):
            raise ValueError(
                "Choose a goal expression from the selector."
            )

        if depth_limit < 0:
            raise ValueError("Depth must be zero or greater.")

        available = {}

        for expression in facts:
            available[expression] = query_fact_stv(expression)

        available.update(derived_facts)

        lines = [
            f"Target goal: {goal}",
            f"Maximum depth: {depth_limit}",
            "",
            "Backward chaining starts from the selected goal.",
            "Candidate rules are retrieved dynamically from "
            "knowledge/rule.metta.",
            "No specific conclusion is hardcoded.",
        ]

        success, result_stv = prove_goal(
            goal,
            available,
            depth_limit,
            set(),
            lines,
        )

        section(lines, "FINAL PROOF RESULT")

        row(lines, "Goal", goal)
        row(lines, "Proven", "YES" if success else "NO")

        if result_stv is not None:
            show_stv(lines, "Goal STV", result_stv)
        else:
            row(lines, "Goal STV", "No result")

        # Execute the project's actual MeTTa backward-chaining function.
        engine_query = (
            f"!(backward-query {goal} &self "
            f"(fromNumber {depth_limit}))"
        )

        section(lines, "ACTUAL METTA BACKWARD-CHAINING RESULT")
        row(lines, "Query", engine_query)

        engine_result = execute(engine_query)

        lines.append(format_result(engine_result))

        lines.extend([
            "",
            "EXECUTION NOTE",
            "The proof trace above shows the dynamically matched rules "
            "and their STV calculations.",
            "The actual backward-query result is displayed separately "
            "from the Python proof trace.",
        ])

        reasoning_history.append({
            "mode": "backward",
            "goal": goal,
            "depth": depth_limit,
            "success": success,
        })

        show_output(
            "BACKWARD CHAINING — FULL TRACE",
            "\n".join(lines),
        )

        refresh_selectors()

    except Exception as error:
        show_error("BACKWARD CHAINING", error)


# ============================================================
# VIEW THE ACTUAL ENGINE SOURCE
# ============================================================

def show_engine_source():
    try:
        lines = []

        for path in [PLN_FILE, *CHAIN_FILES]:
            section(
                lines,
                str(path.relative_to(BASE_DIR)),
            )
            lines.append(read_source(path))

        show_output(
            "ACTUAL METTA ENGINE SOURCE",
            "\n".join(lines),
        )

    except Exception as error:
        show_error("ENGINE SOURCE", error)


def show_knowledge_source():
    try:
        lines = []

        for path in [FACT_FILE, RULE_FILE]:
            section(
                lines,
                str(path.relative_to(BASE_DIR)),
            )
            lines.append(read_source(path))

        show_output(
            "ACTUAL KNOWLEDGE-BASE SOURCE",
            "\n".join(lines),
        )

    except Exception as error:
        show_error("KNOWLEDGE BASE", error)


# ============================================================
# INITIALIZE THE METTA ENGINE
# ============================================================

try:
    load_project()
except Exception as error:
    raise SystemExit(
        f"Could not initialize the MeTTa engine:\n{error}"
    )


# ============================================================
# GUI
# ============================================================

root = tk.Tk()
root.title("Agricultural PLN Reasoning Engine")
root.geometry("1250x900")
root.configure(bg="#101827")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6)
style.configure("TCombobox", padding=4)


# ---------------- Application heading -------------------------

tk.Label(
    root,
    text="Agricultural PLN Reasoning Engine",
    font=("Arial", 22, "bold"),
    bg="#101827",
    fg="white",
).pack(anchor="w", padx=20, pady=(15, 4))

tk.Label(
    root,
    text=(
        "Knowledge Base • STV • Deduction • Induction • "
        "Abduction • Revision • Forward and Backward Chaining"
    ),
    font=("Arial", 10),
    bg="#101827",
    fg="#aeb9cc",
).pack(anchor="w", padx=20, pady=(0, 12))


# ---------------- Operation and input selectors ----------------

input_frame = tk.LabelFrame(
    root,
    text="Select Operation and Inputs",
    bg="#101827",
    fg="white",
    padx=10,
    pady=8,
)

input_frame.pack(fill=tk.X, padx=18, pady=4)

operation_var = tk.StringVar(value="Deduction")
depth_var = tk.StringVar(value="3")


tk.Label(
    input_frame,
    text="Operation:",
    bg="#101827",
    fg="white",
).grid(row=0, column=0, padx=5, pady=5, sticky="w")

ttk.Combobox(
    input_frame,
    textvariable=operation_var,
    values=list(OPERATIONS.keys()),
    state="readonly",
    width=16,
).grid(row=0, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Fact / input 1:",
    bg="#101827",
    fg="white",
).grid(row=0, column=2, padx=5, pady=5, sticky="w")

fact1_combo = ttk.Combobox(
    input_frame,
    state="readonly",
    width=34,
)

fact1_combo.grid(row=0, column=3, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Fact / input 2:",
    bg="#101827",
    fg="white",
).grid(row=1, column=0, padx=5, pady=5, sticky="w")

fact2_combo = ttk.Combobox(
    input_frame,
    state="readonly",
    width=34,
)

fact2_combo.grid(row=1, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Rule (for abduction):",
    bg="#101827",
    fg="white",
).grid(row=1, column=2, padx=5, pady=5, sticky="w")

rule_combo = ttk.Combobox(
    input_frame,
    state="readonly",
    width=30,
)

rule_combo.grid(row=1, column=3, padx=5, pady=5, sticky="w")


tk.Label(
    input_frame,
    text="Backward goal:",
    bg="#101827",
    fg="white",
).grid(row=2, column=0, padx=5, pady=5, sticky="w")

goal_combo = ttk.Combobox(
    input_frame,
    state="readonly",
    width=34,
)

goal_combo.grid(row=2, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Search depth:",
    bg="#101827",
    fg="white",
).grid(row=2, column=2, padx=5, pady=5, sticky="w")

ttk.Combobox(
    input_frame,
    textvariable=depth_var,
    values=["0", "1", "2", "3", "4", "5", "6", "7"],
    state="readonly",
    width=8,
).grid(row=2, column=3, padx=5, pady=5, sticky="w")


# ---------------- Main operation buttons -----------------------

action_frame = tk.LabelFrame(
    root,
    text="Run Reasoning",
    bg="#101827",
    fg="white",
    padx=10,
    pady=8,
)

action_frame.pack(fill=tk.X, padx=18, pady=4)

actions = [
    ("Run Selected Operation", run_selected_operation),
    ("Forward Chaining", run_forward),
    ("Backward Chaining", run_backward),
    ("Show All Facts + STVs", show_all_facts),
    ("Show All Rules", show_all_rules),
    ("Refresh Selectors", refresh_selectors),
]

for index, (label, callback) in enumerate(actions):
    ttk.Button(
        action_frame,
        text=label,
        command=callback,
    ).grid(
        row=index // 3,
        column=index % 3,
        padx=5,
        pady=5,
        sticky="ew",
    )

for column in range(3):
    action_frame.columnconfigure(column, weight=1)


# ---------------- Revision controls ----------------------------

revision_frame = tk.LabelFrame(
    root,
    text="Revision Inputs",
    bg="#101827",
    fg="white",
    padx=10,
    pady=8,
)

revision_frame.pack(fill=tk.X, padx=18, pady=4)


tk.Label(
    revision_frame,
    text="Existing proposition:",
    bg="#101827",
    fg="white",
).grid(row=0, column=0, padx=5, pady=5)

revision_target_combo = ttk.Combobox(
    revision_frame,
    state="readonly",
    width=34,
)

revision_target_combo.grid(row=0, column=1, padx=5, pady=5)


tk.Label(
    revision_frame,
    text="New evidence source:",
    bg="#101827",
    fg="white",
).grid(row=0, column=2, padx=5, pady=5)

evidence_combo = ttk.Combobox(
    revision_frame,
    state="readonly",
    width=34,
)

evidence_combo.grid(row=0, column=3, padx=5, pady=5)


new_evidence_strength_var = tk.StringVar()
new_evidence_confidence_var = tk.StringVar()


tk.Label(
    revision_frame,
    text="New evidence strength:",
    bg="#101827",
    fg="white",
).grid(row=1, column=0, padx=5, pady=5, sticky="w")

ttk.Entry(
    revision_frame,
    textvariable=new_evidence_strength_var,
    width=12,
).grid(row=1, column=1, padx=5, pady=5, sticky="w")


tk.Label(
    revision_frame,
    text="New evidence confidence:",
    bg="#101827",
    fg="white",
).grid(row=1, column=2, padx=5, pady=5, sticky="w")

ttk.Entry(
    revision_frame,
    textvariable=new_evidence_confidence_var,
    width=12,
).grid(row=1, column=3, padx=5, pady=5, sticky="w")


def run_revision_from_controls():
    operation_var.set("Revision")
    fact1_combo.set(revision_target_combo.get())
    fact2_combo.set(evidence_combo.get())

    run_selected_operation()


ttk.Button(
    revision_frame,
    text="Run Revision",
    command=run_revision_from_controls,
).grid(row=0, column=4, padx=5, pady=5)


# ---------------- Source buttons --------------------------------

source_frame = tk.Frame(root, bg="#101827")
source_frame.pack(pady=5)

ttk.Button(
    source_frame,
    text="View Knowledge-Base Source",
    command=show_knowledge_source,
).grid(row=0, column=0, padx=5)

ttk.Button(
    source_frame,
    text="View MeTTa Engine Source",
    command=show_engine_source,
).grid(row=0, column=1, padx=5)


# ---------------- Output panel ----------------------------------

output = ScrolledText(
    root,
    font=("DejaVu Sans Mono", 10),
    bg="#0b1220",
    fg="#e5e7eb",
    insertbackground="white",
    wrap=tk.WORD,
    height=24,
)

output.pack(
    fill=tk.BOTH,
    expand=True,
    padx=18,
    pady=(8, 16),
)

output.configure(state=tk.DISABLED)


show_output(
    "AGRICULTURAL PLN REASONING ENGINE",
    f"Loaded facts: {len(facts)}\n"
    f"Loaded rules: {len(rules)}\n\n"
    "1. Select an operation and its inputs.\n"
    "2. Deduction and induction automatically match a rule "
    "from the selected premises.\n"
    "3. Abduction uses the selected explanatory rule and "
    "shows its premises.\n"
    "4. Backward chaining starts from the selected goal and "
    "searches the loaded rules dynamically.\n"
    "5. Revision accepts new evidence strength and confidence.\n"
    "6. Derived STVs remain available in this GUI session.\n\n"
    "Important: session-derived STVs are not persisted to "
    "the source files."
)

refresh_selectors()

root.mainloop()