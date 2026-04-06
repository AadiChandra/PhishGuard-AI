import streamlit as st
import joblib
import pandas as pd

from feature_extractor import extract_features

# Load model
model = joblib.load("model.pkl")

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    .title-style {
        font-size: 38px;
        font-weight: 700;
        color: #f8fafc;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle-style {
        font-size: 18px;
        color: #cbd5e1;
        text-align: center;
        margin-bottom: 30px;
    }
    .card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
        color: white;
        margin-bottom: 20px;
    }
    .safe-box {
        background-color: #064e3b;
        color: #d1fae5;
        padding: 18px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
    }
    .danger-box {
        background-color: #7f1d1d;
        color: #fee2e2;
        padding: 18px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
    }
    .info-text {
        color: #e2e8f0;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="title-style">🛡️ PhishGuard AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-style">Detect suspicious URLs using Machine Learning and basic cyber security features</div>',
    unsafe_allow_html=True
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("📌 About Project")
    st.write("""
    This project analyzes a URL and predicts whether it is:
    - **Legitimate**
    - **Phishing**
    
    It uses:
    - URL-based feature extraction
    - Machine Learning model
    - Streamlit UI
    """)

    st.header("🧪 Try Example URLs")
    st.code("https://www.google.com")
    st.code("http://verify-paytm-login-free-offer.xyz")
    st.code("http://claim-prize-money-now.ml")

    st.header("💡 Safety Tips")
    st.write("""
    - Check if URL uses **HTTPS**
    - Avoid links with too many **hyphens**
    - Be careful with words like **login**, **verify**, **free**, **claim**
    - Never enter passwords on suspicious websites
    """)

# ---------- Input Section ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
url = st.text_input("🔗 Enter URL to analyze:", placeholder="Example: https://www.google.com")
check_button = st.button("🚀 Analyze URL")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Prediction ----------
if check_button:
    if url.strip() == "":
        st.warning("Please enter a URL first.")
    else:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        features = extract_features(url)
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]

        phishing_confidence = probability[1] * 100
        legitimate_confidence = probability[0] * 100

        # Threat score
        threat_score = int(phishing_confidence)

        # Result Section
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔍 URL Length", len(url))

        with col2:
            st.metric("⚠️ Threat Score", f"{threat_score}/100")

        with col3:
            if prediction == 1:
                st.metric("🚨 Prediction", "Phishing")
            else:
                st.metric("✅ Prediction", "Legitimate")

        st.subheader("Confidence Level")
        st.progress(threat_score if threat_score <= 100 else 100)

        if prediction == 1:
            st.markdown(
                f'<div class="danger-box">⚠️ Warning: This URL is predicted as <b>PHISHING</b><br>Confidence: {phishing_confidence:.2f}%</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="safe-box">✅ This URL is predicted as <b>LEGITIMATE</b><br>Confidence: {legitimate_confidence:.2f}%</div>',
                unsafe_allow_html=True
            )

        # Risk Level
        st.subheader("Risk Level")
        if threat_score < 30:
            st.success("Low Risk")
        elif threat_score < 70:
            st.warning("Medium Risk")
        else:
            st.error("High Risk")

        # Feature Table
        st.subheader("Extracted Features")

        feature_names = [
            "URL Length",
            "Has HTTPS",
            "Dot Count",
            "Hyphen Count",
            "Slash Count",
            "Digit Count",
            "Has @ Symbol",
            "Has IP Address",
            "Suspicious Word Count",
            "Domain Length"
        ]

        feature_df = pd.DataFrame({
            "Feature": feature_names,
            "Value": features
        })

        st.dataframe(feature_df, use_container_width=True)

        # Interpretation
        st.subheader("Analysis Summary")

        reasons = []

        if features[1] == 0:
            reasons.append("URL does not use HTTPS")
        if features[3] > 2:
            reasons.append("URL contains many hyphens")
        if features[6] == 1:
            reasons.append("URL contains @ symbol")
        if features[7] == 1:
            reasons.append("URL uses an IP address instead of a normal domain")
        if features[8] > 0:
            reasons.append("URL contains suspicious keywords like login, verify, free, claim")
        if len(url) > 50:
            reasons.append("URL is unusually long")

        if reasons:
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.write("- No major suspicious pattern detected from current feature set.")

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Built with ❤️ using Python, Scikit-learn, and Streamlit</p>",
    unsafe_allow_html=True
)