#!/usr/bin/env python3
"""
agri-pln-metta: Command Line Interface
Provides an interactive and scripted CLI for querying the Agricultural PLN Reasoning Engine.
"""

import sys
import os
import re
import argparse
import subprocess
import shutil
from pathlib import Path

def find_metta_bin():
    p = shutil.which("metta")
    if p:
        return p
    candidates = [
        "/home/hope/Projects/pln_engin_project/.venv-metta/bin/metta",
        str(Path.home() / ".cargo/bin/metta"),
        str(Path.home() / ".local/bin/metta"),
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return "metta"

def run_metta_script(script_path, cwd=None):
    metta_bin = find_metta_bin()
    if cwd is None:
        cwd = os.path.dirname(os.path.abspath(script_path))
    cmd = [metta_bin, os.path.basename(script_path)]
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return proc.stdout, proc.stderr, proc.returncode

def run_inline_query(metta_query, project_root):
    metta_bin = find_metta_bin()
    script = f"""
!(register-module! knowledge)
!(register-module! pln)

!(import! &self knowledge:agriculture_kb)
!(import! &self pln:stv)
!(import! &self pln:formulas)
!(import! &self pln:deduction)
!(import! &self pln:induction)
!(import! &self pln:abduction)
!(import! &self pln:revision)
!(import! &self pln:chaining)
!(import! &self pln:forward)
!(import! &self pln:backward)

!{metta_query}
"""
    tmp_path = project_root / ".tmp_query.metta"
    try:
        with open(tmp_path, "w") as f:
            f.write(script)
        stdout, stderr, code = run_metta_script(str(tmp_path), cwd=str(project_root))
        return stdout
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

def print_banner():
    print("=" * 80)
    print(" 🌾 agri-pln-metta: Agricultural Probabilistic Logic Network Engine")
    print("    Hyperon MeTTa Domain-Specific Probabilistic Reasoning System")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(
        description="agri-pln-metta: Agricultural Probabilistic Logic Network Reasoning Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 1. demo
    subparsers.add_parser("demo", help="Run the full interactive MeTTa demonstration")
    
    # 2. test
    subparsers.add_parser("test", help="Run all automated unit and integration test suites")
    
    # 3. forward
    fwd_parser = subparsers.add_parser("forward", help="Run forward chaining diagnosis")
    fwd_parser.add_argument("--crop", default="Coffee", help="Observed crop (e.g. Coffee, Maize, Tomato)")
    fwd_parser.add_argument("--condition", default="HighHumidity", help="Observed environmental condition")
    fwd_parser.add_argument("--symptom", default="OrangeLeafSpots", help="Observed symptom")
    
    # 4. backward
    bwd_parser = subparsers.add_parser("backward", help="Run goal-driven backward chaining")
    bwd_parser.add_argument("--crop", default="Coffee", help="Target crop")
    bwd_parser.add_argument("--disease", default="CoffeeLeafRust", help="Target disease hypothesis")
    bwd_parser.add_argument("--condition", default="HighHumidity", help="Observed condition (or None)")
    bwd_parser.add_argument("--symptom", default="OrangeLeafSpots", help="Observed symptom")
    
    # 5. revise
    rev_parser = subparsers.add_parser("revise", help="Revise two evidence sources for a proposition")
    rev_parser.add_argument("--prop", default="CoffeeLeafRust", help="Proposition name")
    rev_parser.add_argument("--s1", type=float, default=0.85, help="Strength 1")
    rev_parser.add_argument("--c1", type=float, default=0.70, help="Confidence 1")
    rev_parser.add_argument("--s2", type=float, default=0.95, help="Strength 2")
    rev_parser.add_argument("--c2", type=float, default=0.90, help="Confidence 2")
    
    # 6. scenarios
    subparsers.add_parser("scenarios", help="Run all 7 evaluation scenarios")

    args = parser.parse_args()
    project_root = Path(__file__).parent.resolve()
    
    print_banner()
    
    if args.command == "demo" or args.command is None:
        demo_file = project_root / "demo.metta"
        print("[+] Running agri-pln-metta Demonstration...\n")
        out, err, code = run_metta_script(str(demo_file), cwd=str(project_root))
        print(out)
        if err:
            print(f"Error: {err}", file=sys.stderr)
            
    elif args.command == "test":
        subprocess.run([sys.executable, str(project_root / "runner.py")])
        
    elif args.command == "forward":
        query = f"(forward-chain-full &self {args.crop} {args.condition} {args.symptom})"
        print(f"\n[+] Executing Forward Chaining Pipeline:")
        print(f"    - Crop: {args.crop}")
        print(f"    - Environmental Condition: {args.condition}")
        print(f"    - Foliar Symptom: {args.symptom}\n")
        res = run_inline_query(query, project_root)
        print("--- MeTTa Engine Result ---")
        print(res)
        
    elif args.command == "backward":
        if args.condition and args.condition != "None":
            query = f"(backward-verify-goal-complete &self {args.crop} {args.disease} {args.condition} {args.symptom})"
        else:
            query = f"(backward-verify-goal-incomplete &self {args.crop} {args.disease} {args.symptom})"
        print(f"\n[+] Executing Goal-Driven Backward Search for: {args.disease} on {args.crop}\n")
        res = run_inline_query(query, project_root)
        print("--- MeTTa Engine Result ---")
        print(res)
        
    elif args.command == "revise":
        query = f"(revise-evidence-sources {args.prop} FieldScouting (stv {args.s1} {args.c1}) LaboratoryPCR (stv {args.s2} {args.c2}))"
        print(f"\n[+] Executing Probabilistic Revision for Proposition: {args.prop}")
        print(f"    - Source 1 (Field Scouting): s={args.s1}, c={args.c1}")
        print(f"    - Source 2 (Laboratory PCR): s={args.s2}, c={args.c2}\n")
        res = run_inline_query(query, project_root)
        print("--- MeTTa Engine Result ---")
        print(res)
        
    elif args.command == "scenarios":
        scenarios_file = project_root / "queries" / "scenarios.metta"
        query = "(run-all-scenarios)"
        print("\n[+] Executing All 7 Required Evaluation Scenarios in MeTTa...\n")
        res = run_inline_query(query, project_root)
        print("--- MeTTa Engine Result ---")
        print(res)

if __name__ == "__main__":
    main()
