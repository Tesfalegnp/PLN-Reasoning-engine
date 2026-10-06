import pytest
from src.pln_engine.parser import (
    parse_truth_value_from_str,
    parse_statement_from_str,
    parse_proof_tree_from_str,
    parse_derivation_atom
)

def test_parse_truth_value():
    tv = parse_truth_value_from_str("(stv 0.95 0.812)")
    assert tv is not None
    assert tv.strength == 0.95
    assert tv.confidence == 0.812

def test_parse_statement():
    s = parse_statement_from_str("(AfflictedWith CoffeePlant01 CoffeeLeafRust)")
    assert s.predicate == "AfflictedWith"
    assert s.arguments == ["CoffeePlant01", "CoffeeLeafRust"]

def test_parse_proof_tree():
    raw_tree = "(Rule mp (Fact (HasSymptom CoffeePlant01 OrangeRustPustules)) (Fact (→ (HasSymptom CoffeePlant01 OrangeRustPustules) (AfflictedWith CoffeePlant01 CoffeeLeafRust))))"
    node = parse_proof_tree_from_str(raw_tree)
    assert node is not None
    assert node.node_type == "Rule"
    assert node.rule_name == "mp"
    assert len(node.children) == 2
    assert node.children[0].node_type == "Fact"
    assert "CoffeePlant01" in node.children[0].statement.arguments

def test_parse_derivation_atom():
    raw = "(Proof (⊢ (RequiresTreatment CoffeePlant01 CopperFungicideSpray) (stv 0.77 0.43)) (Rule mp (Fact (AfflictedWith CoffeePlant01 CoffeeLeafRust)) (Fact (→ (AfflictedWith CoffeePlant01 CoffeeLeafRust) (RequiresTreatment CoffeePlant01 CopperFungicideSpray)))))"
    d = parse_derivation_atom(raw)
    assert d is not None
    assert d.truth_value.strength == 0.77
    assert d.statement.predicate == "RequiresTreatment"
    assert d.proof_tree is not None
    assert d.proof_tree.rule_name == "mp"
