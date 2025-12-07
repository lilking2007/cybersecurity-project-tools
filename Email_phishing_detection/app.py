import streamlit as st
import pandas as pd
from src.model import load_model, predict_email
from src.features import MetadataExtractor

st.set_page_config(
    page_title="Phishing Email Detector",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #1f2937;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stTextArea textarea {
        background-color: #f9fafb;
        color: #000000;
        border: 1px solid #d1d5db;
        border-radius: 5px;
    }
    .stButton>button {
        color: white;
        background-color: #3b82f6;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    .safe {
        color: #10b981;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .phishing {
        color: #ef4444;
        font-weight: bold;
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Phishing Email Detector")
st.markdown("Analyze email content to detect potential phishing attempts using AI.")

# Load Model
@st.cache_resource
def get_model():
    return load_model()

model = get_model()
if model is None:
    st.error("Model could not be loaded. Please ensure training has been run.")

# Input Section
email_content = st.text_area("Paste Email Content Here", height=200, placeholder="Subject: Urgent Action Required...\n\nDear User, ...")

if st.button("Analyze Email"):
    if email_content:
        with st.spinner("Analyzing..."):
            prediction, probability = predict_email(model, email_content)
            
            # Display Result
            st.markdown("---")
            if prediction == 1:
                st.markdown(f"<p class='phishing'>🚨 Suspicious Activity Detected (Phishing)</p>", unsafe_allow_html=True)
                st.progress(int(probability * 100))
                st.write(f"Confidence Score: **{probability*100:.2f}%**")
                
                # Simple heuristic explanations
                st.subheader("Why?")
                extractor = MetadataExtractor()
                meta_features = extractor.transform([email_content])[0]
                # [url_count, keyword_count, length]
                if meta_features[0] > 0:
                    st.warning(f"Contains {meta_features[0]} URL(s). Be careful with links.")
                if meta_features[1] > 0:
                    st.warning(f"Contains {meta_features[1]} suspicious keyword(s) (e.g., 'urgent', 'verify').")
            else:
                st.markdown(f"<p class='safe'>✅ Email seems Safe</p>", unsafe_allow_html=True)
                st.progress(int((1-probability) * 100))
                st.write(f"Confidence Score: **{(1-probability)*100:.2f}%**")
                
    else:
        st.warning("Please enter some text to analyze.")

st.markdown("---")
st.caption("Powered by Scikit-Learn • Random Forest Classifier")

if __name__ == "__main__":
    import os
    import sys
    import subprocess
    
    # Prevent recursive execution by checking if running inside the launcher context
    if not os.environ.get("STREAMLIT_LAUNCHER_ACTIVE"):
        env = os.environ.copy()
        env["STREAMLIT_LAUNCHER_ACTIVE"] = "true"
        # Run the streamlit app using the current python executable
        subprocess.run([sys.executable, "-m", "streamlit", "run", __file__], env=env)
