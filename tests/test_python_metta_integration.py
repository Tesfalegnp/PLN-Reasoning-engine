import pytest
from src.pln_engine.runner import PLNRunner
from src.pln_engine.models import TruthValue, QueryResult, DerivationResult, ProofNode

@pytest.fixture
def runner():
    return PLNRunner()

def test_pipeline_backward_chaining(runner):
    """Verify complete pipeline: Python -> Hyperon -> MeTTa -> BC -> Parser -> Model."""
    # 1. Python triggers query
    res = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant01 CopperFungicideSpray)",
        depth=2,
        kb_name="coffee_agriculture"
    )

    # 2. Assert structured QueryResult model
    assert isinstance(res, QueryResult)
    assert res.mode == "backward_chaining"
    assert res.success is True
    assert res.execution_time_ms > 0

    # 3. Assert DerivationResult models
    assert len(res.derivations) >= 1
    d = res.derivations[0]
    assert isinstance(d, DerivationResult)
    assert isinstance(d.truth_value, TruthValue)
    assert d.truth_value.strength > 0
    assert d.truth_value.confidence > 0

    # 4. Assert ProofNode hierarchy
    assert isinstance(d.proof_tree, ProofNode)
    assert d.proof_tree.node_type == "Rule"
    assert len(d.proof_tree.children) > 0

def test_pipeline_forward_chaining(runner):
    """Verify complete pipeline: Python -> Hyperon -> MeTTa -> FC -> Parser -> Model."""
    res = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        depth=2,
        kb_name="coffee_agriculture"
    )

    assert isinstance(res, QueryResult)
    assert res.mode == "forward_chaining"
    assert res.success is True
    assert len(res.derivations) >= 2

def test_pipeline_pln_revision(runner):
    """Verify complete pipeline: Python -> Hyperon -> MeTTa -> Truth_Revision -> Parser -> TruthValue."""
    tv1 = TruthValue(0.85, 0.75)
    tv2 = TruthValue(0.20, 0.70)
    rev = runner.run_revision(tv1, tv2)

    assert isinstance(rev, TruthValue)
    assert abs(rev.strength - 0.5656) < 0.01
    assert abs(rev.confidence - 0.8421) < 0.01

def test_pipeline_raw_metta_passthrough(runner):
    """Verify raw MeTTa passthrough without Python interception."""
    res = runner.execute_raw_metta("!(+ 40 2)")
    assert len(res) > 0
    assert str(res[0][0]) == "42"

def test_to_dict_serialization(runner):
    """Verify serialization to dict for Streamlit and REST compatibility."""
    res = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant01 CoffeeLeafRust)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    d_dict = res.to_dict()
    assert isinstance(d_dict, dict)
    assert d_dict["success"] is True
    assert "derivations" in d_dict
    assert len(d_dict["derivations"]) >= 1
