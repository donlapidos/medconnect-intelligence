
import streamlit as st
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

# Page config
st.set_page_config(
    page_title="MedConnect Intelligence",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better styling
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏥 MedConnect Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Clinical Reasoning AI Co-Pilot | Powered by MedGemma 1.5</div>', unsafe_allow_html=True)

# Sidebar - Clinical Evidence
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
    st.markdown("**Advantages:**")
    st.markdown("✓ Explainable reasoning")
    st.markdown("✓ Multi-modal analysis")
    st.markdown("✓ Works anywhere")
    
    st.divider()
    
    st.header("📈 Impact Potential")
    st.markdown("**Per Lausanne:**")
    st.markdown("• Earlier intervention")
    st.markdown("• Better documentation")
    st.markdown("• Lives saved")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🩺 Clinical Analysis", 
    "📋 Pre-loaded Cases", 
    "💾 CSV Upload",
    "📖 About"
])

# === HUGGING FACE AUTHENTICATION (Cloud-ready) ===
import os
from huggingface_hub import login

# Try Streamlit secrets first (cloud), then environment variable (local)
try:
    HF_TOKEN = st.secrets["huggingface"]["token"]
    login(token=HF_TOKEN)
except:
    # Fallback to environment variable for local development
    HF_TOKEN = os.getenv('HF_TOKEN')
    if HF_TOKEN:
        try:
            login(token=HF_TOKEN)
        except:
            pass
# === END AUTHENTICATION ===

# Initialize session state for model
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.model = None
    st.session_state.tokenizer = None

# Load model function
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/medgemma-1.5-4b-it")
    
    # CPU-friendly loading (slower but works everywhere)
    model = AutoModelForCausalLM.from_pretrained(
        "google/medgemma-1.5-4b-it",
        torch_dtype=torch.float32,
        device_map="cpu",
        low_cpu_mem_usage=True
    )
    return tokenizer, model

# Inference function
def ask_medgemma_ui(prompt, max_tokens=1000):
    if not st.session_state.model_loaded:
        tokenizer, model = load_model()
        st.session_state.tokenizer = tokenizer
        st.session_state.model = model
        st.session_state.model_loaded = True
    
    inputs = st.session_state.tokenizer(prompt, return_tensors="pt").to("cpu")
    outputs = st.session_state.model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=False
    )
    response = st.session_state.tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("model\n")[-1].strip()

