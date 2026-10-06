import pytest
from src.pln_engine.runner import PLNRunner
from src.pln_engine.models import TruthValue

@pytest.fixture(scope="module")
def runner():
    return PLNRunner()

def test_scout_conflicting_evidence_revision(runner):
    """
    Agricultural Scenario: Two field scouts inspect CoffeePlant01 for rust symptoms.
    - Scout A (Senior Agronomist): Rust pustules observed -> (stv 0.85 0.75)
    - Scout B (Field Assistant): Rust pustules not confirmed / negative -> (stv 0.20 0.70)
    PLN Revision pools evidence without discarding either observation.
    """
    tv_scout_a = TruthValue(0.85, 0.75)
    tv_scout_b = TruthValue(0.20, 0.70)

    fused_tv = runner.run_revision(tv_scout_a, tv_scout_b)

    assert fused_tv is not None
    # Strength should be between 0.20 and 0.85, weighted by evidence weight
    assert pytest.approx(fused_tv.strength, 0.01) == 0.5656
    # Confidence MUST be strictly greater than either individual confidence
    assert fused_tv.confidence > tv_scout_a.confidence
    assert fused_tv.confidence > tv_scout_b.confidence
    assert pytest.approx(fused_tv.confidence, 0.01) == 0.8421

def test_concordant_evidence_reinforcement(runner):
    """
    Agricultural Scenario: Two scouts both observe high humidity risk on CoffeePlant01.
    - Scout A: (stv 0.90 0.80)
    - Scout B: (stv 0.92 0.75)
    Belief should remain high while confidence substantially increases.
    """
    tv1 = TruthValue(0.90, 0.80)
    tv2 = TruthValue(0.92, 0.75)

    fused_tv = runner.run_revision(tv1, tv2)
    assert fused_tv is not None
    assert fused_tv.strength > 0.90
    assert fused_tv.confidence > 0.80
    assert fused_tv.confidence > 0.75

def test_three_way_field_evidence_pooling(runner):
    """Sequential revision of three field observation sensors."""
    tv1 = TruthValue(0.85, 0.70)
    tv2 = TruthValue(0.80, 0.60)
    tv3 = TruthValue(0.30, 0.50)

    step1 = runner.run_revision(tv1, tv2)
    assert step1 is not None
    final_tv = runner.run_revision(step1, tv3)
    assert final_tv is not None
    # Total accumulated confidence should be highest
    assert final_tv.confidence > tv1.confidence
