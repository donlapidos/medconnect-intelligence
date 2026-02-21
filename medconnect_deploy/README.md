# MedConnect Intelligence
## Clinical Reasoning AI Co-Pilot

### Quick Start

1. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

2. **Authenticate with Hugging Face:**
   - Get token from: https://huggingface.co/settings/tokens
   - Run: `huggingface-cli login`
   - Paste your token

3. **Run the app:**
```bash
   streamlit run streamlit_app.py
```

4. **Access interface:**
   - Opens automatically at http://localhost:8501
   - Or manually navigate to that URL

### Features

- 🩺 Interactive patient data entry
- 📋 Pre-loaded clinical cases
- 💾 CSV batch processing
- 📊 Evidence-based impact metrics
- 🤖 Explainable AI reasoning

### Clinical Evidence

Based on Lausanne University Hospital study (2026):
- 25% reduction in sepsis mortality
- 131% improvement in sepsis documentation
- Earlier intervention enabled

### Technology

- **Model:** Google MedGemma 1.5 (4B parameters)
- **Hardware:** GPU recommended (works on CPU but slower)
- **Dataset:** Can analyze any patient data format

### For MedGemma Impact Challenge

- **Competition:** https://www.kaggle.com/competitions/med-gemma-impact-challenge
- **Deadline:** February 24, 2026
- **Category:** Clinical Decision Support

---

**Developer:** Lionel Lapidos
