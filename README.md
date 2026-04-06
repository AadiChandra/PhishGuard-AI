# 🛡️ PhishGuard AI - Phishing URL Detector

A Machine Learning-based web application that detects phishing URLs using feature extraction and classification techniques.

## 🚀 Features
- Detects phishing vs legitimate URLs
- Uses Random Forest model
- Extracts URL-based features
- Interactive UI using Streamlit
- Displays threat score and analysis

## 🧠 Tech Stack
- Python
- Scikit-learn
- Streamlit
- Pandas

## 📂 Project Files
- app.py → Streamlit UI
- train_model.py → Model training
- feature_extractor.py → Feature extraction
- dataset.csv → Training dataset
- model.pkl → Trained model

## ▶️ How to Run

```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
