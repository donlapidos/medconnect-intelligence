#!/bin/bash

echo "🏥 MedConnect Intelligence - Starting..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Check HF authentication
echo "Checking Hugging Face authentication..."
python -c "from huggingface_hub import whoami; whoami()" 2>/dev/null || {
    echo "⚠️  Please authenticate with Hugging Face:"
    echo "   huggingface-cli login"
    exit 1
}

echo "✅ All checks passed"
echo ""
echo "🚀 Launching MedConnect Intelligence..."
streamlit run streamlit_app.py
