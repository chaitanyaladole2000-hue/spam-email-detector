"""
Quick Setup Script (Uses spam.tsv with label + message)
"""

import pandas as pd
import re
import string
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("=" * 60)
print("QUICK SETUP - USING spam.tsv (label + message)")
print("=" * 60)

# --------------------------------------------------
# Step 1: Check dataset
# --------------------------------------------------
if not os.path.exists("spam.tsv"):
    print("\nERROR: spam.tsv file not found!")
    exit()

print("\nLoading dataset...")
df = pd.read_csv("spam.tsv", sep="\t", encoding='latin-1')

# Fix column names explicitly
df.columns = ['label', 'message']

print(f"Dataset loaded: {len(df)} emails")

# Convert labels → numeric
df['label'] = df['label'].map({'spam': 1, 'ham': 0})

# Remove missing values
df = df.dropna(subset=['message'])

# --------------------------------------------------
# Step 2: Clean text
# --------------------------------------------------
def clean_text(text):
    text = str(text).lower()

    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)

    # Keep numbers

    text = text.translate(str.maketrans('', '', string.punctuation))
    text = " ".join(text.split())

    return text

print("\nCleaning text...")
df['cleaned'] = df['message'].apply(clean_text)

# --------------------------------------------------
# Step 3: Feature extraction
# --------------------------------------------------
print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 2),
    stop_words='english'
)

X = vectorizer.fit_transform(df['cleaned'])
y = df['label']

print(f"Features created: {X.shape[1]}")

# --------------------------------------------------
# Step 4: Train model
# --------------------------------------------------
print("\nTraining model...")

model = LogisticRegression(
    max_iter=500,
    class_weight='balanced'
)

model.fit(X, y)

print("Model trained successfully!")

# --------------------------------------------------
# Step 5: Save model
# --------------------------------------------------
print("\nSaving model files...")

joblib.dump(model, "spam_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Files created successfully!")

# --------------------------------------------------
# Step 6: Quick Test
# --------------------------------------------------
print("\n" + "=" * 60)
print("QUICK TEST")
print("=" * 60)

test_emails = [
    "Win 5000 rupees now!",
    "Let's meet tomorrow",
    "Limited time offer, claim reward",
    "Please check the report"
]

for email in test_emails:
    cleaned = clean_text(email)
    vec = vectorizer.transform([cleaned])

    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]

    label = "SPAM" if pred == 1 else "HAM"
    confidence = max(prob) * 100

    print(f"\nEmail: {email}")
    print(f"Prediction: {label} ({confidence:.2f}%)")

print("\nQuick setup completed successfully!")