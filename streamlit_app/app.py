import os
import sys
import time
import streamlit as st

# Ensure project root is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.pln_engine.runner import PLNRunner
from src.pln_engine.models import TruthValue, QueryResult, DerivationResult, ProofNode

st.set_page_config(
    page_title="Coffee Agriculture PLN Reasoning System",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern agronomic reasoning styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        background: linear-gradient(120deg, #10B981, #059669, #047857);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .badge-runtime {
        background-color: #064E3B;
        color: #A7F3D0;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
    }
    .proof-node {
        background: rgba(16, 185, 129, 0.08);
        border-left: 3px solid #10B981;
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 0 6px 6px 0;
    }
    .rule-tag {
        background: #065F46;
        color: #D1FAE5;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
    }
    .trace-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 14px;
        margin-top: 10px;
    }
    .metric-box {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_runner():
    return PLNRunner(project_root=root_dir)

runner = get_runner()

# Header Section
st.markdown('<div class="main-title">☕ Coffee Agriculture Probabilistic Reasoning System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">MeTTa-native Probabilistic Logic Network (PLN) for coffee plant disease diagnosis, evidence pooling, and treatment protocols.</div>', unsafe_allow_html=True)
st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <span class="badge-runtime">⚡ Hyperon 0.2.10 Native MeTTa</span>
    <span class="badge-runtime" style="background-color: #1E3A8A; color: #BFDBFE;">🌿 Hemileia vastatrix & Colletotrichum Domain</span>
    <span class="badge-runtime" style="background-color: #4C1D95; color: #DDD6FE;">🔬 Exact TrueAGI PLN Formulas</span>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("Reasoning Configuration")

mode = st.sidebar.selectbox(
    "Reasoning Strategy",
    [
        "Backward Chaining (Goal-Directed Diagnosis)",
        "Forward Chaining (Data-Driven Progression)",
        "Conflicting Evidence Resolution (PLN Revision)",
        "Compare Forward vs Backward Chaining"
    ]
)

depth = st.sidebar.slider(
    "Peano Search Depth (Nat)",
    min_value=1,
    max_value=3,
    value=2,
    help="Bounded depth preventing infinite recursion: Z, S Z, S (S Z)."
)

# Knowledge Base Inspector
with st.sidebar.expander("🌾 Knowledge Base Inspector (coffee_agriculture.metta)"):
    kb_code = runner.get_kb_content("coffee_agriculture")
    st.code(kb_code, language="lisp")

# Helper to recursively display proof trees
def render_proof_node(node: ProofNode, level: int = 0):
    indent = "&nbsp;" * (level * 6)
    if node.node_type == "Fact":
        st.markdown(
            f"{indent}📌 <b>Observed Fact</b>: <code>{node.statement.raw}</code>",
            unsafe_allow_html=True
        )
    elif node.node_type == "Initial":
        st.markdown(
            f"{indent}🌱 <b>Seed Premise</b>: <code>{node.statement.raw}</code>",
            unsafe_allow_html=True
        )
    elif node.node_type == "Rule":
        rule_desc = f"Rule ({node.rule_name})"
        if node.rule_name == "mp":
            rule_desc = "Modus Ponens (Symptom Detachment)"
        elif node.rule_name == "ded":
            rule_desc = "PLN Deduction (Causal/Taxonomic Transitivity)"
        st.markdown(
            f"{indent}⚙️ <span class=\"rule-tag\">{rule_desc}</span>",
            unsafe_allow_html=True
        )
        for child in node.children:
            render_proof_node(child, level + 1)

# --------------------------------------------------------------------
# Mode 1: Backward Chaining
# --------------------------------------------------------------------
if mode == "Backward Chaining (Goal-Directed Diagnosis)":
    st.subheader("🎯 Goal-Directed Backward Chaining")
    st.markdown("Prove an agronomic hypothesis or treatment recommendation by recursively searching backward from goal to premises.")

    presets = [
        "(RequiresTreatment CoffeePlant01 CopperFungicideSpray)",
        "(AfflictedWith CoffeePlant01 CoffeeLeafRust)",
        "(RequiresTreatment CoffeePlant02 TargetedBerryFungicide)",
        "(AfflictedWith CoffeePlant03 NitrogenDeficiency)",
        "(RequiresTreatment CoffeePlant01 CanopyPruning)",
        "(Inheritance CoffeePlant01 SusceptibleToRust)"
    ]

    col1, col2 = st.columns([3, 1])
    with col1:
        preset_choice = st.selectbox(
            "Select Diagnostic Goal or Enter Custom Query",
            options=presets + ["Custom Query"]
        )
        if preset_choice == "Custom Query":
            query_target = st.text_input("MeTTa Goal Statement", value="(RequiresTreatment CoffeePlant01 CopperFungicideSpray)")
        else:
            query_target = st.text_input("MeTTa Goal Statement", value=preset_choice)

    with col2:
        st.write("")
        st.write("")
        run_btn = st.button("🚀 Execute MeTTa Engine", use_container_width=True, type="primary")

    if run_btn:
        with st.spinner("Executing native MeTTa backward chainer in official Hyperon runtime..."):
            result = runner.run_backward_chaining(
                target_statement=query_target,
                depth=depth,
                kb_name="coffee_agriculture"
            )

        if result.success:
            st.success(f"Goal Proven! Found {len(result.derivations)} valid proof(s) in {result.execution_time_ms:.2f} ms")

            for i, d in enumerate(result.derivations, 1):
                with st.container():
                    st.markdown(f"### Derivation #{i}: `⊢ {d.statement.raw}`")
                    
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric("Strength ($s$)", f"{d.truth_value.strength:.4f}", help="Probability mode")
                    with m2:
                        st.metric("Confidence ($c$)", f"{d.truth_value.confidence:.4f}", help="Certainty parameter")
                    with m3:
                        w_val = d.truth_value.confidence / max(1e-6, 1.0 - d.truth_value.confidence)
                        st.metric("Weight of Evidence ($w$)", f"{w_val:.2f}", help="w = c / (1 - c)")

                    # Explainable Reasoning Trace
                    st.markdown("#### 🔍 Explainable Reasoning Trace")
                    st.markdown(f"""
                    <div class="trace-card">
                        <b>Target Agronomic Goal:</b> <code>{query_target}</code><br>
                        <b>Concluded Truth Value:</b> Simple Truth Value <b>(stv {d.truth_value.strength:.4f} {d.truth_value.confidence:.4f})</b><br>
                        <b>Reasoning Explanation:</b> Verified through depth-bounded backward search over <code>coffee_agriculture.metta</code>. Subgoals resolved against field symptoms and detached via PLN Modus Ponens.
                    </div>
                    """, unsafe_allow_html=True)

                    if d.proof_tree:
                        st.markdown("#### 🌳 MeTTa Proof Tree Structure")
                        render_proof_node(d.proof_tree)

                    with st.expander("View Raw MeTTa AST"):
                        st.code(d.raw_metta, language="lisp")
        else:
            st.error(f"Goal could not be proven within search depth {depth}. " + (f"Error: {result.error_message}" if result.error_message else ""))
            st.info("Tip: Multi-step treatment derivations (e.g. HasSymptom -> AfflictedWith -> RequiresTreatment) require depth >= 2.")

# --------------------------------------------------------------------
# Mode 2: Forward Chaining
# --------------------------------------------------------------------
elif mode == "Forward Chaining (Data-Driven Progression)":
    st.subheader("⏩ Data-Driven Forward Chaining")
    st.markdown("Derive all reachable disease diagnoses and management recommendations forward from observed field symptoms.")

    fc_presets = [
        "(HasSymptom CoffeePlant01 OrangeRustPustules)",
        "(HasSymptom CoffeePlant02 DarkBerryLesions)",
        "(HasSymptom CoffeePlant03 YellowLeafChlorosis)",
        "(EnvironmentalRisk CoffeePlant01 DenseShadedCanopy)",
        "(EnvironmentalRisk CoffeePlant01 HighHumidity)"
    ]

    col1, col2 = st.columns([3, 1])
    with col1:
        seed_choice = st.selectbox("Select Seed Premise", options=fc_presets + ["Custom Observation"])
        if seed_choice == "Custom Observation":
            seed_statement = st.text_input("MeTTa Premise Statement", value="(HasSymptom CoffeePlant01 OrangeRustPustules)")
        else:
            seed_statement = st.text_input("MeTTa Premise Statement", value=seed_choice)

    with col2:
        st.write("")
        st.write("")
        run_fc_btn = st.button("🚀 Run Forward Chaining", use_container_width=True, type="primary")

    col_s, col_c = st.columns(2)
    with col_s:
        seed_s = st.slider("Observed Symptom Strength ($s$)", 0.0, 1.0, 0.88, 0.01)
    with col_c:
        seed_c = st.slider("Observed Symptom Confidence ($c$)", 0.0, 1.0, 0.85, 0.01)

    if run_fc_btn:
        with st.spinner("Propagating forward across agricultural rules..."):
            result = runner.run_forward_chaining(
                premise_statement=seed_statement,
                premise_tv=TruthValue(seed_s, seed_c),
                depth=depth,
                kb_name="coffee_agriculture"
            )

        if result.success:
            st.success(f"Forward Chaining Complete: Derived {len(result.derivations)} agricultural fact(s) in {result.execution_time_ms:.2f} ms")

            for idx, d in enumerate(result.derivations, 1):
                with st.expander(f"Derived Statement #{idx}: {d.statement.raw}", expanded=True):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Strength ($s$)", f"{d.truth_value.strength:.4f}")
                    c2.metric("Confidence ($c$)", f"{d.truth_value.confidence:.4f}")
                    w = d.truth_value.confidence / max(1e-6, 1.0 - d.truth_value.confidence)
                    c3.metric("Weight of Evidence ($w$)", f"{w:.2f}")
                    st.code(d.raw_metta, language="lisp")
        else:
            st.warning("No new derivations reached with current depth.")

# --------------------------------------------------------------------
# Mode 3: Conflicting Evidence Resolution (PLN Revision)
# --------------------------------------------------------------------
elif mode == "Conflicting Evidence Resolution (PLN Revision)":
    st.subheader("⚖️ Conflicting Field Evidence Resolution via PLN Revision")
    st.markdown("""
    When two agricultural field scouts inspect the same coffee plot with **conflicting findings**,
    PLN does NOT overwrite observations. Instead, it converts confidence into **evidence weight** ($w = \\frac{c}{1 - c}$)
    and pools their observations:
    $$s_{rev} = \\frac{s_1 w_1 + s_2 w_2}{w_1 + w_2}, \\quad w_{total} = w_1 + w_2, \\quad c_{rev} = \\frac{w_{total}}{w_{total} + 1}$$
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🧑‍🌾 Scout A (Visual Foliage Scout)")
        st.caption("Reports visible orange powdery pustules on CoffeePlant01.")
        s1 = st.slider("Scout A Strength ($s_1$)", 0.0, 1.0, 0.85, 0.01)
        c1 = st.slider("Scout A Confidence ($c_1$)", 0.0, 0.99, 0.75, 0.01)
        w1 = c1 / max(1e-6, 1.0 - c1)
        st.info(f"Evidence Weight $w_1$: **{w1:.2f}**")

    with col2:
        st.markdown("#### 🔬 Scout B (Canopy Health Inspector)")
        st.caption("Reports clean foliage, doubting acute rust infection.")
        s2 = st.slider("Scout B Strength ($s_2$)", 0.0, 1.0, 0.20, 0.01)
        c2 = st.slider("Scout B Confidence ($c_2$)", 0.0, 0.99, 0.70, 0.01)
        w2 = c2 / max(1e-6, 1.0 - c2)
        st.info(f"Evidence Weight $w_2$: **{w2:.2f}**")

    tv_revised = runner.run_revision(TruthValue(s1, c1), TruthValue(s2, c2))

    if tv_revised:
        st.markdown("---")
        st.markdown("### 📊 Fused Knowledge State (Calculated via Native MeTTa)")
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("Pooled Strength ($s$)", f"{tv_revised.strength:.4f}", help="Weighted compromise")
        rc2.metric(
            "Pooled Confidence ($c$)",
            f"{tv_revised.confidence:.4f}",
            delta=f"+{tv_revised.confidence - max(c1, c2):.4f} over highest source",
            help="Strictly increases when pooling independent evidence"
        )
        w_total = w1 + w2
        rc3.metric("Total Evidence Weight ($w_{total}$)", f"{w_total:.2f}")

        st.markdown(f"""
        <div class="trace-card">
            <b>PLN Agronomic Conclusion:</b><br>
            The conflicting observations produce a balanced probability of <b>{tv_revised.strength:.4f}</b> (reflecting disagreement between observers),
            while the combined evidence weight grows to <b>{w_total:.2f}</b>, raising confidence to <b>{tv_revised.confidence:.4f}</b>.
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------------
# Mode 4: Compare Forward vs Backward Chaining
# --------------------------------------------------------------------
elif mode == "Compare Forward vs Backward Chaining":
    st.subheader("⚖️ Forward vs Backward Chaining Comparison")
    st.markdown("Compare data-driven forward chaining against goal-driven backward chaining operating over the **same** knowledge base.")

    sample_seed = "(HasSymptom CoffeePlant01 OrangeRustPustules)"
    sample_goal = "(RequiresTreatment CoffeePlant01 CopperFungicideSpray)"

    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("#### ⏩ Forward Chaining (Data-Driven)")
        st.markdown(f"**Seed Premise:** `{sample_seed}`")
        if st.button("Run Forward Comparison", type="primary", use_container_width=True):
            fc_res = runner.run_forward_chaining(sample_seed, depth=2, kb_name="coffee_agriculture")
            if fc_res.success:
                st.success(f"Generated {len(fc_res.derivations)} derived statements in {fc_res.execution_time_ms:.2f} ms")
                for d in fc_res.derivations:
                    st.write(f"- `{d.statement.raw}` : STV ({d.truth_value.strength:.4f}, {d.truth_value.confidence:.4f})")

    with c_right:
        st.markdown("#### 🎯 Backward Chaining (Goal-Driven)")
        st.markdown(f"**Target Goal:** `{sample_goal}`")
        if st.button("Run Backward Comparison", type="secondary", use_container_width=True):
            bc_res = runner.run_backward_chaining(sample_goal, depth=2, kb_name="coffee_agriculture")
            if bc_res.success:
                st.success(f"Proven with {len(bc_res.derivations)} proof paths in {bc_res.execution_time_ms:.2f} ms")
                for d in bc_res.derivations:
                    st.write(f"- `{d.statement.raw}` : STV ({d.truth_value.strength:.4f}, {d.truth_value.confidence:.4f})")
                    if d.proof_tree:
                        render_proof_node(d.proof_tree)

# Agronomic Disclaimer
st.markdown("---")
st.caption("⚠️ **Agronomic Note**: This system is a formal probabilistic reasoning demonstration evaluating PLN inference over plant pathology rules. It is designed for AI knowledge engineering validation and is not an autonomous substitute for certified agricultural inspection.")
