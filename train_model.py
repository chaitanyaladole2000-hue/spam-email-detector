"""
Spam Email Detection - Final Training Script
Uses TF-IDF + Logistic Regression with proper evaluation
"""

import pandas as pd
import re
import string
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# --------------------------------------------------
# Header
# --------------------------------------------------
print("=" * 60)
print("SPAM EMAIL DETECTION - MODEL TRAINING")
print("=" * 60)

# --------------------------------------------------
# Step 1: Load Dataset
# --------------------------------------------------
print("\n[1/6] Loading dataset...")

if not os.path.exists("spam.tsv"):
    print("ERROR: spam.tsv file not found!")
    exit()

# Load dataset
df = pd.read_csv("spam.tsv", sep="\t", encoding='latin-1')

# Force correct column names
df.columns = ['label', 'message']

print(f"Dataset size: {len(df)} emails")

# Convert labels: spam → 1, ham → 0
df['label'] = df['label'].map({'spam': 1, 'ham': 0})

print(f"Spam: {sum(df['label'] == 1)} | Ham: {sum(df['label'] == 0)}")

# Remove missing values
df = df.dropna(subset=['message'])

# --------------------------------------------------
# Step 2: Text Preprocessing
# --------------------------------------------------
print("\n[2/6] Cleaning text...")

def clean_text(text):
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # Keep numbers (important for spam detection)

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove extra spaces
    text = " ".join(text.split())

    return text

df['cleaned'] = df['message'].apply(clean_text)

# --------------------------------------------------
# Step 3: Train-Test Split
# --------------------------------------------------
print("\n[3/6] Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    df['cleaned'],
    df['label'],
    test_size=0.2,
    random_state=42,
    stratify=df['label']
)

print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# --------------------------------------------------
# Step 4: Feature Extraction (TF-IDF)
# --------------------------------------------------
print("\n[4/6] Extracting features...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words='english'
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"Total features: {X_train_tfidf.shape[1]}")

# --------------------------------------------------
# Step 5: Model Training
# --------------------------------------------------
print("\n[5/6] Training model...")

model = LogisticRegression(
    max_iter=1000,
    C=2,
    class_weight='balanced'
)

model.fit(X_train_tfidf, y_train)

# --------------------------------------------------
# Step 6: Evaluation
# --------------------------------------------------
print("\n[6/6] Evaluating model...")

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["HAM", "SPAM"]))

print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"TN: {cm[0][0]}, FP: {cm[0][1]}")
print(f"FN: {cm[1][0]}, TP: {cm[1][1]}")

# --------------------------------------------------
# Save Model
# --------------------------------------------------
print("\nSaving model...")

joblib.dump(model, "spam_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model saved successfully!")

# --------------------------------------------------
# Quick Testing
# --------------------------------------------------
print("\n" + "=" * 60)
print("SAMPLE TESTING")
print("=" * 60)

test_emails = [
    "Congratulations! You have won 5000 dollars!",
    "Let's meet tomorrow for the project discussion.",
    "Limited time offer! Claim your reward now!",
    "Please review the attached document."
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

print("\nTraining completed successfully!")