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


# ============================================================
# FORMAT RESULT
# ============================================================

def format_result(result):
    if not result:
        return "No result returned."

    lines = []

    for item in result:
        lines.append(str(item))

    return "\n".join(lines)


# ============================================================
# RUN PLN DEDUCTION
# ============================================================

def run_deduction():
    output.delete("1.0", tk.END)

    try:
        code = """
        !(deduction
            (fact-stv (soil-dry))
            (fact-stv (temperature-high))
            (stv-value 0 0))
        """

        result = mt.run(code)

        output.insert(
            tk.END,
            "PLN DEDUCTION\n"
            "==============\n\n"
            "Premise 1:\n"
            "soil-dry\n\n"
            "Premise 2:\n"
            "temperature-high\n\n"
            "Conclusion:\n"
            "coffee-plant-water-stressed\n\n"
            "Truth-value calculation:\n"
            f"{format_result(result)}\n"
        )

    except Exception as error:
        output.insert(tk.END, f"ERROR:\n{error}")


# ============================================================
# RUN FORWARD CHAINING
# ============================================================

def run_forward():
    output.delete("1.0", tk.END)

    try:
        code = """
        !(forward-query
            (soil-dry)
            (agri-kb)
            (agri-rules)
            (fromNumber 4))
        """

        result = mt.run(code)

        output.insert(
            tk.END,
            "FORWARD CHAINING\n"
            "================\n\n"
            "Starting fact:\n"
            "soil-dry\n\n"
            "Direction:\n"
            "FACT → RULE → CONCLUSION → NEXT RULE\n\n"
            f"Engine result:\n{format_result(result)}\n"
        )

    except Exception as error:
        output.insert(tk.END, f"ERROR:\n{error}")


# ============================================================
# RUN BACKWARD CHAINING
# ============================================================

def run_backward():
    output.delete("1.0", tk.END)

    try:
        code = """
        !(backward-query
            (irrigate-coffee-plant)
            (agri-kb)
            (agri-rules)
            (fromNumber 5))
        """

        result = mt.run(code)

        output.insert(
            tk.END,
            "BACKWARD CHAINING\n"
            "=================\n\n"
            "Goal:\n"
            "irrigate-coffee-plant\n\n"
            "Direction:\n"
            "GOAL → REQUIRED PREMISES → FACTS\n\n"
            f"Engine result:\n{format_result(result)}\n"
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
        !(deduction
            (fact-stv (soil-dry))
            (fact-stv (temperature-high))
            (stv-value 0 0))

        !(deduction
            (stv-value 0.765 0.792)
            (fact-stv (water-available))
            (stv-value 0 0))

        !(backward-query
            (irrigate-coffee-plant)
            (agri-kb)
            (agri-rules)
            (fromNumber 5))
        """

        result = mt.run(code)

        output.insert(
            tk.END,
            "AGRICULTURAL PLN SCENARIO\n"
            "==========================\n\n"
            "Observed facts:\n"
            "  • Soil is dry\n"
            "  • Temperature is high\n"
            "  • Water is available\n"
            "  • Farmer can irrigate\n\n"
            "Reasoning chain:\n\n"
            "  soil-dry\n"
            "       +\n"
            "  temperature-high\n"
            "       ↓\n"
            "  coffee-plant-water-stressed\n"
            "       +\n"
            "  water-available\n"
            "       ↓\n"
            "  irrigation-recommended\n"
            "       +\n"
            "  farmer-can-irrigate\n"
            "       ↓\n"
            "  irrigate-coffee-plant\n\n"
            f"Engine output:\n{format_result(result)}\n"
        )

    except Exception as error:
        output.insert(tk.END, f"ERROR:\n{error}")


# ============================================================
# GUI
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


button_frame = tk.Frame(
    root,
    bg="#101827"
)

button_frame.pack(pady=10)


deduction_button = ttk.Button(
    button_frame,
    text="PLN Deduction",
    command=run_deduction
)

deduction_button.grid(
    row=0,
    column=0,
    padx=8
)


forward_button = ttk.Button(
    button_frame,
    text="Forward Chaining",
    command=run_forward
)

forward_button.grid(
    row=0,
    column=1,
    padx=8
)


backward_button = ttk.Button(
    button_frame,
    text="Backward Chaining",
    command=run_backward
)

backward_button.grid(
    row=0,
    column=2,
    padx=8
)


scenario_button = ttk.Button(
    button_frame,
    text="Run Agriculture Scenario",
    command=run_scenario
)

scenario_button.grid(
    row=0,
    column=3,
    padx=8
)


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

output.pack(
    padx=30,
    pady=25,
    fill=tk.BOTH,
    expand=True
)


root.mainloop()