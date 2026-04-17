import joblib
import re
import numpy as np

model = joblib.load("scam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# =========================
# SMART FEATURES
# =========================
def extract_risk_features(text):
    text_lower = text.lower()

    return [
        len(text),
        int(any(c.isdigit() for c in text)),
        int("http" in text or "www" in text),
        int("urgent" in text_lower),
        int("verify" in text_lower),
        int("bank" in text_lower),
        int("money" in text_lower),
        int("click" in text_lower)
    ]

scam_keywords = [
    "win", "free", "urgent", "click", "prize",
    "lottery", "bank", "account", "verify",
    "password", "reward", "atm", "suspended"
]

# =========================
# PREDICTION FUNCTION
# =========================
def predict_scam(text):
    cleaned = clean_text(text)

    vec = vectorizer.transform([cleaned])

    # Risk scoring
    features = extract_risk_features(text)
    risk_score = sum(features) * 5

    # ML prediction
    prediction = model.predict(vec)[0]

    try:
        prob = model.predict_proba(vec)[0][prediction]
        confidence = round(prob * 100, 2)
    except:
        confidence = 60

    # Keyword detection
    found_keywords = [w for w in scam_keywords if w in cleaned]

    # =========================
    # SMART DECISION LOGIC
    # =========================
    if prediction == 1 or risk_score > 50:
        label = "Scam"
        confidence = max(confidence, 75)

    elif confidence < 55:
        label = "Suspicious"

    else:
        label = "Safe"

    return {
        "label": label,
        "confidence": confidence,
        "keywords_detected": found_keywords,
        "risk_score": risk_score,
        "message": "Hybrid AI (ML + Rules + Risk Engine)"
    }