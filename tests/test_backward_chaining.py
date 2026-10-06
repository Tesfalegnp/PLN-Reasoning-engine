import pytest
from src.pln_engine.runner import PLNRunner

@pytest.fixture(scope="module")
def runner():
    return PLNRunner()

def test_bc_case_a_direct_fact(runner):
    """Case A: Direct fact retrieval from the agricultural knowledge base."""
    res = runner.run_backward_chaining(
        target_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    assert len(res.derivations) >= 1
    d = res.derivations[0]
    assert d.statement.predicate == "HasSymptom"
    assert "CoffeePlant01" in d.statement.arguments
    assert pytest.approx(d.truth_value.strength, 0.01) == 0.88
    assert pytest.approx(d.truth_value.confidence, 0.01) == 0.85
    assert d.proof_tree is not None
    assert d.proof_tree.node_type == "Fact"

def test_bc_case_b_one_rule(runner):
    """Case B: One-step goal resolution via Modus Ponens: HasSymptom -> AfflictedWith."""
    res = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant01 CoffeeLeafRust)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    assert len(res.derivations) >= 1
    d = res.derivations[0]
    assert d.statement.predicate == "AfflictedWith"
    assert "CoffeeLeafRust" in d.statement.arguments
    assert pytest.approx(d.truth_value.strength, 0.01) == 0.8384
    assert pytest.approx(d.truth_value.confidence, 0.01) == 0.6395
    assert d.proof_tree is not None
    assert d.proof_tree.node_type == "Rule"
    assert d.proof_tree.rule_name == "mp"

def test_bc_case_c_multi_step(runner):
    """Case C: Multi-step goal resolution: HasSymptom -> AfflictedWith -> RequiresTreatment."""
    res = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant01 CopperFungicideSpray)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    assert len(res.derivations) >= 1
    d = res.derivations[0]
    assert d.statement.predicate == "RequiresTreatment"
    assert "CopperFungicideSpray" in d.statement.arguments
    assert d.proof_tree is not None
    assert d.proof_tree.node_type == "Rule"

def test_bc_case_d_missing_fact(runner):
    """Case D: Missing fact / unprovable goal returns clean failure."""
    res = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant04 CoffeeBerryDisease)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert res.success is False
    assert len(res.derivations) == 0

def test_bc_case_e_multiple_proofs(runner):
    """Case E: Target with multiple valid inference pathways in knowledge base."""
    # (RequiresTreatment CoffeePlant01 CopperFungicideSpray) has 2 derivations:
    # 1. via sequential Modus Ponens
    # 2. via Implication Deduction followed by Modus Ponens
    res = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant01 CopperFungicideSpray)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    assert len(res.derivations) == 2
    rule_types = [d.proof_tree.children[1].node_type for d in res.derivations]
    assert "Fact" in rule_types or "Rule" in rule_types

def test_bc_case_f_cycles(runner):
    """Case F: Cyclic rules terminate cleanly under Peano depth bounds."""
    cyclic_script = """
    (: Nat Type)
    (: Z Nat)
    (: S (-> Nat Nat))
    (: stv (-> Number Number TruthValue))

    (= (Truth_Apply_Rule2 mp (stv $s1 $c1) (stv $s2 $c2))
       (stv (* $s1 $s2) (* $c1 $c2)))

    (= (kb) (superpose (
       (⊢ (RustRisk PlantX) (stv 0.9 0.8))
       (⊢ (→ (RustRisk $p) (RustSeverity $p)) (stv 0.9 0.8))
       (⊢ (→ (RustSeverity $p) (RustRisk $p)) (stv 0.9 0.8))
    )))

    (= (rb) (rule mp $p (→ $p $q) $q))

    (= (bc (⊢ $concl $tv) $depth)
       (let (⊢ $concl $tv) (kb)
         (Proof (⊢ $concl $tv) (Fact $concl))))

    (= (bc (⊢ $concl $tv) (S $k))
       (let* (((rule mp $p (→ $p $concl) $concl) (rb))
              ((Proof (⊢ (→ $p $concl) $tvImp) $subImp) (bc (⊢ (→ $p $concl) $tvImp) $k))
              ((Proof (⊢ $p $tvP) $subP) (bc (⊢ $p $tvP) $k))
              ($tv (Truth_Apply_Rule2 mp $tvP $tvImp)))
         (Proof (⊢ $concl $tv) (Rule mp $subP $subImp))))

    !(bc (⊢ (RustSeverity PlantX) $tv) (S (S Z)))
    """
    res = runner.execute_raw_metta(cyclic_script)
    assert len(res) > 0
    assert len(res[0]) > 0
    assert "Proof" in str(res[0][0])

def test_bc_case_g_truth_value_propagation(runner):
    """Case G: Derived STV depends quantitatively on actual premise STVs."""
    res = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant01 CoffeeLeafRust)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    d = res.derivations[0]
    # HasSymptom: (0.88, 0.85); Implication: (0.95, 0.90)
    # s = 0.88*0.95 + 0.02*(1-0.88) = 0.8384
    # c = 0.88*0.95 * 0.85*0.90 = 0.63954
    assert pytest.approx(d.truth_value.strength, 0.001) == 0.8384
    assert pytest.approx(d.truth_value.confidence, 0.001) == 0.6395
