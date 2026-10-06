import pytest
from src.pln_engine.runner import PLNRunner
from src.pln_engine.models import TruthValue

@pytest.fixture(scope="module")
def runner():
    return PLNRunner()

def test_truth_weight_conversions(runner):
    """Verifies bidirectional weight of evidence conversions: w = c / (1 - c), c = w / (w + 1)."""
    script = """
    !(Truth_c2w 0.75)
    !(Truth_w2c 3.0)
    """
    res = runner.execute_raw_metta(script)
    # 0.75 / (1 - 0.75) = 3.0
    w = float(str(res[0][0]))
    assert pytest.approx(w, 0.01) == 3.0
    # 3.0 / (3.0 + 1) = 0.75
    c = float(str(res[1][0]))
    assert pytest.approx(c, 0.01) == 0.75

def test_pln_negation(runner):
    """PLN Negation: s' = 1 - s, c' = c."""
    script = "!(Truth_Negation (stv 0.8 0.9))"
    res = runner.execute_raw_metta(script)
    assert "(stv 0.19999999999999996 0.9)" in str(res[0][0]) or "(stv 0.2" in str(res[0][0])

def test_pln_intersection(runner):
    """PLN Conjunction/Intersection: s = s1 * s2, c = c1 * c2."""
    script = "!(Truth_Intersection (stv 0.8 0.7) (stv 0.6 0.5))"
    res = runner.execute_raw_metta(script)
    assert "(stv 0.48 0.35)" in str(res[0][0])

def test_pln_deduction_formula(runner):
    """PLN Deduction: OrangeRustPustules -> CoffeeLeafRust, CoffeeLeafRust -> CopperFungicideSpray."""
    script = "!(Truth_Deduction (stv 0.90 0.85) (stv 0.80 0.75))"
    res = runner.execute_raw_metta(script)
    # s = 0.9 * 0.8 = 0.72; c = 0.72 * 0.85 * 0.75 = 0.459
    assert "(stv 0.7200000000000001 0.459)" in str(res[0][0])

def test_pln_modus_ponens_formula(runner):
    """PLN Modus Ponens with base rate 0.02: P, (P -> Q) |- Q."""
    script = "!(Truth_ModusPonens (stv 0.88 0.85) (stv 0.95 0.90))"
    res = runner.execute_raw_metta(script)
    # s = 0.88*0.95 + 0.02*(1 - 0.88) = 0.836 + 0.0024 = 0.8384
    # c = (0.88*0.95)*(0.85*0.90) = 0.836 * 0.765 = 0.63954
    assert "(stv 0.8383999999999999 0.63954)" in str(res[0][0])

def test_pln_revision_rule(runner):
    """PLN Revision: Exact evidence pooling between two independent observations."""
    tv = runner.run_revision(TruthValue(0.85, 0.75), TruthValue(0.20, 0.70))
    assert tv is not None
    assert pytest.approx(tv.strength, 0.01) == 0.5656
    assert pytest.approx(tv.confidence, 0.01) == 0.8421

def test_pln_induction_formula(runner):
    """PLN Induction: ArabicaBourbon -> SusceptibleToRust, ArabicaBourbon -> PrematureBerryDrop."""
    script = "!(Truth_Induction (stv 0.80 0.70) (stv 0.85 0.75))"
    res = runner.execute_raw_metta(script)
    assert "(stv 0.68" in str(res[0][0])

def test_pln_abduction_formula(runner):
    """PLN Abduction: CoffeeLeafRust -> Defoliation, NitrogenDeficiency -> Defoliation."""
    script = "!(Truth_Abduction (stv 0.85 0.75) (stv 0.80 0.70))"
    res = runner.execute_raw_metta(script)
    assert "(stv 0.68" in str(res[0][0])

def test_pln_boundary_values(runner):
    """Verifies STV behavior on boundary values [0, 1]."""
    script = """
    !(Truth_Deduction (stv 0.0 0.0) (stv 1.0 0.99))
    !(Truth_Revision (stv 1.0 0.5) (stv 1.0 0.5))
    """
    res = runner.execute_raw_metta(script)
    assert "(stv 0 0)" in str(res[0][0]) or "(stv 0.0 0.0)" in str(res[0][0])
    assert "(stv 1.0" in str(res[1][0]) or "(stv 1 " in str(res[1][0])
