import pytest
from src.pln_engine.runner import PLNRunner

@pytest.fixture(scope="module")
def runner():
    return PLNRunner()

def test_missing_fact_unprovable_goal(runner):
    """Case D: Querying an agronomic condition with no supporting evidence returns success=False."""
    result = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant01 SoilSterilization)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert result.success is False
    assert len(result.derivations) == 0

def test_unknown_entity_unprovable(runner):
    """Querying an unknown plant entity returns no derivations."""
    result = runner.run_backward_chaining(
        target_statement="(AfflictedWith NonExistentPlant99 CoffeeLeafRust)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert result.success is False
    assert len(result.derivations) == 0

def test_chlorosis_without_pustules_does_not_prove_rust(runner):
    """
    Negative Agronomic Test: CoffeePlant03 exhibits YellowLeafChlorosis and AcidicLeachedSoil.
    The system must NOT falsely conclude CoffeeLeafRust, because OrangeRustPustules is absent!
    Instead, it correctly explains NitrogenDeficiency.
    """
    result = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant03 CoffeeLeafRust)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    # CoffeeLeafRust cannot be proven for CoffeePlant03
    assert result.success is False
    assert len(result.derivations) == 0

    # But NitrogenDeficiency CAN be proven for CoffeePlant03
    nitrogen_res = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant03 NitrogenDeficiency)",
        depth=1,
        kb_name="coffee_agriculture"
    )
    assert nitrogen_res.success is True
    assert len(nitrogen_res.derivations) >= 1

def test_healthy_plant_no_berry_disease(runner):
    """
    Negative Agronomic Test: CoffeePlant04 is a control plant with no lesions.
    Querying CoffeeBerryDisease must return insufficient evidence.
    """
    result = runner.run_backward_chaining(
        target_statement="(AfflictedWith CoffeePlant04 CoffeeBerryDisease)",
        depth=2,
        kb_name="coffee_agriculture"
    )
    assert result.success is False
    assert len(result.derivations) == 0

def test_depth_cutoff_insufficient_depth(runner):
    """Depth 1 is insufficient to prove a 2-step transitive chain."""
    # (RequiresTreatment CoffeePlant01 CopperFungicideSpray) requires depth 2
    result = runner.run_backward_chaining(
        target_statement="(RequiresTreatment CoffeePlant01 CopperFungicideSpray)",
        depth=1,  # Insufficient depth!
        kb_name="coffee_agriculture"
    )
    assert result.success is False
    assert len(result.derivations) == 0

def test_cyclic_rules_termination(runner):
    """Cyclic agronomic rules (e.g. Risk -> Severity -> Risk) must terminate cleanly under Peano depth."""
    cyclic_script = """
    (: Nat Type)
    (: Z Nat)
    (: S (-> Nat Nat))
    (: stv (-> Number Number TruthValue))

    (= (Truth_Apply_Rule2 mp (stv $s1 $c1) (stv $s2 $c2))
       (stv (* $s1 $s2) (* $c1 $c2)))

    ;; Cyclic KB: Risk implies Severity, Severity implies Risk
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
