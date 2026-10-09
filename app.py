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
        raise ValueError(f"Strength must be between 0 and 1: {strength}")

    if not 0.0 <= confidence <= 1.0:
        raise ValueError(
            f"Confidence must be between 0 and 1: {confidence}"
        )

    return strength, confidence


def stv_text(stv):
    return f"(stv {stv[0]:.6f} {stv[1]:.6f})"


def parse_stv(result):
    """
    Parse a truth value returned by the MeTTa runtime.

    Accepted result formats include:
        (stv-value 0.765 0.792)
        (stv 0.765 0.792)
    """
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
    """
    Load the knowledge base and the actual MeTTa implementations.

    Python reads fact/rule metadata to populate the UI. The inference
    operations themselves are executed by the MeTTa implementation.
    """
    global facts, rules

    fact_source = read_source(FACT_FILE)
    rule_source = read_source(RULE_FILE)
    pln_source = read_source(PLN_FILE)

    # Load the knowledge base and rule base.
    execute(fact_source)
    execute(rule_source)

    # Load the actual PLN operations.
    execute(pln_source)

    # Load both search engines.
    for path in CHAIN_FILES:
        execute(read_source(path))

    # Helper that queries stored fact truth values from AtomSpace.
    execute("""
    (= (fact-stv $fact)
        (match &self
            (: $id $fact (stv $s $c))
            (stv-value $s $c)))
    """)

    # Parse fact names and IDs from the knowledge-base source.
    # STVs are queried from MeTTa when an operation is executed.
    facts = {}

    for match in FACT_PATTERN.finditer(fact_source):
        fact_id, expression, strength, confidence = match.groups()

        facts[expression] = {
            "id": fact_id,
            "source_stv": validate_stv(strength, confidence),
        }

    # Parse rules from the actual rule file.
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
    """Ask the loaded MeTTa engine for an original fact's STV."""
    if expression not in facts:
        raise ValueError(f"Not an original knowledge-base fact: {expression}")

    result = execute(f"!(fact-stv {expression})")
    return parse_stv(result)


def get_stv(expression, prefer_derived=True):
    """
    Get a truth value.

    For a fact derived during this session, prefer the latest derived STV.
    When inspecting original evidence, prefer_derived=False returns the
    original STV from the loaded knowledge base.
    """
    if prefer_derived and expression in derived_facts:
        return derived_facts[expression]

    if expression in facts:
        return query_fact_stv(expression)

    if expression in derived_facts:
        return derived_facts[expression]

    raise ValueError(f"No STV is available for {expression}")


