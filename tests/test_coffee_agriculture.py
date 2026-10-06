import pytest
from src.pln_engine.runner import PLNRunner
from src.pln_engine.models import TruthValue

@pytest.fixture(scope="module")
def runner():
    return PLNRunner()

def test_coffee_bc_direct_fact(runner):
    """Case A: Direct fact query in Coffee Agriculture KB."""
    result = runner.run_backward_chaining(
        target_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert result.success is True
    assert len(result.derivations) >= 1
    d = result.derivations[0]
    assert abs(d.truth_value.strength - 0.88) < 0.01
    assert abs(d.truth_value.confidence - 0.85) < 0.01
    assert d.proof_tree is not None
    assert d.proof_tree.node_type == "Fact"

def test_coffee_bc_single_step_disease(runner):
    """Case B: 1-step backward chaining (Symptom -> Disease)."""
    result = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant01 CoffeeLeafRust)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert result.success is True
    assert len(result.derivations) >= 1
    d = result.derivations[0]
    assert "CoffeeLeafRust" in d.statement.raw
    assert d.truth_value.strength > 0.80
    assert d.truth_value.confidence > 0.50
    assert d.proof_tree.node_type == "Rule"
    assert d.proof_tree.rule_name == "mp"

def test_coffee_bc_two_step_treatment(runner):
    """Case C: 2-step backward chaining (Symptom -> Disease -> Treatment)."""
    result = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant01 CopperFungicideSpray)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert result.success is True
    assert len(result.derivations) >= 1
    d = result.derivations[0]
    assert "CopperFungicideSpray" in d.statement.raw
    assert d.truth_value.strength > 0.70
    assert d.proof_tree.node_type == "Rule"
    assert len(d.proof_tree.children) == 2

def test_coffee_berry_disease_pathway(runner):
    """Case D: Coffee Berry Disease (Colletotrichum) diagnostic and therapeutic pathway."""
    result = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant02 TargetedBerryFungicide)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert result.success is True
    assert len(result.derivations) >= 1
    assert any("TargetedBerryFungicide" in d.statement.raw for d in result.derivations)
    assert any(d.truth_value.strength > 0.60 for d in result.derivations)

def test_coffee_fc_derives_disease_and_treatment(runner):
    """Forward Chaining: Seed premise derives both disease and treatment."""
    result = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert result.success is True
    derived_raw = [d.statement.raw for d in result.derivations]
    assert any("CoffeeLeafRust" in s for s in derived_raw)
    assert any("CopperFungicideSpray" in s for s in derived_raw)

def test_coffee_nutrient_deficiency_pathway(runner):
    """Agronomic pathway: Chlorosis -> NitrogenDeficiency -> Fertilizer."""
    result = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant03 NitrogenFertilizer)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert result.success is True
    assert any("NitrogenFertilizer" in d.statement.raw for d in result.derivations)

def test_coffee_canopy_management_pathway(runner):
    """Agronomic cultural practice: Dense shaded canopy requires pruning."""
    result = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant01 CanopyPruning)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert result.success is True
    assert any("CanopyPruning" in d.statement.raw for d in result.derivations)