# Tab 1: Manual Input
with tab1:
    st.header("Enter Patient Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Laboratory Values")
        creatinine_current = st.number_input("Creatinine (current, mg/dL)", 0.0, 20.0, 2.8, 0.1)
        creatinine_baseline = st.number_input("Creatinine (baseline, mg/dL)", 0.0, 5.0, 1.0, 0.1)
        bun = st.number_input("BUN (mg/dL)", 0, 200, 45, 1)
        urine_output = st.number_input("24hr Urine Output (mL)", 0, 5000, 350, 50)
        
        st.subheader("Vital Signs (Optional)")
        temp = st.number_input("Temperature (°C)", 35.0, 42.0, 37.0, 0.1)
        heart_rate = st.number_input("Heart Rate (bpm)", 40, 200, 80, 1)
        resp_rate = st.number_input("Respiratory Rate", 8, 60, 16, 1)
        bp_systolic = st.number_input("BP Systolic (mmHg)", 60, 250, 120, 1)
    
    with col2:
        st.subheader("Medications")
        medications_text = st.text_area(
            "Current medications (one per line)",
            "Ibuprofen 800mg TID\nLisinopril 10mg daily\nMetformin 500mg BID",
            height=150
        )
        
        st.subheader("Patient Context")
        age = st.number_input("Age (years)", 18, 120, 65, 1)
        sex = st.selectbox("Sex", ["Male", "Female"])
        
        clinical_notes = st.text_area(
            "Clinical Notes (optional)",
            "Patient reports decreased urine output and fatigue",
            height=100
        )
    
    if st.button("🔍 Analyze Patient", type="primary", use_container_width=True):
        
        # Build comprehensive prompt
        medications_list = [m.strip() for m in medications_text.split("\n") if m.strip()]
        
        prompt = f"""Analyze this patient's clinical data:

Patient: {age}-year-old {sex}

Current Labs:
- Serum creatinine: {creatinine_current} mg/dL (baseline: {creatinine_baseline} mg/dL)
- Blood urea nitrogen (BUN): {bun} mg/dL
- Urine output: {urine_output} mL in 24 hours

Vital Signs:
- Temperature: {temp}°C
- Heart rate: {heart_rate} bpm
- Respiratory rate: {resp_rate} breaths/min
- Blood pressure: {bp_systolic}/? mmHg

Current Medications:
{chr(10).join(f"- {med}" for med in medications_list)}

Clinical Notes:
{clinical_notes}

Provide comprehensive analysis including:
1. Most likely diagnosis
2. Clinical reasoning connecting these parameters
3. Severity assessment
4. Immediate recommended actions
5. Risk factors and complications to monitor"""

        with st.spinner("🤖 MedGemma analyzing patient data..."):
            
            # Show comparison panels
            col_trad, col_ai = st.columns(2)
            
            with col_trad:
                st.markdown("### ❌ Traditional EMR System")
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown("**📊 Lab Alerts:**")
                if creatinine_current > 1.3:
                    st.markdown(f"⚠️ Creatinine: {creatinine_current} mg/dL **HIGH**")
                if bun > 20:
                    st.markdown(f"⚠️ BUN: {bun} mg/dL **HIGH**")
                if urine_output < 400:
                    st.markdown(f"⚠️ Low urine output: {urine_output} mL")
                
                st.markdown("**❌ No Clinical Synthesis**")
                st.markdown("**❌ No Medication Analysis**")
                st.markdown("**❌ No Action Recommendations**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.warning("⚠️ Nurse must manually recognize patterns → Delayed intervention")
            
            with col_ai:
                st.markdown("### ✅ MedConnect Intelligence")
                
                # Get AI response
                response = ask_medgemma_ui(prompt, max_tokens=1000)
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("**🤖 AI Clinical Reasoning:**")
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show evidence-based impact
            st.divider()
            st.markdown("### 📊 Evidence-Based Impact (Lausanne Study)")
            
            impact_col1, impact_col2, impact_col3 = st.columns(3)
            
            with impact_col1:
                st.metric(
                    "In-Hospital Mortality",
                    "15.3%",
                    delta="-5.2%",
                    delta_color="inverse",
                    help="With AI: 15.3% vs Without AI: 20.5%"
                )
            
            with impact_col2:
                st.metric(
                    "90-Day Mortality", 
                    "26.1%",
                    delta="-6.9%",
                    delta_color="inverse",
                    help="With AI: 26.1% vs Without AI: 33.0%"
                )
            
            with impact_col3:
                st.metric(
                    "Sepsis Documentation",
                    "3.58%",
                    delta="+2.03%",
                    help="With AI: 3.58% vs Without AI: 1.55%"
                )

# Tab 2: Pre-loaded Cases
with tab2:
    st.header("📋 Pre-loaded Clinical Cases")
    
    case_option = st.selectbox(
        "Select a clinical scenario:",
        [
            "1. Drug-Induced Acute Kidney Injury (AKI)",
            "2. Sepsis Secondary to UTI",
            "3. Diabetic Ketoacidosis with AKI"
        ]
    )
    
    if "Drug-Induced" in case_option:
        st.markdown("**Case 1: 65-year-old male with drug-induced AKI**")
        st.json({
            "creatinine_current": "2.8 mg/dL",
            "creatinine_baseline": "1.0 mg/dL",
            "bun": "45 mg/dL",
            "urine_output": "350 mL/24hr",
            "medications": ["Ibuprofen 800mg TID", "Lisinopril 10mg", "Metformin 500mg"]
        })
        
        if st.button("Analyze Case 1", type="primary"):
            prompt = """Analyze this patient:

65-year-old male
Creatinine: 2.8 mg/dL (baseline 1.0 mg/dL)
BUN: 45 mg/dL  
Urine output: 350 mL/24hr
Medications: Ibuprofen 800mg TID, Lisinopril, Metformin

Provide diagnosis, reasoning, and immediate actions."""
            
            with st.spinner("Analyzing..."):
                response = ask_medgemma_ui(prompt)
                st.success("**MedGemma Analysis:**")
                st.markdown(response)
    
    elif "Sepsis" in case_option:
        st.markdown("**Case 2: Elderly patient with UTI-related sepsis**")
        st.json({
            "temperature": "38.9°C",
            "heart_rate": "118 bpm",
            "respiratory_rate": "24 breaths/min",
            "wbc": "18.5 × 10⁹/L",
            "lactate": "3.2 mmol/L",
            "bp": "95/58 mmHg"
        })
        
        if st.button("Analyze Case 2", type="primary"):
            prompt = """Analyze this patient:

Elderly patient with UTI symptoms
Temperature: 38.9°C
Heart Rate: 118 bpm
Respiratory Rate: 24 breaths/min
WBC: 18.5 × 10⁹/L
Lactate: 3.2 mmol/L
Blood Pressure: 95/58 mmHg

Calculate SIRS criteria, qSOFA score, diagnose, and recommend immediate actions."""
            
            with st.spinner("Analyzing..."):
                response = ask_medgemma_ui(prompt)
                st.success("**MedGemma Analysis:**")
                st.markdown(response)

# Tab 3: CSV Upload
with tab3:
    st.header("💾 Upload Patient Data (CSV)")
    
    st.markdown("""
    Upload a CSV file with patient data. Required columns:
    - `creatinine_current`, `creatinine_baseline`, `bun`, `urine_output`
    - Optional: `temperature`, `heart_rate`, `respiratory_rate`, `bp_systolic`, `wbc`, `lactate`
    """)
    
    uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
    
    if uploaded_file is not None:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        
        st.success(f"✅ Loaded {len(df)} patients")
        st.dataframe(df.head())
        
        if st.button("Analyze All Patients", type="primary"):
            st.info("🔄 Analyzing patients... (This may take a few minutes)")
            
            results = []
            progress_bar = st.progress(0)
            
            for idx, row in df.iterrows():
                # Build prompt from row data
                prompt = f"""Analyze patient:
Creatinine: {row.get('creatinine_current')} mg/dL (baseline: {row.get('creatinine_baseline', 'unknown')})
BUN: {row.get('bun')} mg/dL
Urine: {row.get('urine_output')} mL/24hr

Provide brief diagnosis and severity (1-2 sentences)."""
                
                response = ask_medgemma_ui(prompt, max_tokens=200)
                results.append({
                    'patient_id': idx + 1,
                    'diagnosis': response[:150] + "..." if len(response) > 150 else response
                })
                
                progress_bar.progress((idx + 1) / len(df))
            
            st.success("✅ Analysis complete!")
            st.dataframe(pd.DataFrame(results))

# Tab 4: About
with tab4:
    st.header("📖 About MedConnect Intelligence")
    
    st.markdown("""
    ### The Problem
    
    Even advanced hospital EMR systems (like Singapore's EPIC) flag individual abnormal values 
    but **don't connect the dots** to suggest diagnoses. Nurses must manually recognize patterns 
    across 20+ parameters while managing multiple patients.
    
    ### The Solution
    
    **MedConnect Intelligence** provides an AI-powered clinical reasoning layer that:
    - Synthesizes multiple parameters simultaneously
    - Identifies medication interactions and contraindications
    - Calculates clinical scores (SIRS, qSOFA, SOFA)
    - Provides explainable reasoning (not black box)
    - Works across ANY infrastructure level
    
    ### Clinical Evidence
    
    **Lausanne University Hospital Study (2026)**
    - Published in *npj Digital Medicine*
    - 97,559 patient stays analyzed
    - **25% mortality reduction** with AI-assisted sepsis detection
    - Improved documentation and earlier intervention
    
    ### Technology Stack
    
    - **Foundation Model:** Google MedGemma 1.5 (4B parameters)
    - **Training:** Pre-trained on millions of medical cases
    - **Capabilities:** Multimodal (text, imaging, EHR data)
    - **Deployment:** API-based (works anywhere)
    
    ### Competitive Advantage
    
    | Traditional EMR | Lausanne HERACLES | MedConnect Intelligence |
    |-----------------|-------------------|-------------------------|
    | Individual flags | Sepsis probability | Full clinical reasoning |
    | No synthesis | Black box ML | Explainable AI |
    | Manual pattern recognition | Automated detection | Automated + Explained |
    | - | Hospital-specific | Works anywhere |
    
    ### Next Steps
    
    1. **Validation:** Test with MIMIC-III dataset
    2. **UI Enhancement:** Mobile-friendly interface
    3. **Integration:** FHIR API for EMR systems
    4. **Expansion:** Additional clinical conditions
    
    ---
    
    **Built for:** MedGemma Impact Challenge (Kaggle)  
    **Developer:** Gotalk Studios  
    **Deadline:** February 24, 2026
    """)
    
    st.divider()
    
    st.markdown("### 📚 References")
    st.markdown("""
    1. Despraz, J., et al. (2026). An artificial intelligence-powered learning health system 
       to improve sepsis detection and quality of care. *npj Digital Medicine*.
    2. Google Health AI. (2026). MedGemma 1.5: Next generation medical image interpretation.
    3. Singer, M., et al. (2016). Sepsis-3 Consensus Definitions. *JAMA*.
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    MedConnect Intelligence | Powered by MedGemma 1.5 | MedGemma Impact Challenge 2026
</div>
""", unsafe_allow_html=True)
