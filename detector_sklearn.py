"""
Spam Detector - TF-IDF + Logistic Regression
Fallback model used when distilbert_model/ is not available.
"""

import joblib
import re
import string
import os

# ── Load model files ───────────────────────────────────────────
_MODEL_PATH      = "spam_model.pkl"
_VECTORIZER_PATH = "vectorizer.pkl"

_model      = None
_vectorizer = None

def _load():
    global _model, _vectorizer
    if _model is None:
        if not os.path.exists(_MODEL_PATH) or not os.path.exists(_VECTORIZER_PATH):
            raise FileNotFoundError(
                "sklearn model files not found. Run train_model.py first."
            )
        _model      = joblib.load(_MODEL_PATH)
        _vectorizer = joblib.load(_VECTORIZER_PATH)

# ── Text cleaning (must match train_model.py) ──────────────────
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " url ", text)
    text = re.sub(r"\S+@\S+", " email ", text)
    text = re.sub(r"\d+", " num ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())
    return text

# ── Prediction ─────────────────────────────────────────────────
def predict_spam(text):
    try:
        _load()
        cleaned  = clean_text(text)
        vec      = _vectorizer.transform([cleaned])
        pred     = _model.predict(vec)[0]
        prob     = _model.predict_proba(vec)[0]
        label    = "SPAM" if pred == 1 else "HAM"
        confidence = float(max(prob))
        return {
            "label":      label,
            "prediction": label,
            "confidence": confidence,
            "is_spam":    label == "SPAM",
            "email_text": text,
            "model_used": "sklearn"
        }
    except Exception as e:
        return {
            "label":      "ERROR",
            "prediction": "ERROR",
            "confidence": 0.0,
            "is_spam":    False,
            "email_text": text,
            "message":    str(e),
            "model_used": "sklearn"
        }
