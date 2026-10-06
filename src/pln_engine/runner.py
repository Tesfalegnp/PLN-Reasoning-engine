import os
import time
from typing import List, Dict, Optional, Any
import hyperon
from src.pln_engine.models import TruthValue, QueryResult, DerivationResult
from src.pln_engine.parser import parse_derivation_atom, parse_truth_value_from_str

class PLNRunner:
    """Official TrueAGI Hyperon runner orchestrating MeTTa PLN reasoning."""

    def __init__(self, project_root: Optional[str] = None):
        if project_root is None:
            # Default to directory containing project
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.project_root = project_root
        self.metta_dir = os.path.join(self.project_root, "metta")
        self.core_files = [
            os.path.join(self.metta_dir, "chaining/nat.metta"),
            os.path.join(self.metta_dir, "core/pln_tv.metta"),
            os.path.join(self.metta_dir, "core/pln_formulas.metta"),
            os.path.join(self.metta_dir, "rules/agriculture_rules.metta"),
        ]

    def _create_metta_instance(self) -> hyperon.MeTTa:
        """Instantiates a MeTTa runner with standard library environment."""
        env = hyperon.Environment.custom_env(
            working_dir=self.project_root,
            config_dir=""
        )
        runner = hyperon.MeTTa(env_builder=env)
        # Load core foundational modules
        for filepath in self.core_files:
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    runner.run(f.read())
            else:
                raise FileNotFoundError(f"Core MeTTa file missing: {filepath}")
        return runner

    def _int_to_peano(self, n: int) -> str:
        """Converts an integer to Peano Nat expression string, e.g. 2 -> (S (S Z))"""
        res = "Z"
        for _ in range(max(0, n)):
            res = f"(S {res})"
        return res

    def list_knowledge_bases(self) -> List[str]:
        """Lists available knowledge base names."""
        kb_dir = os.path.join(self.metta_dir, "kb")
        if not os.path.exists(kb_dir):
            return []
        kbs = []
        for fname in os.listdir(kb_dir):
            if fname.endswith(".metta"):
                kbs.append(fname[:-6])
        return sorted(kbs)

    def get_kb_content(self, kb_name: str) -> str:
        """Returns the raw content of a knowledge base."""
        filepath = os.path.join(self.metta_dir, "kb", f"{kb_name}.metta")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read()
        return ""

    def run_backward_chaining(
        self,
        target_statement: str,
        depth: int = 1,
        kb_name: str = "coffee_agriculture"
    ) -> QueryResult:
        """Executes depth-bounded Backward Chaining in MeTTa."""
        t0 = time.perf_counter()
        runner = self._create_metta_instance()

        # Load backward chaining engine
        bc_path = os.path.join(self.metta_dir, "chaining/bc.metta")
        with open(bc_path, "r") as f:
            runner.run(f.read())

        # Load chosen knowledge base
        kb_path = os.path.join(self.metta_dir, "kb", f"{kb_name}.metta")
        if not os.path.exists(kb_path):
            return QueryResult(
                mode="backward_chaining",
                target_query=target_statement,
                kb_name=kb_name,
                depth=depth,
                success=False,
                error_message=f"Knowledge base not found: {kb_name}"
            )

        with open(kb_path, "r") as f:
            runner.run(f.read())

        peano_depth = self._int_to_peano(depth)
        query = f"!(bc (⊢ {target_statement} $tv) {peano_depth})"

        try:
            raw_results = runner.run(query)
            t1 = time.perf_counter()
            exec_time = (t1 - t0) * 1000.0

            derivations: List[DerivationResult] = []
            seen_raw = set()

            for group in raw_results:
                for atom in group:
                    atom_str = str(atom).strip()
                    if atom_str and atom_str not in seen_raw:
                        seen_raw.add(atom_str)
                        d = parse_derivation_atom(atom_str)
                        if d:
                            derivations.append(d)

            return QueryResult(
                mode="backward_chaining",
                target_query=target_statement,
                kb_name=kb_name,
                depth=depth,
                success=len(derivations) > 0,
                derivations=derivations,
                execution_time_ms=exec_time
            )
        except Exception as e:
            t1 = time.perf_counter()
            return QueryResult(
                mode="backward_chaining",
                target_query=target_statement,
                kb_name=kb_name,
                depth=depth,
                success=False,
                error_message=str(e),
                execution_time_ms=(t1 - t0) * 1000.0
            )

    def run_forward_chaining(
        self,
        premise_statement: str,
        premise_tv: Optional[TruthValue] = None,
        depth: int = 1,
        kb_name: str = "coffee_agriculture"
    ) -> QueryResult:
        """Executes step-bounded Forward Chaining in MeTTa."""
        t0 = time.perf_counter()
        runner = self._create_metta_instance()

        fc_path = os.path.join(self.metta_dir, "chaining/fc.metta")
        with open(fc_path, "r") as f:
            runner.run(f.read())

        kb_path = os.path.join(self.metta_dir, "kb", f"{kb_name}.metta")
        if not os.path.exists(kb_path):
            return QueryResult(
                mode="forward_chaining",
                target_query=premise_statement,
                kb_name=kb_name,
                depth=depth,
                success=False,
                error_message=f"Knowledge base not found: {kb_name}"
            )

        with open(kb_path, "r") as f:
            runner.run(f.read())

        if premise_tv is None:
            premise_tv = TruthValue(1.0, 0.95)

        peano_depth = self._int_to_peano(depth)
        query = f"!(fc (⊢ {premise_statement} (stv {premise_tv.strength} {premise_tv.confidence})) {peano_depth})"

        try:
            raw_results = runner.run(query)
            t1 = time.perf_counter()
            exec_time = (t1 - t0) * 1000.0

            derivations: List[DerivationResult] = []
            seen_raw = set()

            for group in raw_results:
                for atom in group:
                    atom_str = str(atom).strip()
                    if atom_str and atom_str not in seen_raw:
                        seen_raw.add(atom_str)
                        d = parse_derivation_atom(atom_str)
                        if d:
                            derivations.append(d)

            return QueryResult(
                mode="forward_chaining",
                target_query=premise_statement,
                kb_name=kb_name,
                depth=depth,
                success=len(derivations) > 0,
                derivations=derivations,
                execution_time_ms=exec_time
            )
        except Exception as e:
            t1 = time.perf_counter()
            return QueryResult(
                mode="forward_chaining",
                target_query=premise_statement,
                kb_name=kb_name,
                depth=depth,
                success=False,
                error_message=str(e),
                execution_time_ms=(t1 - t0) * 1000.0
            )

    def run_revision(self, tv1: TruthValue, tv2: TruthValue) -> Optional[TruthValue]:
        """Calculates PLN Revision by calling MeTTa's Truth_Revision function."""
        runner = self._create_metta_instance()
        query = f"!(Truth_Revision (stv {tv1.strength} {tv1.confidence}) (stv {tv2.strength} {tv2.confidence}))"
        results = runner.run(query)
        for group in results:
            for atom in group:
                tv = parse_truth_value_from_str(str(atom))
                if tv:
                    return tv
        return None

    def execute_raw_metta(self, script: str) -> List[List[Any]]:
        """Executes arbitrary MeTTa code within initialized runner."""
        runner = self._create_metta_instance()
        return runner.run(script)
