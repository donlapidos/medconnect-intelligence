import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="MedConnect Intelligence",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏥 MedConnect Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Clinical Reasoning AI Co-Pilot | Powered by MedGemma 1.5</div>', unsafe_allow_html=True)

# Main CTA for working demo - subtle version
st.info("""
🚀 **Try the Full Working Demo**

For real-time MedGemma analysis with GPU acceleration, visit the **[Kaggle Notebook →](https://www.kaggle.com/code/donlapidos/medgemma-clinical-intelligence-aki-detection)**

*This Streamlit app showcases the interface. The Kaggle version provides complete clinical reasoning with faster inference.*
""")

# Sidebar
with st.sidebar:
    st.header("📊 Clinical Evidence")
    st.markdown("**Lausanne Study (2026)**")
    st.markdown("*97,559 patient stays*")
    st.metric("Mortality Reduction", "25%", delta="-5.2% absolute")
    st.metric("Sepsis Documentation", "+131%", delta="+2.03% absolute")

    st.divider()

    st.header("🔬 Technology")
    st.markdown("**Foundation Model:**")
    st.markdown("Google MedGemma 1.5 (4B)")

    st.divider()

    st.header("✅ Validation")
    st.markdown("**MIMIC-III Database:**")
    st.markdown("• 29 AKI cases analyzed")
    st.markdown("• 25 Sepsis cases analyzed")
    st.markdown("• Real ICU patient data")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 About",
    "🎯 Demo Preview",
    "📊 MIMIC-III Results",
    "🔗 Links"
])

with tab1:
    st.header("About MedConnect Intelligence")

    st.markdown("""
    ### The Problem

    Even advanced hospital EMR systems (like Singapore's EPIC) flag individual abnormal values
    but **don't connect the dots** to suggest diagnoses. Nurses must manually recognize patterns
    across 20+ parameters while managing multiple patients.

    ### The Solution

    **MedConnect Intelligence** provides an AI-powered clinical reasoning layer that:
    - Synthesizes multiple parameters simultaneously
    - Identifies medication interactions and contraindications
    - Calculates clinical scores (SIRS, qSOFA, KDIGO)
    - Provides explainable reasoning (not black box)
    - Works across ANY infrastructure level
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>✅ Clinical Validation</h4>
            <p><strong>Lausanne University Hospital Study</strong></p>
            <ul>
                <li>97,559 patient stays analyzed</li>
                <li>25% reduction in sepsis mortality</li>
                <li>131% improvement in documentation</li>
                <li>Published: npj Digital Medicine (2026)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>✅ Real-World Validation</h4>
            <p><strong>MIMIC-III Critical Care Database</strong></p>
            <ul>
                <li>29 AKI cases extracted & analyzed</li>
                <li>25 Sepsis cases extracted & analyzed</li>
                <li>De-identified ICU patient data</li>
                <li>MedGemma clinical reasoning validated</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    ### Competitive Advantage

    | Traditional EMR | Lausanne HERACLES | MedConnect Intelligence |
    |-----------------|-------------------|-------------------------|
    | Individual flags | Sepsis probability | Full clinical reasoning |
    | No synthesis | Black box ML | Explainable AI |
    | Manual pattern recognition | Automated detection | Automated + Explained |
    | - | Hospital-specific | Works anywhere |
    """)

with tab2:
    st.header("🎯 Interface Preview")

    st.info("👆 **For the full working demo with real-time MedGemma analysis, click the purple box above to launch the Kaggle notebook.**")

    st.markdown("### Sample Use Case: Drug-Induced AKI")

    # Show mock interface
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Patient Data Entry")
        st.number_input("Creatinine (current, mg/dL)", value=2.8, disabled=True)
        st.number_input("Creatinine (baseline, mg/dL)", value=1.0, disabled=True)
        st.number_input("BUN (mg/dL)", value=45, disabled=True)
        st.number_input("Urine Output (mL/24hr)", value=350, disabled=True)
        st.text_area("Medications", value="Ibuprofen 800mg TID\nLisinopril 10mg daily\nMetformin 500mg BID", disabled=True, height=100)

    with col2:
        st.subheader("AI Analysis Output (Example)")
        st.markdown("""
        **MedGemma Clinical Reasoning:**

        **Diagnosis:** Acute Kidney Injury (Drug-Induced)

        **KDIGO Stage:** Stage 2 (Moderate)
        - Creatinine 2.8x baseline (1.0 → 2.8 mg/dL)
        - Meets KDIGO Stage 2 criteria (≥2.0x baseline)

        **Etiology:** Nephrotoxic Drug Combination
        - **NSAID (Ibuprofen)** + **ACE Inhibitor (Lisinopril)**
        - This combination causes synergistic nephrotoxicity
        - NSAIDs reduce afferent arteriolar dilation
        - ACE inhibitors reduce efferent arteriolar constriction
        - Result: Decreased glomerular filtration pressure

        **Immediate Actions:**
        1. **STOP Ibuprofen immediately**
        2. **Hold Lisinopril** until kidney function improves
        3. **Hold Metformin** (risk of lactic acidosis with AKI)
        4. IV fluid resuscitation (assess volume status first)
        5. Monitor for hyperkalemia (ACE-I + AKI)

        **Monitoring:**
        - Daily creatinine, electrolytes
        - Strict I/O monitoring
        - Consider nephrology consult if worsening
        """)

    st.success("👆 This is an example output. See the **Kaggle demo** for real-time analysis!")