def all_expressions():
    """Facts, derived conclusions, and rule conclusions for selectors."""
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
    """Find a rule whose two premises match the selected facts."""
    for rule in rules:
        pair = {rule["premise1"], rule["premise2"]}

        if pair == {fact_a, fact_b}:
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
    Invoke the operation defined in engine/pln.metta.

    The formulas are not reimplemented in Python.
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
        "Check the MeTTa result, selected facts, and loaded rules."
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
    Save a derived result in the current GUI session.

    This does not modify agriculture.metta or insert a new atom into
    AtomSpace. It makes the derived STV available to later GUI operations.
    """
    derived_facts[expression] = stv

    reasoning_history.append({
        "expression": expression,
        "stv": stv,
        "description": description,
    })


# ============================================================
# GENERAL OPERATION TRACE
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
        rule = get_rule(selected_rule_id) if selected_rule_id else None

        section(lines, "STEP 1 — SELECTED OPERATION")
        row(lines, "Operation", operation)
        row(lines, "MeTTa function", OPERATIONS[operation])

        if operation in ("Deduction", "Induction"):
            stv_a = get_stv(fact_a)
            stv_b = get_stv(fact_b)

            section(lines, "STEP 2 — FIRST INPUT")
            row(lines, "Fact / conclusion", fact_a)
            show_stv(lines, "Input STV", stv_a)

            section(lines, "STEP 3 — SECOND INPUT")
            row(lines, "Fact / conclusion", fact_b)
            show_stv(lines, "Input STV", stv_b)

            matched = matching_rule(fact_a, fact_b)

            if matched:
                rule = matched

            section(lines, "STEP 4 — MATCHING RULE")
            if rule:
                rule_details(lines, rule)
            else:
                lines.append(
                    "No rule with these two premises was found."
                )
                lines.append(
                    "The selected two-input PLN operation can still run."
                )

            result = run_pln_operation(operation, stv_a, stv_b)

            if operation == "Deduction" and rule:
                derived_expression = rule["conclusion"]
                save_derived(
                    derived_expression,
                    result["stv"],
                    f"Deduction using {rule['id']}",
                )
            else:
                derived_expression = (
                    f"(derived-{operation.lower()} "
                    f"{fact_a} {fact_b})"
                )
                save_derived(
                    derived_expression,
                    result["stv"],
                    f"{operation} from selected inputs",
                )

            section(lines, "STEP 5 — METTA EXECUTION")
            row(lines, "Query", result["query"])
            row(lines, "Raw result", result["raw"])

            section(lines, "STEP 6 — RESULT")
            row(lines, "Derived expression", derived_expression)
            show_stv(lines, "Result STV", result["stv"])

            if operation == "Induction":
                row(lines, "Interpretation", "Evidence → Generalization")
            else:
                row(lines, "Interpretation", "Premises → Conclusion")

        elif operation == "Abduction":
            # For abduction, fact A is the observed conclusion.
            observed = fact_a
            observed_stv = get_stv(observed)

            # Prefer a rule that actually concludes the observation.
            candidates = rules_for_conclusion(observed)

            if candidates:
                rule = next(
                    (r for r in candidates if r["id"] == selected_rule_id),
                    candidates[0],
                )

            section(lines, "STEP 2 — OBSERVED FACT")
            row(lines, "Observed fact", observed)
            show_stv(lines, "Observed STV", observed_stv)

            section(lines, "STEP 3 — SELECTED EXPLANATORY RULE")
            if not rule:
                raise ValueError("Select a rule for abduction.")

            rule_details(lines, rule)

            if rule["conclusion"] != observed:
                lines.append(
                    "WARNING: the selected rule's conclusion differs "
                    "from the observed fact. Choose a matching rule "
                    "for a meaningful explanation."
                )

            # Abduction combines the observed STV with the rule STV
            # using the operation implemented by this project's PLN.
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

            section(lines, "STEP 4 — METTA EXECUTION")
            row(lines, "Query", result["query"])
            row(lines, "Raw result", result["raw"])

            section(lines, "STEP 5 — POSSIBLE EXPLANATION")
            row(lines, "Explanation", (
                f"{rule['premise1']} AND {rule['premise2']}"
            ))
            show_stv(lines, "Result STV", result["stv"])
            row(lines, "Direction", "Observed conclusion → Possible causes")

        elif operation == "Revision":
            # Revise the selected proposition using the manually entered
            # strength and confidence for the new evidence.
            existing_stv = get_stv(fact_a, prefer_derived=False)
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
                "Direction",
                "Existing evidence + New evidence → Revised STV",
            )

        refresh_selectors()
        show_output(f"{operation.upper()} — STEP-BY-STEP TRACE",
                    "\n".join(lines))

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

        show_output("FACTS AND STV VALUES", "\n".join(lines))

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

    show_output("RULES LOADED FROM rule.metta", "\n".join(lines))


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
            "Operations are executed using the loaded pln.metta functions.",
        ]

        frontier = {start}
        fired_rules = set()
        final_frontier = set()

        for depth in range(1, depth_limit + 1):
            section(lines, f"DEPTH {depth}")

            next_frontier = set()
            applied_this_depth = 0

            for rule in rules:
                if rule["id"] in fired_rules:
                    continue

                p1 = rule["premise1"]
                p2 = rule["premise2"]

                # A rule is relevant if at least one premise belongs
                # to the current frontier and both premises are known.
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

                row(lines, "Premise 1 STV", stv_text(stv1))
                row(lines, "Premise 2 STV", stv_text(stv2))

                result = run_pln_operation("Deduction", stv1, stv2)

                conclusion = rule["conclusion"]
                conclusion_stv = result["stv"]

                row(lines, "MeTTa query", result["query"])
                row(lines, "Raw result", result["raw"])

                # If the conclusion is already known, combine the
                # old and new evidence using the actual revision rule.
                if conclusion in available:
                    old_stv = available[conclusion]

                    lines.append("")
                    lines.append("Existing conclusion found.")
                    row(lines, "Previous STV", stv_text(old_stv))
                    row(lines, "New evidence STV", stv_text(conclusion_stv))

                    revision = run_pln_operation(
                        "Revision",
                        old_stv,
                        conclusion_stv,
                    )

                    row(lines, "Revision query", revision["query"])
                    row(lines, "Revised STV", stv_text(revision["stv"]))

                    conclusion_stv = revision["stv"]

                available[conclusion] = conclusion_stv
                derived_facts[conclusion] = conclusion_stv
                next_frontier.add(conclusion)

                row(lines, "Derived conclusion", conclusion)
                row(lines, "Conclusion STV", stv_text(conclusion_stv))

                fired_rules.add(rule["id"])
                applied_this_depth += 1

            final_frontier = next_frontier

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

        # Run the actual loaded MeTTa chaining function separately.
        engine_query = (
            f"!(forward-query {start} &self "
            f"(fromNumber {depth_limit}))"
        )

        section(lines, "RAW RESULT FROM forward_chain.metta")
        row(lines, "Query", engine_query)
        lines.append(format_result(execute(engine_query)))

        lines.extend([
            "",
            "STV TRACE NOTE",
            "The rule-by-rule STV calculations shown above call pln.metta.",
            "The existing forward_chain.metta search returns conclusions, "
            "but does not itself propagate STVs through every recursive step.",
        ])

        reasoning_history.append({
            "mode": "forward",
            "start": start,
            "depth": depth_limit,
        })

        show_output("FORWARD CHAINING — FULL TRACE", "\n".join(lines))
        refresh_selectors()

    except Exception as error:
        show_error("FORWARD CHAINING", error)


# ============================================================
# BACKWARD CHAINING — PROOF TRACE
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
        lines.append("This branch stops: the goal is already known.")
        return True, stv

    if remaining_depth <= 0:
        lines.append("STOP: search depth limit reached.")
        return False, None

    if goal in visited:
        lines.append("STOP: cycle detected.")
        return False, None

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
            lines.append("Rule failed: first premise was not proved.")
            continue

        ok2, stv2 = prove_goal(
            rule["premise2"],
            available,
            remaining_depth - 1,
            next_visited,
            lines,
        )

        if not ok2:
            lines.append("Rule failed: second premise was not proved.")
            continue

        section(lines, f"CALCULATE CONCLUSION STV — {rule['id']}")

        row(lines, "Premise 1", rule["premise1"])
        show_stv(lines, "Premise 1 STV", stv1)

        row(lines, "Premise 2", rule["premise2"])
        show_stv(lines, "Premise 2 STV", stv2)

        result = run_pln_operation("Deduction", stv1, stv2)

        row(lines, "MeTTa query", result["query"])
        row(lines, "Raw result", result["raw"])

        conclusion_stv = result["stv"]

        # Incorporate the rule's own truth value using the same PLN
        # operation implementation, making the extra step explicit.
        rule_result = run_pln_operation(
            "Deduction",
            conclusion_stv,
            rule["stv"],
        )

        row(lines, "Rule-combination query", rule_result["query"])
        show_stv(lines, "Derived conclusion STV", rule_result["stv"])

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
            "Backward chaining starts from the target and searches",
            "for rules that can prove it.",
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

        # Also execute the project's own backward chaining definition.
        engine_query = (
            f"!(backward-query {goal} &self "
            f"(fromNumber {depth_limit}))"
        )

        section(lines, "RAW RESULT FROM backward_chain.metta")
        row(lines, "Query", engine_query)
        lines.append(format_result(execute(engine_query)))

        reasoning_history.append({
            "mode": "backward",
            "goal": goal,
            "depth": depth_limit,
            "success": success,
        })

        show_output("BACKWARD CHAINING — FULL TRACE", "\n".join(lines))
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
            section(lines, str(path.relative_to(BASE_DIR)))
            lines.append(read_source(path))

        show_output("ACTUAL METTA ENGINE SOURCE", "\n".join(lines))

    except Exception as error:
        show_error("ENGINE SOURCE", error)


def show_knowledge_source():
    try:
        lines = []

        for path in [FACT_FILE, RULE_FILE]:
            section(lines, str(path.relative_to(BASE_DIR)))
            lines.append(read_source(path))

        show_output("ACTUAL KNOWLEDGE-BASE SOURCE", "\n".join(lines))

    except Exception as error:
        show_error("KNOWLEDGE BASE", error)


# ============================================================
# GUI
# ============================================================

try:
    load_project()
except Exception as error:
    raise SystemExit(f"Could not initialize the MeTTa engine:\n{error}")


root = tk.Tk()
root.title("Agricultural PLN Reasoning Engine")
root.geometry("1250x900")
root.configure(bg="#101827")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6)
style.configure("TCombobox", padding=4)

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
        "Knowledge Base • STV • Deduction • Induction • Abduction "
        "• Revision • Forward and Backward Chaining"
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
    text="Rule:",
    bg="#101827",
    fg="white",
).grid(row=1, column=2, padx=5, pady=5, sticky="w")

rule_combo = ttk.Combobox(
    input_frame,
    state="readonly",
    width=16,
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

# The new evidence STV is entered here; both values must be between 0 and 1.
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
    # Reuse the general operation handler with the selected proposition
    # and the manually entered new-evidence strength/confidence.
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
    "2. Run the operation to see each input STV and the MeTTa result.\n"
    "3. Select a rule to inspect its premises, conclusion, and rule STV.\n"
    "4. Use Forward or Backward Chaining to inspect a reasoning trace.\n"
    "5. Derived STVs remain available in this GUI session.\n\n"
    "Important: session-derived STVs are not persisted to the source files."
)

refresh_selectors()
root.mainloop()