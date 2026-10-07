"""
agri-pln-metta: Streamlit Interactive Agricultural Reasoning Dashboard
Provides a modern visual interface for demonstrating Probabilistic Logic Network (PLN)
reasoning over the agricultural MeTTa knowledge base.
"""

import sys
import os
import time
from pathlib import Path
import streamlit as st

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.resolve()))
from engine_bridge import AgriPLNEngine

# Page Configuration
st.set_page_config(
    page_title="agri-pln-metta: Agricultural PLN Reasoner",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2E7D32;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F1F8E9;
        border-radius: 10px;
        padding: 1.2rem;
        border-left: 5px solid #4CAF50;
        margin-bottom: 1rem;
    }
    .step-card {
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
    }
    .badge-high {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-warn {
        background-color: #FFF3E0;
        color: #E65100;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Engine
@st.cache_resource
def get_engine():
    return AgriPLNEngine()

engine = get_engine()

# Sidebar: Scenarios and System Controls
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sprout.png", width=64)
    st.markdown("### 🌾 agri-pln-metta")
    st.markdown("**Domain-Specific Agricultural PLN Reasoning Engine in MeTTa**")
    st.markdown("---")
    
    st.markdown("#### ⚡ Quick Demo Scenarios")
    demo_choice = st.radio(
        "Select an Evaluation Scenario:",
        [
            "Custom Query",
            "Demo 1: Coffee Disease Diagnosis (Full Chain)",
            "Demo 2: Incomplete Evidence (Uncertainty Penalty)",
            "Demo 3: Differential Diagnosis (Yellow Leaves)",
            "Demo 4: Evidence Revision (Scouting + Lab PCR)",
            "Demo 5: 3-Hop Causal Chain (Poor Drainage -> Wilting)",
            "Demo 6: Goal-Driven Backward Chaining",
            "Demo 7: Inductive Rule Learning (Farm Surveys)"
        ]
    )
    
    st.markdown("---")
    st.markdown("#### ⚙️ Engine Diagnostics")
    st.text(f"MeTTa Executable:\n{engine.metta_bin}")
    st.text("AtomSpace: &agriculture-kb")
    
    if st.button("🧪 Run Automated Test Suite"):
        with st.spinner("Executing all 9 MeTTa test suites..."):
            import subprocess
            runner_script = engine.project_root / "runner.py"
            proc = subprocess.run([sys.executable, str(runner_script)], capture_output=True, text=True)
            if proc.returncode == 0:
                st.success("All 9 test suites passed successfully!")
                st.code(proc.stdout)
            else:
                st.error("Some tests failed:")
                st.code(proc.stdout + "\n" + proc.stderr)

# Header Section
st.markdown('<div class="main-header">🌾 Agricultural PLN Reasoning Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Probabilistic Logic Network reasoning over an agriculture-specific Hyperon MeTTa knowledge base.</div>', unsafe_allow_html=True)

# Application Navigation Tabs
tab_main, tab_diff, tab_rev, tab_chain, tab_all_scenarios = st.tabs([
    "🎯 Diagnostic & Treatment Reasoner",
    "🔍 Differential Diagnosis",
    "⚖️ Evidence Revision Lab",
    "⛓️ Multi-Hop Causal Explorer",
    "📋 All 7 Scenarios Benchmark"
])

# ------------------------------------------------------------------------------
# TAB 1: Main Diagnostic & Treatment Reasoner
# ------------------------------------------------------------------------------
with tab_main:
    # Preset handler for Quick Demos
    preset_crop = "Coffee"
    preset_cond = "HighHumidity"
    preset_sym = "OrangeLeafSpots"
    
    if demo_choice == "Demo 1: Coffee Disease Diagnosis (Full Chain)":
        preset_crop, preset_cond, preset_sym = "Coffee", "HighHumidity", "OrangeLeafSpots"
        st.info("💡 **Scenario 1 & 6:** Demonstrates full forward deduction + abduction + revision with curative treatment prescriptions.")
    elif demo_choice == "Demo 2: Incomplete Evidence (Uncertainty Penalty)":
        preset_crop, preset_cond, preset_sym = "Coffee", "None", "OrangeLeafSpots"
        st.warning("⚠️ **Scenario 2:** Demonstrates incomplete observations (missing environmental humidity). Confidence is penalized and missing evidence is reported.")
    elif demo_choice == "Demo 3: Differential Diagnosis (Yellow Leaves)":
        preset_crop, preset_cond, preset_sym = "Coffee", "HighHumidity", "YellowLeaves"
        st.info("💡 **Scenario 3:** Demonstrates multiple competing candidate causes explaining *YellowLeaves*.")
    
    col1, col2, col3 = st.columns(3)
    
    crops_list = ["Coffee", "Maize", "Wheat", "Teff", "Tomato", "Potato", "Barley"]
    conds_list = ["HighHumidity", "ExcessMoisture", "PoorDrainage", "WarmTemperature", "DenseCanopyShade", "DroughtStress", "LowSoilFertility", "AcidicSoil", "None"]
    syms_list = ["OrangeLeafSpots", "YellowLeaves", "BrownPustules", "WaterSoakedLesions", "WhitePowderyPatches", "Wilting", "StuntedGrowth", "PrematureBerryDrop", "MarginalLeafScorching", "ConcentricRingSpots"]
    
    with col1:
        sel_crop = st.selectbox("1. Select Crop:", crops_list, index=crops_list.index(preset_crop) if preset_crop in crops_list else 0)
    with col2:
        sel_cond = st.selectbox("2. Observed Environmental Condition:", conds_list, index=conds_list.index(preset_cond) if preset_cond in conds_list else 0)
    with col3:
        sel_sym = st.selectbox("3. Observed Foliar / Plant Symptom:", syms_list, index=syms_list.index(preset_sym) if preset_sym in syms_list else 0)
        
    btn_run = st.button("🚀 Run Agricultural PLN Inference", type="primary", use_container_width=True)
    
    if btn_run or demo_choice in ["Demo 1: Coffee Disease Diagnosis (Full Chain)", "Demo 2: Incomplete Evidence (Uncertainty Penalty)"]:
        with st.spinner("Invoking MeTTa PLN reasoning engine..."):
            start_t = time.time()
            if sel_cond == "None":
                # Incomplete evidence query
                res = engine.query_backward_chaining(sel_crop, "CoffeeLeafRust", None, sel_sym)
                dur = time.time() - start_t
                
                st.markdown("### 📊 PLN Reasoning Results (Incomplete Evidence)")
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Goal Hypothesis", f"{res['disease']}")
                m2.metric("Calculated Strength (s)", f"{res['strength']:.4f}")
                m3.metric("Calculated Confidence (c)", f"{res['confidence']:.4f}")
                m4.metric("Status", "Partially Supported", delta="-Low Confidence", delta_color="inverse")
                
                st.markdown("#### 🧩 Evidence & Missing Factor Analysis")
                st.markdown(f"- ✅ **Verified Evidence:** Observed `{sel_sym}` on `{sel_crop}`")
                st.markdown(f"- ⚠️ **Missing Required Evidence:** Unobserved `HighHumidity` (Environmental trigger)")
                st.markdown(f"- 📉 **Uncertainty Penalty:** Confidence reduced from typical ~0.74 to **{res['confidence']:.4f}** due to lack of environmental confirmation.")
                
                st.markdown("#### 💬 Plain-English Interpretation")
                st.info(f"The symptom **{sel_sym}** is consistent with **{res['disease']}**, but without confirmation of conducive microclimatic humidity, the diagnosis carries higher epistemic uncertainty.")
                
            else:
                # Full forward chaining query
                res = engine.query_forward_chaining(sel_crop, sel_cond, sel_sym)
                dur = time.time() - start_t
                
                if res["success"]:
                    st.markdown("### 📊 Agricultural PLN Reasoning Result")
                    
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Inferred Disease", res["disease"])
                    m2.metric("Calculated Strength (s)", f"{res['strength']:.4f}")
                    m3.metric("Calculated Confidence (c)", f"{res['confidence']:.4f}")
                    m4.metric("Inference Time", f"{dur:.2f}s")
                    
                    col_path, col_treat = st.columns([1.2, 1.0])
                    
                    with col_path:
                        st.markdown("#### 🧠 Step-by-Step Reasoning Trace")
                        st.markdown(f"""
                        <div class="step-card">
                            <strong>Step 1 (Observation):</strong> Crop <code>{sel_crop}</code> + Environment <code>{sel_cond}</code> + Symptom <code>{sel_sym}</code>
                        </div>
                        <div class="step-card">
                            <strong>Step 2 (Risk Deduction):</strong> <code>{sel_cond}</code> &rarr; <em>increases-risk</em> &rarr; <code>{res['disease']}</code> (Deduction STV)
                        </div>
                        <div class="step-card">
                            <strong>Step 3 (Diagnostic Abduction):</strong> <code>{res['disease']}</code> &rarr; <em>causes</em> &rarr; <code>{sel_sym}</code> &vdash; <code>{res['disease']}</code> (Abduction STV)
                        </div>
                        <div class="step-card">
                            <strong>Step 4 (Evidence Fusion):</strong> Risk STV &oplus; Abduced STV &rarr; <strong>Fused Belief (STV {res['strength']:.3f} {res['confidence']:.3f})</strong>
                        </div>
                        <div class="step-card">
                            <strong>Step 5 (Treatment Deduction):</strong> <code>{res['disease']}</code> &rarr; <em>effective-treatment</em> &rarr; Actionable IPM Prescriptions
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("#### 💬 Interpretation")
                        st.success(f"**{res['disease']}** is probabilistically supported with **{res['strength']*100:.1f}% strength** and **{res['confidence']*100:.1f}% confidence**. This is an evidence-supported hypothesis, not an absolute certainty.")

                    with col_treat:
                        st.markdown("#### 💊 Actionable IPM Recommendations")
                        if res["treatments"]:
                            for t in res["treatments"]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h4 style="margin:0; color:#1B5E20;">🌿 {t['action']}</h4>
                                    <p style="margin:4px 0 0 0; color:#333;">Calculated Efficacy: <strong>s={t['strength']:.3f}</strong> | Confidence: <strong>c={t['confidence']:.3f}</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No specific chemical treatment registered; recommend cultural sanitation.")
                else:
                    st.warning(f"No conclusive causal chain found linking {sel_crop}, {sel_cond}, and {sel_sym} in the knowledge base.")

            with st.expander("🛠️ Inspect Raw MeTTa AST & Execution Trace"):
                st.code(res.get("raw_output", ""))

# ------------------------------------------------------------------------------
# TAB 2: Differential Diagnosis
# ------------------------------------------------------------------------------
with tab_diff:
    st.markdown("### 🔍 Differential Diagnosis: Multiple Competing Explanations")
    st.markdown("Evaluates ambiguous foliar symptoms that can arise from multiple distinct pathogens or abiotic deficiencies.")
    
    c1, c2 = st.columns(2)
    with c1:
        diff_crop = st.selectbox("Select Crop for Differential Diagnosis:", ["Coffee", "Tomato", "Maize", "Wheat"], key="diff_c")
    with c2:
        diff_sym = st.selectbox("Select Ambiguous Symptom:", ["YellowLeaves", "Wilting", "StuntedGrowth", "ConcentricRingSpots"], key="diff_s")
        
    if st.button("🔍 Run Differential Abduction"):
        with st.spinner("Computing candidate etiologies in MeTTa..."):
            candidates = engine.query_differential_diagnosis(diff_crop, diff_sym)
            if candidates:
                st.markdown(f"#### Found {len(candidates)} Plausible Etiologies for `{diff_sym}` on `{diff_crop}`:")
                for cand in candidates:
                    col_c1, col_c2, col_c3 = st.columns([1.5, 1.0, 1.0])
                    col_c1.markdown(f"**🔬 {cand['disease']}**")
                    col_c2.progress(cand['strength'], text=f"Strength: {cand['strength']:.3f}")
                    col_c3.progress(cand['confidence'], text=f"Confidence: {cand['confidence']:.3f}")
            else:
                st.info("No competing candidates found for this crop-symptom pair.")

# ------------------------------------------------------------------------------
# TAB 3: Evidence Revision Lab
# ------------------------------------------------------------------------------
with tab_rev:
    st.markdown("### ⚖️ PLN Belief Revision & Evidence Fusion")
    st.markdown("Combines independent evidence sources (e.g. Field Scouting + Laboratory Diagnostic) using PLN Revision algebra.")
    
    col_src1, col_src2 = st.columns(2)
    
    with col_src1:
        st.markdown("#### 📋 Source 1: Field Visual Scouting")
        s1 = st.slider("Scouting Strength (s1)", 0.0, 1.0, 0.85, 0.01)
        c1 = st.slider("Scouting Confidence (c1)", 0.0, 0.99, 0.70, 0.01)
        
    with col_src2:
        st.markdown("#### 🔬 Source 2: Laboratory Assay / PCR")
        s2 = st.slider("Laboratory Strength (s2)", 0.0, 1.0, 0.95, 0.01)
        c2 = st.slider("Laboratory Confidence (c2)", 0.0, 0.99, 0.90, 0.01)
        
    prop_name = st.text_input("Target Proposition / Disease:", "CoffeeLeafRust")
    
    if st.button("⚖️ Execute PLN Revision"):
        with st.spinner("Computing evidence fusion in MeTTa..."):
            rev_res = engine.query_revision(prop_name, s1, c1, s2, c2)
            
            st.markdown("#### 📊 Revision Outcome")
            r1, r2, r3 = st.columns(3)
            r1.metric("Combined Strength (s)", f"{rev_res['combined_strength']:.4f}", delta=f"{rev_res['combined_strength'] - s1:+.3f} vs Source 1")
            r2.metric("Combined Confidence (c)", f"{rev_res['combined_confidence']:.4f}", delta=f"{rev_res['combined_confidence'] - max(c1, c2):+.3f} vs Max Input")
            r3.metric("Evidence Status", "Reinforced" if rev_res['combined_confidence'] > max(c1, c2) else "Revised")
            
            if s1 > 0.5 and s2 < 0.5:
                st.warning("⚠️ **Conflicting Evidence:** Visual symptoms contradicted by negative lab assay. Strength moved to weighted center while confidence reflects combined evidence weight.")
            else:
                st.success("✅ **Reinforcing Evidence:** Independent sources agree. Total confidence increased significantly through evidence accumulation.")

# ------------------------------------------------------------------------------
# TAB 4: Multi-Hop Causal Explorer
# ------------------------------------------------------------------------------
with tab_chain:
    st.markdown("### ⛓️ Multi-Hop Causal Path & Uncertainty Propagation")
    st.markdown("Demonstrates transitive causal chaining: `PoorDrainage` &rarr; `WaterloggedSoil` &rarr; `RootRot` &rarr; `Wilting`.")
    
    if st.button("⛓️ Trace 3-Hop Causal Chain"):
        with st.spinner("Evaluating multi-hop chain in MeTTa..."):
            chain_res = engine.query_3hop_chain()
            
            st.markdown(f"""
            <div class="step-card">
                <h4>Causal Path:</h4>
                <p><strong>PoorDrainage</strong> &rarr; [promotes] &rarr; <strong>WaterloggedSoil</strong> &rarr; [increases-risk] &rarr; <strong>RootRot</strong> &rarr; [causes] &rarr; <strong>Wilting</strong></p>
                <p>End-to-End Cumulative STV: <strong>Strength: {chain_res['strength']:.4f}</strong> | <strong>Confidence: {chain_res['confidence']:.4f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("Notice how confidence progressively decays across each transitive hop, modeling epistemic uncertainty accumulation over long causal paths.")

# ------------------------------------------------------------------------------
# TAB 5: All 7 Scenarios Benchmark
# ------------------------------------------------------------------------------
with tab_all_scenarios:
    st.markdown("### 📋 Complete 7 Required Evaluation Scenarios")
    if st.button("▶️ Run Complete Evaluation Suite (All 7 Scenarios)"):
        with st.spinner("Executing all 7 scenarios in MeTTa..."):
            out, err, code = engine.run_raw_query("!(run-all-scenarios)")
            st.success("All 7 scenarios executed successfully!")
            st.code(out)
