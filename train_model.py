"""
Spam Email Detection - TF-IDF + Logistic Regression Training
Best configuration: 10k features, trigrams, sublinear TF, C=5
"""

import pandas as pd
import re
import string
import joblib
import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("=" * 60)
print("SPAM DETECTOR - TF-IDF + LOGISTIC REGRESSION TRAINING")
print("=" * 60)

# ── 1. Load Dataset ────────────────────────────────────────────
print("\n[1/6] Loading dataset...")

if not os.path.exists("spam.tsv"):
    print("ERROR: spam.tsv not found!")
    exit()

df = pd.read_csv("spam.tsv", sep="\t", encoding="latin-1")
df = df[["label", "message"]]
df = df[df["label"].isin(["ham", "spam"])]      # drop malformed rows
df = df.dropna(subset=["message"])
df["label"] = df["label"].map({"spam": 1, "ham": 0})

print(f"  Total  : {len(df)}")
print(f"  Spam   : {df['label'].sum()}")
print(f"  Ham    : {(df['label'] == 0).sum()}")

# ── 2. Clean Text ──────────────────────────────────────────────
print("\n[2/6] Cleaning text...")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " url ", text)       # URL token
    text = re.sub(r"\S+@\S+", " email ", text)            # EMAIL token
    text = re.sub(r"\d+", " num ", text)                  # NUMBER token
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())
    return text

df["cleaned"] = df["message"].apply(clean_text)

# ── 3. Train-Test Split ────────────────────────────────────────
print("\n[3/6] Splitting dataset (80/20, stratified)...")

X_train, X_test, y_train, y_test = train_test_split(
    df["cleaned"], df["label"],
    test_size=0.2, random_state=42, stratify=df["label"]
)
print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

# ── 4. TF-IDF Vectorization ────────────────────────────────────
print("\n[4/6] Building TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 3),       # unigrams, bigrams, trigrams
    stop_words="english",
    sublinear_tf=True,        # log(1+tf) — dampens high freq terms
    min_df=2                  # ignore ultra-rare terms
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf  = vectorizer.transform(X_test)
print(f"  Features: {X_train_tfidf.shape[1]}")

# ── 5. Train Model ─────────────────────────────────────────────
print("\n[5/6] Training Logistic Regression...")

model = LogisticRegression(
    max_iter=1000,
    C=5,                      # stronger regularization relaxation
    class_weight="balanced",
    solver="lbfgs"
)
model.fit(X_train_tfidf, y_train)

# ── 6. Evaluate ────────────────────────────────────────────────
print("\n[6/6] Evaluating...")

y_pred = model.predict(X_test_tfidf)
acc = accuracy_score(y_test, y_pred)

print(f"\n  Accuracy : {acc * 100:.2f}%\n")
print("  Classification Report:")
print(classification_report(y_test, y_pred, target_names=["HAM", "SPAM"]))

cm = confusion_matrix(y_test, y_pred)
print("  Confusion Matrix:")
print(f"  TN:{cm[0][0]}  FP:{cm[0][1]}")
print(f"  FN:{cm[1][0]}  TP:{cm[1][1]}")

# ── Save ───────────────────────────────────────────────────────
print("\nSaving model files...")
joblib.dump(model,      "spam_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("  ✓ spam_model.pkl")
print("  ✓ vectorizer.pkl")


print("\n✓ Training complete!")
