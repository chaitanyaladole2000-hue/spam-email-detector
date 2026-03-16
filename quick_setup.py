"""
Quick Setup - Creates model files without full training
"""

import pandas as pd
import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

print("Creating spam_model.pkl and vectorizer.pkl...")

# Simple training data
spam_emails = [
    "Congratulations! You've won a free lottery!",
    "Make money fast from home! Earn $5000!",
    "Buy cheap medications without prescription!",
    "Your account has been compromised! Click here!",
    "You've won a free iPhone! Complete survey!",
    "Click here to claim free gift card!",
    "Your package is waiting! Confirm address!",
    "Act now! Offer expires in 24 hours!",
    "You won $1,000,000! Send bank details!",
    "Free credit check! No hidden fees!",
    "Hot stock tips! Invest now!",
    "Your computer is infected! Download fix!",
    "Lowest mortgage rates! Apply today!",
    "Weight loss miracle! Lose 20 pounds!",
    "Free vacation! Just pay taxes!"
]

ham_emails = [
    "Hello, can we schedule a meeting?",
    "Please find attached the report.",
    "Thank you for your order.",
    "Hi team, reminder about meeting.",
    "Could you send updated documents?",
    "Happy birthday!",
    "Project deadline extended.",
    "Please review the proposal.",
    "Welcome to our team!",
    "Server maintenance scheduled.",
    "Thanks for registering.",
    "Order has been shipped.",
    "Please confirm attendance.",
    "Weather looks great!",
    "Meeting minutes attached."
]

# Create data
texts = spam_emails + ham_emails
labels = [1] * len(spam_emails) + [0] * len(ham_emails)

# Simple clean function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return ' '.join(text.split())

# Clean texts
cleaned_texts = [clean_text(t) for t in texts]

# Create and train model
vectorizer = TfidfVectorizer(max_features=100)
X = vectorizer.fit_transform(cleaned_texts)

model = LogisticRegression()
model.fit(X, labels)

# Save model and vectorizer
joblib.dump(model, 'spam_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Files created successfully!")
print(f"  - spam_model.pkl")
print(f"  - vectorizer.pkl")