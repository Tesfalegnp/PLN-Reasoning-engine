from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

@dataclass
class TruthValue:
    strength: float
    confidence: float

    def __repr__(self) -> str:
        return f"<STV s={self.strength:.4f}, c={self.confidence:.4f}>"

    def to_dict(self) -> Dict[str, float]:
        return {
            "strength": round(self.strength, 6),
            "confidence": round(self.confidence, 6)
        }

@dataclass
class Statement:
    raw: str
    predicate: str
    arguments: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return self.raw

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw": self.raw,
            "predicate": self.predicate,
            "arguments": self.arguments
        }

@dataclass
class ProofNode:
    node_type: str  # "Fact", "Rule", "Initial"
    statement: Statement
    truth_value: Optional[TruthValue] = None
    rule_name: Optional[str] = None
    children: List['ProofNode'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type,
            "statement": self.statement.to_dict() if self.statement else None,
            "truth_value": self.truth_value.to_dict() if self.truth_value else None,
            "rule": self.rule_name,
            "children": [c.to_dict() for c in self.children]
        }

@dataclass
class DerivationResult:
    statement: Statement
    truth_value: TruthValue
    proof_tree: Optional[ProofNode] = None
    raw_metta: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statement": self.statement.to_dict(),
            "truth_value": self.truth_value.to_dict(),
            "proof_tree": self.proof_tree.to_dict() if self.proof_tree else None,
            "raw_metta": self.raw_metta
        }

@dataclass
class QueryResult:
    mode: str  # "backward_chaining" or "forward_chaining"
    target_query: str
    kb_name: str
    depth: int
    success: bool
    derivations: List[DerivationResult] = field(default_factory=list)
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "query": self.target_query,
            "kb": self.kb_name,
            "depth": self.depth,
            "success": self.success,
            "derivations": [d.to_dict() for d in self.derivations],
            "execution_time_ms": round(self.execution_time_ms, 2),
            "error": self.error_message
        }
