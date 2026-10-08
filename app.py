from hyperon import MeTTa
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import os


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
ENGINE_DIR = os.path.join(BASE_DIR, "engine")


# ============================================================
# INITIALIZE METTA
# ============================================================

mt = MeTTa()


# ============================================================
# LOAD PROJECT FILES
# ============================================================

def load_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def initialize_engine():
    files = [
        os.path.join(KNOWLEDGE_DIR, "agriculture.metta"),
        os.path.join(KNOWLEDGE_DIR, "rule.metta"),
        os.path.join(ENGINE_DIR, "pln.metta"),
        os.path.join(ENGINE_DIR, "forward_chain.metta"),
        os.path.join(ENGINE_DIR, "backward_chain.metta"),
    ]

    for path in files:
        code = load_file(path)
        mt.run(code)

    # Register AtomSpace helper function
    mt.run("""
    (= (fact-stv $fact)
        (match &self
            (: $id $fact (stv $s $c))
            (stv-value $s $c)))
    """)


# ============================================================
# FORMAT RESULT
# ============================================================

def format_result(result):
    if not result:
        return "No result returned from AtomSpace."

    lines = []
    for group in result:
        if isinstance(group, list):
            for item in group:
                lines.append(str(item))
        else:
            lines.append(str(group))

    return "\n".join(lines)


# ============================================================
# RUN PLN DEDUCTION
# ============================================================

def run_deduction():
    output.delete("1.0", tk.END)

    try:
        code = """
        !(let $a (fact-stv (soil-dry))
            (let $b (fact-stv (temperature-high))
                (deduction $a $b)))
        """

        result = mt.run(code)

        output.insert(
            tk.END,
            "PLN DEDUCTION\n"
            "==============\n\n"
            "Querying AtomSpace:\n"
            "  Fact 1: (soil-dry) -> (stv 0.90 0.90)\n"
            "  Fact 2: (temperature-high) -> (stv 0.85 0.88)\n\n"
            "Deduction Formula: s = s1 * s2, c = c1 * c2\n\n"
            f"AtomSpace Result:\n{format_result(result)}\n"
        )

    except Exception as error:
        output.insert(tk.END, f"ERROR:\n{error}")


# ============================================================
# RUN FORWARD CHAINING
# ============================================================

def run_forward():
    output.delete("1.0", tk.END)

    try:
        code = "!(forward-query (soil-dry) &self (fromNumber 3))"

        result = mt.run(code)

        output.insert(
            tk.END,
            "FORWARD CHAINING\n"
            "================\n\n"
            "Starting Fact:\n"
            "  (soil-dry)\n\n"
            "Direction:\n"
            "  Data-Driven Expansion (FACT -> RULE -> CONCLUSION)\n\n"
            f"Derived Conclusions from AtomSpace:\n{format_result(result)}\n"
        )

    except Exception as error:
        output.insert(tk.END, f"ERROR:\n{error}")


# ============================================================
# RUN BACKWARD CHAINING
# ============================================================

def run_backward():
    output.delete("1.0", tk.END)

    try:
        code = "!(backward-query (irrigate-coffee-plant) &self (fromNumber 3))"

        result = mt.run(code)

        output.insert(
            tk.END,
            "BACKWARD CHAINING\n"
            "=================\n\n"
            "Target Goal:\n"
            "  (irrigate-coffee-plant)\n\n"
            "Direction:\n"
            "  Goal-Driven Search (GOAL -> REQUIRED SUBGOALS -> FACTS)\n\n"
            f"Generated Proof Tree from AtomSpace:\n{format_result(result)}\n"
        )

    except Exception as error:
        output.insert(tk.END, f"ERROR:\n{error}")


# ============================================================
# RUN COMPLETE SCENARIO
# ============================================================

def run_scenario():
    output.delete("1.0", tk.END)

    try:
        code = """
        !(let $a (fact-stv (soil-dry))
            (let $b (fact-stv (temperature-high))
                (deduction $a $b)))

        !(let $ab (let $a (fact-stv (soil-dry))
                      (let $b (fact-stv (temperature-high))
                          (deduction $a $b)))
            (let $c (fact-stv (water-available))
                (deduction $ab $c)))

        !(backward-query (irrigate-coffee-plant) &self (fromNumber 3))
        """

        result = mt.run(code)

        output.insert(
            tk.END,
            "AGRICULTURAL PLN SCENARIO\n"
            "==========================\n\n"
            "Executing Multi-Step Agricultural Scenario on AtomSpace...\n\n"
            f"AtomSpace Execution Output:\n{format_result(result)}\n"
        )

    except Exception as error:
        output.insert(tk.END, f"ERROR:\n{error}")


# ============================================================
# GUI SETUP
# ============================================================

initialize_engine()

root = tk.Tk()
root.title("Agricultural PLN Reasoning Engine")
root.geometry("950x700")
root.configure(bg="#101827")

title = tk.Label(
    root,
    text="Agricultural PLN Reasoning Engine",
    font=("Arial", 22, "bold"),
    bg="#101827",
    fg="white"
)
title.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Probabilistic Logic Networks • MeTTa • Forward & Backward Chaining",
    font=("Arial", 11),
    bg="#101827",
    fg="#aeb9cc"
)
subtitle.pack(pady=(0, 20))

button_frame = tk.Frame(root, bg="#101827")
button_frame.pack(pady=10)

deduction_button = ttk.Button(
    button_frame,
    text="PLN Deduction",
    command=run_deduction
)
deduction_button.grid(row=0, column=0, padx=8)

forward_button = ttk.Button(
    button_frame,
    text="Forward Chaining",
    command=run_forward
)
forward_button.grid(row=0, column=1, padx=8)

backward_button = ttk.Button(
    button_frame,
    text="Backward Chaining",
    command=run_backward
)
backward_button.grid(row=0, column=2, padx=8)

scenario_button = ttk.Button(
    button_frame,
    text="Run Agriculture Scenario",
    command=run_scenario
)
scenario_button.grid(row=0, column=3, padx=8)

output = ScrolledText(
    root,
    width=110,
    height=30,
    font=("DejaVu Sans Mono", 11),
    bg="#0b1220",
    fg="#e5e7eb",
    insertbackground="white",
    wrap=tk.WORD
)
output.pack(padx=30, pady=25, fill=tk.BOTH, expand=True)

root.mainloop()