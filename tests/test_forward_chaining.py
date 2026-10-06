import pytest
from src.pln_engine.runner import PLNRunner
from src.pln_engine.models import TruthValue

@pytest.fixture(scope="module")
def runner():
    return PLNRunner()

def test_fc_1_direct_fact(runner):
    """Test 1: Direct fact preservation at depth 0."""
    res = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        premise_tv=TruthValue(0.88, 0.85),
        depth=0,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    assert len(res.derivations) == 1
    d = res.derivations[0]
    assert d.statement.predicate == "HasSymptom"
    assert pytest.approx(d.truth_value.strength, 0.01) == 0.88

def test_fc_2_one_step_derivation(runner):
    """Test 2: One-step derivation: OrangeRustPustules -> CoffeeLeafRust."""
    res = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        premise_tv=TruthValue(0.88, 0.85),
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    preds = [d.statement.predicate for d in res.derivations]
    assert "AfflictedWith" in preds
    disease_d = [d for d in res.derivations if d.statement.predicate == "AfflictedWith"][0]
    assert "CoffeeLeafRust" in disease_d.statement.arguments

def test_fc_3_two_step_derivation(runner):
    """Test 3: Two-step derivation: OrangeRustPustules -> CoffeeLeafRust -> CopperFungicideSpray."""
    res = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        premise_tv=TruthValue(0.88, 0.85),
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    preds = [d.statement.predicate for d in res.derivations]
    assert "RequiresTreatment" in preds
    treatment_d = [d for d in res.derivations if d.statement.predicate == "RequiresTreatment"][0]
    assert "CopperFungicideSpray" in treatment_d.statement.arguments

def test_fc_4_multiple_rules(runner):
    """Test 4: Derivations trigger across different rule branches."""
    # From DenseShadedCanopy: triggers CanopyPruning
    res = runner.run_forward_chaining(
        premise_statement="(EnvironmentalRisk CoffeePlant01 DenseShadedCanopy)",
        premise_tv=TruthValue(0.80, 0.75),
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    preds = [d.statement.predicate for d in res.derivations]
    assert "RequiresTreatment" in preds

def test_fc_5_unavailable_premise(runner):
    """Test 5: An unmatchable premise yields only the initial seed statement."""
    res = runner.run_forward_chaining(
        premise_statement="(UnknownCondition CoffeePlant01 BizarreFactor)",
        premise_tv=TruthValue(0.50, 0.50),
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    assert len(res.derivations) == 1
    assert res.derivations[0].statement.predicate == "UnknownCondition"

def test_fc_6_duplicate_derivation(runner):
    """Test 6: Verify derivations do not contain unmanaged raw duplicates."""
    res = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert res.success is True
    raw_statements = [d.statement.raw for d in res.derivations]
    # Check that each distinct derived theorem is distinct
    assert len(raw_statements) == len(set(raw_statements))

def test_fc_7_cycles(runner):
    """Test 7: Cyclic forward propagation terminates under Peano depth."""
    cyclic_script = """
    (: Nat Type)
    (: Z Nat)
    (: S (-> Nat Nat))
    (: stv (-> Number Number TruthValue))

    (= (Truth_Apply_Rule2 mp (stv $s1 $c1) (stv $s2 $c2))
       (stv (* $s1 $s2) (* $c1 $c2)))

    (= (kb) (superpose (
       (⊢ (→ (RustPustules $p) (RustInfection $p)) (stv 0.9 0.8))
       (⊢ (→ (RustInfection $p) (RustPustules $p)) (stv 0.9 0.8))
    )))

    (= (rb) (rule mp $p (→ $p $q) $q))

    (= (fc (⊢ $p1 $tv1) Z)
       (Derivation (⊢ $p1 $tv1) (Initial $p1)))

    (= (fc (⊢ $p1 $tv1) (S $k))
       (superpose (
         (Derivation (⊢ $p1 $tv1) (Initial $p1))
         (let* (((rule mp $p1 $p2 $concl) (rb))
                ((⊢ $p2 $tv2) (kb))
                ($tvConcl (Truth_Apply_Rule2 mp $tv1 $tv2)))
           (fc (⊢ $concl $tvConcl) $k)))))

    !(fc (⊢ (RustPustules CoffeePlant01) (stv 0.9 0.8)) (S (S Z)))
    """
    res = runner.execute_raw_metta(cyclic_script)
    assert len(res) > 0
    assert len(res[0]) > 0
    assert "Derivation" in str(res[0][0])

def test_fc_8_depth_limit(runner):
    """Test 8: Strict depth horizon bounds."""
    res_d1 = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    preds_d1 = [d.statement.predicate for d in res_d1.derivations]
    assert "RequiresTreatment" not in preds_d1

    res_d2 = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    preds_d2 = [d.statement.predicate for d in res_d2.derivations]
    assert "RequiresTreatment" in preds_d2

def test_fc_9_truth_value_propagation(runner):
    """Test 9: Forward truth value propagation matches Modus Ponens calculation."""
    res = runner.run_forward_chaining(
        premise_statement="(HasSymptom CoffeePlant01 OrangeRustPustules)",
        premise_tv=TruthValue(0.88, 0.85),
        depth=1,
        kb_name="coffee_agriculture"
    )
    disease_d = [d for d in res.derivations if d.statement.predicate == "AfflictedWith"][0]
    # MP formula: s = 0.88*0.95 + 0.02*(1-0.88) = 0.8384; c = 0.88*0.95 * 0.85*0.90 = 0.63954
    assert pytest.approx(disease_d.truth_value.strength, 0.01) == 0.8384
    assert pytest.approx(disease_d.truth_value.confidence, 0.01) == 0.6395
