"""
Spam Email Detection Model Training Script
This script trains the model on the spam.tsv file
"""

import pandas as pd
import numpy as np
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

print("=" * 60)
print("SPAM EMAIL DETECTION MODEL TRAINING")
print("=" * 60)

# Step 1: Load dataset from TSV file
print("\n[1/5] Loading dataset from spam.tsv...")
if not os.path.exists('spam.tsv'):
    print("ERROR: spam.tsv not found!")
    print("Please create spam.tsv with 'text' and 'label' columns.")
    exit(1)

# Read TSV file (tab-separated)
df = pd.read_csv('spam.tsv', sep='\t')

print(f"    Dataset loaded: {len(df)} samples")
print(f"    Columns: {list(df.columns)}")

# Check if required columns exist
if 'text' not in df.columns or 'label' not in df.columns:
    print("ERROR: spam.tsv must have 'text' and 'label' columns!")
    print(f"Found columns: {list(df.columns)}")
    exit(1)

print(f"    Spam samples: {sum(df['label'] == 1)}")
print(f"    Ham samples: {sum(df['label'] == 0)}")

# Check for missing values
if df['text'].isnull().any():
    print("    Warning: Found missing values. Cleaning...")
    df = df.dropna(subset=['text'])
    print(f"    After cleaning: {len(df)} samples")

# Step 2: Preprocess text
print("\n[2/5] Preprocessing text data...")

def clean_text(text):
    """Clean and preprocess email text"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    
    return text

df['cleaned_text'] = df['text'].apply(clean_text)
print("    Text cleaning completed!")

# Step 3: Split data
print("\n[3/5] Splitting data into train and test sets...")
X = df['cleaned_text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"    Training samples: {len(X_train)}")
print(f"    Testing samples: {len(X_test)}")

# Step 4: Create TF-IDF features
print("\n[4/5] Creating TF-IDF features...")
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
print(f"    Feature extraction completed!")
print(f"    Number of features: {X_train_tfidf.shape[1]}")

# Step 5: Train Model
print("\n[5/5] Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_tfidf, y_train)
print("    Model training completed!")

# Step 6: Evaluate Model
print("\n[EVALUATING] Model performance...")
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n    ACCURACY: {accuracy * 100:.2f}%")
print("\n    CLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred, target_names=['HAM', 'SPAM']))

print("\n    CONFUSION MATRIX:")
cm = confusion_matrix(y_test, y_pred)
print(f"    True Negatives: {cm[0][0]}, False Positives: {cm[0][1]}")
print(f"    False Negatives: {cm[1][0]}, True Positives: {cm[1][1]}")

# Step 7: Save model and vectorizer
print("\n[SAVING] Saving model and vectorizer...")
joblib.dump(model, 'spam_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("    Model saved as 'spam_model.pkl'")
print("    Vectorizer saved as 'vectorizer.pkl'")

# Verify files exist
if os.path.exists('spam_model.pkl') and os.path.exists('vectorizer.pkl'):
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nModel is ready to predict new emails!")
else:
    print("\nERROR: Files were not created properly!")

# Step 8: Test with sample predictions
print("\n" + "=" * 60)
print("TESTING WITH SAMPLE EMAILS")
print("=" * 60)

test_emails = [
    "Congratulations! You've won a lottery!",
    "Can we schedule a meeting for tomorrow?",
    "Make money fast from home!",
    "Please find attached the report."
]

for email in test_emails:
    cleaned = clean_text(email)
    tfidf = vectorizer.transform([cleaned])
    prediction = model.predict(tfidf)[0]
    probs = model.predict_proba(tfidf)[0]
    
    result = "SPAM" if prediction == 1 else "HAM"
    confidence = max(probs) * 100
    
    print(f"\nEmail: {email}")
    print(f"Prediction: {result} ({confidence:.2f}%)")