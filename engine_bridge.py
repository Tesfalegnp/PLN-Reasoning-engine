"""
agri-pln-metta: Python-MeTTa Engine Bridge
Connects Python applications (CLI, Streamlit UI) directly to the MeTTa PLN reasoning engine.
All reasoning, STV math, and rule matching are executed natively by MeTTa.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

def find_metta_bin() -> str:
    """Locate the MeTTa binary in system PATH or local virtualenvs."""
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

def parse_metta_s_expr(text: str) -> List[Any]:
    """Parse raw MeTTa S-expression text into nested Python lists."""
    cleaned = re.sub(r'\[\(\)\]', '', text).strip()
    # Tokenize parentheses, quoted strings, and atom symbols
    tokens = re.findall(r'\(|\)|"[^"]*"|[^\s()]+', cleaned)
    
    def parse_tokens(toks: List[str]) -> List[Any]:
        res = []
        while toks:
            t = toks.pop(0)
            if t == '(':
                res.append(parse_tokens(toks))
            elif t == ')':
                return res
            else:
                try:
                    if '.' in t:
                        res.append(float(t))
                    else:
                        res.append(int(t))
                except ValueError:
                    res.append(t.strip('"'))
        return res
    
    return parse_tokens(tokens)

class AgriPLNEngine:
    """Bridge for querying the Agricultural PLN MeTTa Reasoning Engine."""
    
    def __init__(self, project_root: Optional[Path] = None):
        if project_root is None:
            self.project_root = Path(__file__).parent.resolve()
        else:
            self.project_root = Path(project_root).resolve()
        self.metta_bin = find_metta_bin()

    def run_raw_query(self, metta_code: str) -> Tuple[str, str, int]:
        """Execute a MeTTa code snippet with all knowledge and PLN modules loaded."""
        full_script = f"""
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

{metta_code}
"""
        tmp_file = self.project_root / ".tmp_bridge_query.metta"
        try:
            with open(tmp_file, "w") as f:
                f.write(full_script)
            proc = subprocess.run(
                [self.metta_bin, tmp_file.name],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=30
            )
            return proc.stdout, proc.stderr, proc.returncode
        finally:
            if tmp_file.exists():
                tmp_file.unlink()

    def query_forward_chaining(self, crop: str, condition: str, symptom: str) -> Dict[str, Any]:
        """Execute forward chaining inference from field observations."""
        query = f"!(forward-chain-full &self {crop} {condition} {symptom})"
        stdout, stderr, code = self.run_raw_query(query)
        
        # Regex extraction of calculated values
        strength_match = re.search(r'\(Diagnosis\s+\(Disease\s+([^\)]+)\)\s+\(STV\s+\(stv\s+([0-9\.]+)\s+([0-9\.]+)\)\)\)', stdout)
        treatment_matches = re.findall(r'\(Treatment\s+\(Action\s+([^\)]+)\)\s+\(STV\s+\(stv\s+([0-9\.]+)\s+([0-9\.]+)\)\)\)', stdout)
        
        disease = strength_match.group(1) if strength_match else "Unknown"
        diag_s = float(strength_match.group(2)) if strength_match else 0.0
        diag_c = float(strength_match.group(3)) if strength_match else 0.0
        
        treatments = []
        for t_name, t_s, t_c in treatment_matches:
            treatments.append({
                "action": t_name,
                "strength": float(t_s),
                "confidence": float(t_c)
            })
            
        return {
            "crop": crop,
            "condition": condition,
            "symptom": symptom,
            "disease": disease,
            "strength": diag_s,
            "confidence": diag_c,
            "treatments": treatments,
            "raw_output": stdout,
            "success": bool(strength_match)
        }

    def query_backward_chaining(self, crop: str, disease: str, condition: Optional[str], symptom: str) -> Dict[str, Any]:
        """Execute goal-driven backward chaining to verify a target disease."""
        if condition and condition != "None":
            query = f"!(backward-verify-goal-complete &self {crop} {disease} {condition} {symptom})"
        else:
            query = f"!(backward-verify-goal-incomplete &self {crop} {disease} {symptom})"
            
        stdout, stderr, code = self.run_raw_query(query)
        
        stv_match = re.search(r'\(GoalSTV\s+\(stv\s+([0-9\.]+)\s+([0-9\.]+)\)\)', stdout)
        status_match = re.search(r'\(GoalStatus\s+([^\)]+)\)', stdout)
        
        s = float(stv_match.group(1)) if stv_match else 0.0
        c = float(stv_match.group(2)) if stv_match else 0.0
        status = status_match.group(1) if status_match else "Unknown"
        
        return {
            "crop": crop,
            "disease": disease,
            "condition": condition,
            "symptom": symptom,
            "status": status,
            "strength": s,
            "confidence": c,
            "raw_output": stdout,
            "success": bool(stv_match)
        }

    def query_differential_diagnosis(self, crop: str, symptom: str) -> List[Dict[str, Any]]:
        """Run differential diagnosis for symptoms matching multiple candidate causes."""
        query = f"""
