"""
Spam Email Detection Module
"""

import joblib
import re
import string

# Global variables
model = None
vectorizer = None

def load_model():
    """Load the trained model and vectorizer"""
    global model, vectorizer
    try:
        model = joblib.load('spam_model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        print("Model loaded successfully!")
        return True
    except FileNotFoundError:
        print("ERROR: Model files not found!")
        return False

def clean_text(text):
    """Clean and preprocess email text"""
    if not text:
        return ""
    
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    
    return text

def predict_spam(email_text):
    """
    Predict if an email is spam or not
    """
    if model is None or vectorizer is None:
        if not load_model():
            return {
                'prediction': 'ERROR',
                'is_spam': False,
                'confidence': 0.0,
                'spam_probability': 0.0,
                'ham_probability': 0.0,
                'message': 'Model not loaded. Please train the model first!',
                'top_spam_words': [],
                'top_ham_words': []
            }
    
    if not email_text or not email_text.strip():
        return {
            'prediction': 'ERROR',
            'is_spam': False,
            'confidence': 0.0,
            'spam_probability': 0.0,
            'ham_probability': 0.0,
            'message': 'Please enter email content.',
            'top_spam_words': [],
            'top_ham_words': []
        }
    
    try:
        cleaned_text = clean_text(email_text)
        text_tfidf = vectorizer.transform([cleaned_text])
        
        prediction = model.predict(text_tfidf)[0]
        probabilities = model.predict_proba(text_tfidf)[0]
        confidence = max(probabilities) * 100
        
        # Get feature names and their importance
        feature_names = vectorizer.get_feature_names_out()
        tfidf_array = text_tfidf.toarray()[0]
        
        # Get top words for spam and ham
        word_importance = []
        for i, (word, score) in enumerate(zip(feature_names, tfidf_array)):
            if score > 0:
                word_importance.append((word, score))
        
        word_importance.sort(key=lambda x: x[1], reverse=True)
        top_words = word_importance[:5]
        
        result = {
            'prediction': 'SPAM' if prediction == 1 else 'HAM (Not Spam)',
            'is_spam': bool(prediction),
            'confidence': round(float(confidence), 2),
            'spam_probability': round(float(probabilities[1] * 100), 2),
            'ham_probability': round(float(probabilities[0] * 100), 2),
            'message': 'This email appears to be spam!' if prediction == 1 else 'This email appears to be legitimate!',
            'top_words': top_words,
            'email_text': email_text[:200] + "..." if len(email_text) > 200 else email_text
        }
        
        return result
        
    except Exception as e:
        return {
            'prediction': 'ERROR',
            'is_spam': False,
            'confidence': 0.0,
            'spam_probability': 0.0,
            'ham_probability': 0.0,
            'message': f'Error during prediction: {str(e)}',
            'top_words': [],
            'top_spam_words': [],
            'top_ham_words': []
        }

# Load model on module import
model_loaded = load_model()