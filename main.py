from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import joblib
import re

app = FastAPI()

# CORS for production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load("scam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Analytics (simple in-memory for demo)
analytics = {
    "total": 0,
    "scam": 0,
    "safe": 0,
    "suspicious": 0,
    "history": []
}

class Input(BaseModel):
    text: str

def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

@app.post("/predict")
def predict(data: Input):
    text = clean(data.text)

    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]

    try:
        prob = model.predict_proba(vec)[0][pred]
        confidence = round(prob * 100, 2)
    except:
        confidence = 60

    # Logic
    if pred == 1:
        label = "Scam" if confidence > 65 else "Suspicious"
    else:
        label = "Safe"

    # Update analytics
    analytics["total"] += 1
    analytics[label.lower()] += 1

    analytics["history"].append({
        "text": data.text[:60],
        "label": label,
        "confidence": confidence
    })

    analytics["history"] = analytics["history"][-25:]

    return {
        "label": label,
        "confidence": confidence
    }

@app.get("/analytics")
def get_analytics():
    return analytics