!(match &self (Susceptible {crop} $disease (stv $s_susc $c_susc))
   (match &self (Relation causes $disease {symptom} (stv $s_cause $c_cause))
     (match &self (PriorDisease $disease (stv $s_pri $c_pri))
       (let* (($tv_abd (formula-abduction (stv $s_cause $c_cause) (stv 0.90 0.85) (stv $s_pri $c_pri)))
              ($tv_fin (formula-deduction (stv $s_susc $c_susc) $tv_abd)))
         (DifferentialDiagnosis (Crop {crop}) (Symptom {symptom}) (HypothesizedCause $disease) (CalculatedSTV $tv_fin))))))
"""
        stdout, stderr, code = self.run_raw_query(query)
        matches = re.findall(r'\(HypothesizedCause\s+([^\)]+)\)\s+\(CalculatedSTV\s+\(stv\s+([0-9\.]+)\s+([0-9\.]+)\)\)', stdout)
        
        candidates = []
        for dis, s, c in matches:
            candidates.append({
                "disease": dis,
                "strength": float(s),
                "confidence": float(c)
            })
        return candidates

    def query_revision(self, prop: str, s1: float, c1: float, s2: float, c2: float, src1: str = "Scouting", src2: str = "LabPCR") -> Dict[str, Any]:
        """Fuse two evidence sources for a proposition using PLN Revision."""
        query = f"!(revise-evidence-sources {prop} {src1} (stv {s1} {c1}) {src2} (stv {s2} {c2}))"
        stdout, stderr, code = self.run_raw_query(query)
        
        stv_match = re.search(r'\(CombinedSTV\s+\(stv\s+([0-9\.]+)\s+([0-9\.]+)\)\)', stdout)
        s = float(stv_match.group(1)) if stv_match else 0.0
        c = float(stv_match.group(2)) if stv_match else 0.0
        
        return {
            "proposition": prop,
            "source1": {"name": src1, "strength": s1, "confidence": c1},
            "source2": {"name": src2, "strength": s2, "confidence": c2},
            "combined_strength": s,
            "combined_confidence": c,
            "raw_output": stdout
        }

    def query_3hop_chain(self) -> Dict[str, Any]:
        """Execute 3-hop causal reasoning: PoorDrainage -> WaterloggedSoil -> RootRot -> Wilting."""
        query = "!(chain-3-hop &self promotes PoorDrainage WaterloggedSoil increases-risk RootRot causes Wilting)"
        stdout, stderr, code = self.run_raw_query(query)
        stv_match = re.search(r'\(STV\s+\(stv\s+([0-9\.]+)\s+([0-9\.]+)\)\)', stdout)
        s = float(stv_match.group(1)) if stv_match else 0.0
        c = float(stv_match.group(2)) if stv_match else 0.0
        
        return {
            "path": "PoorDrainage -> WaterloggedSoil -> RootRot -> Wilting",
            "strength": s,
            "confidence": c,
            "raw_output": stdout
        }

    def query_induction(self, condition: str, disease: str, pos_cases: float, total_obs: float) -> Dict[str, Any]:
        """Induce generalized risk rule from survey observation counts."""
        query = f"!(induce-farm-risk-rule {condition} {disease} {pos_cases} {total_obs})"
        stdout, stderr, code = self.run_raw_query(query)
        stv_match = re.search(r'\(STV\s+\(stv\s+([0-9\.]+)\s+([0-9\.]+)\)\)', stdout)
        s = float(stv_match.group(1)) if stv_match else 0.0
        c = float(stv_match.group(2)) if stv_match else 0.0
        
        return {
            "condition": condition,
            "disease": disease,
            "positive_cases": pos_cases,
            "total_observations": total_obs,
            "strength": s,
            "confidence": c,
            "raw_output": stdout
        }
