import pandas as pd
import joblib
import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("spam.csv")

# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

# =========================
# TF-IDF (SMART)
# =========================
vectorizer = TfidfVectorizer(
    ngram_range=(1,3),
    stop_words='english',
    max_features=8000,
    sublinear_tf=True
)

X_vec = vectorizer.fit_transform(X)

# =========================
# MODEL (STRONG)
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_vec, y)

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "scam_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

# =========================
# TRAIN SCORE
# =========================
print("✅ Model trained successfully!")
print("📊 Training Accuracy:", round(model.score(X_vec, y) * 100, 2), "%")
print("📁 Samples Used:", len(df))