with tab3:
    st.header("📊 MIMIC-III Validation Results")

    st.markdown("""
    MedConnect Intelligence was validated on real de-identified ICU patient data
    from the **MIMIC-III Critical Care Database**.
    """)

    # Sample AKI data
    st.subheader("Acute Kidney Injury Cases (Sample)")

    sample_aki = pd.DataFrame({
        'Subject ID': [10045, 10124, 10140, 10150, 10184],
        'KDIGO Stage': ['Stage 2 (Moderate)', 'Stage 1 (Mild)', 'Stage 3 (Severe)', 'Stage 1 (Mild)', 'Stage 2 (Moderate)'],
        'Creatinine Peak': [3.2, 1.8, 4.5, 1.7, 2.9],
        'BUN': [58, 32, 72, 28, 48],
        'Nephrotoxic Drugs': ['YES', 'NO', 'YES', 'NO', 'YES']
    })

    st.dataframe(sample_aki, use_container_width=True)

    # Sample Sepsis data
    st.subheader("Sepsis Cases (Sample)")

    sample_sepsis = pd.DataFrame({
        'Subject ID': [10006, 10017, 10027, 10040, 10056],
        'Severity': ['Sepsis (SIRS ≥2)', 'Sepsis (SIRS ≥2)', 'Sepsis (SIRS ≥2)', 'Severe Sepsis', 'Septic Shock'],
        'SIRS Criteria': ['3/4', '4/4', '2/4', '3/4', '4/4'],
        'Lactate (mmol/L)': [1.8, 1.3, None, 3.2, 4.8],
        'Antibiotics': ['YES', 'YES', 'NO', 'YES', 'YES']
    })

    st.dataframe(sample_sepsis, use_container_width=True)

    st.info("📄 Full validation results available in the GitHub repository")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Patients", "54", help="29 AKI + 25 Sepsis")
    with col2:
        st.metric("MedGemma Analyses", "10", help="5 AKI + 5 Sepsis detailed analyses")
    with col3:
        st.metric("Database", "MIMIC-III", help="Gold standard critical care dataset")

with tab4:
    st.header("🔗 Project Links")

    st.markdown("""
    ### Live Demo (GPU-Powered)
    🚀 **[Kaggle Notebook - Full Working Demo](https://www.kaggle.com/code/donlapidos/medgemma-clinical-intelligence-aki-detection)**
    - Real-time MedGemma analysis
    - Runs on Kaggle GPU (fast!)
    - All code with outputs visible
    - MIMIC-III validation included

    ### Source Code
    💻 **[GitHub Repository](https://github.com/donlapidos/medconnect-intelligence)**
    - Complete implementation
    - Documentation
    - MIMIC-III results (CSV files)
    - Setup instructions

    ### Documentation
    📚 **[Competition Submission Write-up](https://github.com/donlapidos/medconnect-intelligence/blob/main/SUBMISSION_WRITEUP.md)**
    - Detailed methodology
    - Clinical evidence
    - Technical architecture
    - Competitive analysis

    ### References
    📖 **Clinical Evidence:**
    - Despraz et al. (2026). "AI-powered learning health system for sepsis." *npj Digital Medicine*
    - 97,559 patients, 25% mortality reduction validated

    ---

    **Competition:** MedGemma Impact Challenge (Kaggle)
    **Deadline:** February 24, 2026
    **Developer:** Lionel Lapidos (Kuching, Sarawak, Malaysia)
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; margin: 2rem 0;">
    MedConnect Intelligence | Powered by MedGemma 1.5 | MedGemma Impact Challenge 2026
</div>
""", unsafe_allow_html=True)
