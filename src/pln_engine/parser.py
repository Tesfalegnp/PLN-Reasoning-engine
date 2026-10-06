import re
from typing import Optional, List, Any
from src.pln_engine.models import TruthValue, Statement, ProofNode, DerivationResult

def parse_truth_value_from_str(s: str) -> Optional[TruthValue]:
    """Extracts (stv strength confidence) from string."""
    m = re.search(r'\(stv\s+([0-9\.\-e]+)\s+([0-9\.\-e]+)\)', s)
    if m:
        try:
            return TruthValue(float(m.group(1)), float(m.group(2)))
        except ValueError:
            return None
    return None

def parse_statement_from_str(s: str) -> Statement:
    """Parses MeTTa logic expression like (HasSymptom CoffeePlant01 OrangeRustPustules) or (→ ...)"""
    cleaned = s.strip()
    # Remove leading ⊢ and outer parentheses if present
    if cleaned.startswith('(⊢'):
        # extract conclusion inside (⊢ concl tv)
        inner = re.sub(r'^\(⊢\s+', '', cleaned)
        # remove trailing tv and paren
        inner = re.sub(r'\(stv\s+[^)]+\)\)$', '', inner).strip()
        cleaned = inner

    # Extract predicate and arguments
    if cleaned.startswith('(') and cleaned.endswith(')'):
        tokens = []
        depth = 0
        current = []
        for char in cleaned[1:-1].strip():
            if char == '(':
                depth += 1
                current.append(char)
            elif char == ')':
                depth -= 1
                current.append(char)
            elif char.isspace() and depth == 0:
                if current:
                    tokens.append("".join(current))
                    current = []
            else:
                current.append(char)
        if current:
            tokens.append("".join(current))
        if tokens:
            pred = tokens[0]
            args = tokens[1:]
            return Statement(raw=cleaned, predicate=pred, arguments=args)

    return Statement(raw=cleaned, predicate=cleaned, arguments=[])

def parse_proof_tree_from_str(s: str) -> Optional[ProofNode]:
    """Recursively parse (Rule rule_name sub1 sub2) or (Fact fact) or (Initial init)"""
    s = s.strip()
    if s.startswith('(Fact'):
        inner = s[5:-1].strip()
        stmt = parse_statement_from_str(inner)
        return ProofNode(node_type="Fact", statement=stmt)
    
    if s.startswith('(Initial'):
        inner = s[8:-1].strip()
        stmt = parse_statement_from_str(inner)
        return ProofNode(node_type="Initial", statement=stmt)

    if s.startswith('(Rule'):
        body = s[5:-1].strip()
        # Extract rule name (first token)
        parts = body.split(None, 1)
        rule_name = parts[0] if parts else "unknown"
        rest = parts[1] if len(parts) > 1 else ""

        # Extract subproof children
        children = []
        depth = 0
        current = []
        for char in rest:
            if char == '(':
                depth += 1
                current.append(char)
            elif char == ')':
                depth -= 1
                current.append(char)
                if depth == 0:
                    child_str = "".join(current).strip()
                    child_node = parse_proof_tree_from_str(child_str)
                    if child_node:
                        children.append(child_node)
                    current = []
            elif depth > 0:
                current.append(char)

        return ProofNode(
            node_type="Rule",
            statement=Statement(raw="", predicate="", arguments=[]),
            rule_name=rule_name,
            children=children
        )
    return None

def parse_derivation_atom(atom_repr: str) -> Optional[DerivationResult]:
    """Parses a complete MeTTa Proof or Derivation expression string into DerivationResult."""
    s = str(atom_repr).strip()
    tv = parse_truth_value_from_str(s)
    if not tv:
        return None

    # Handle (Proof (⊢ $concl $tv) $proofTree)
    if s.startswith('(Proof'):
        # Extract the (⊢ $concl $tv) part
        m_concl = re.search(r'\(⊢\s+(.+?)\s+\(stv', s)
        concl_str = m_concl.group(1).strip() if m_concl else ""
        stmt = parse_statement_from_str(concl_str)

        # Extract the proof tree part: after the second top-level element
        # Match closing of (⊢ ...)
        idx = s.find('(⊢')
        if idx != -1:
            depth = 0
            end_concl = -1
            for i in range(idx, len(s)):
                if s[i] == '(':
                    depth += 1
                elif s[i] == ')':
                    depth -= 1
                    if depth == 0:
                        end_concl = i + 1
                        break
            if end_concl != -1:
                tree_str = s[end_concl:-1].strip()
                proof_tree = parse_proof_tree_from_str(tree_str)
            else:
                proof_tree = None
        else:
            proof_tree = None

        return DerivationResult(
            statement=stmt,
            truth_value=tv,
            proof_tree=proof_tree,
            raw_metta=s
        )

    # Handle (Derivation (⊢ $premise $tv) (Initial $premise))
    if s.startswith('(Derivation'):
        m_concl = re.search(r'\(⊢\s+(.+?)\s+\(stv', s)
        concl_str = m_concl.group(1).strip() if m_concl else ""
        stmt = parse_statement_from_str(concl_str)

        m_init = re.search(r'\(Initial\s+(.+?)\)\)$', s)
        init_str = m_init.group(1).strip() if m_init else ""
        init_stmt = parse_statement_from_str(init_str)
        proof_node = ProofNode(node_type="Initial", statement=init_stmt)

        return DerivationResult(
            statement=stmt,
            truth_value=tv,
            proof_tree=proof_node,
            raw_metta=s
        )

    # Fallback for plain (⊢ $concl $tv)
    if s.startswith('(⊢'):
        m_concl = re.search(r'\(⊢\s+(.+?)\s+\(stv', s)
        concl_str = m_concl.group(1).strip() if m_concl else s
        stmt = parse_statement_from_str(concl_str)
        return DerivationResult(
            statement=stmt,
            truth_value=tv,
            proof_tree=None,
            raw_metta=s
        )

    return None
