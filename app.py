"""
Spam Email Detection Web Application
"""

from flask import Flask, render_template, request, flash, redirect, url_for
from detector import predict_spam
import os

app = Flask(__name__)
app.secret_key = 'spam_detector_secret_key_2024'

# Simple in-memory history (reset when server restarts)
# For permanent history, use a database
history = {
    'total': 0,
    'spam': 0,
    'ham': 0,
    'recent': []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global history
    
    if request.method == 'POST':
        email_text = request.form.get('email_text', '').strip()
        
        if not email_text:
            flash('Please enter email content to check!', 'error')
            return redirect(url_for('predict'))
        
        if len(email_text) < 10:
            flash('Email content is too short. Please enter more text.', 'error')
            return redirect(url_for('predict'))
        
        # Get prediction from ML model
        result = predict_spam(email_text)
        
        print("Prediction result:", result)
        
        if result['prediction'] == 'ERROR':
            flash(result['message'], 'error')
            return redirect(url_for('predict'))
        
        # Update history
        history['total'] += 1
        if result['is_spam']:
            history['spam'] += 1
        else:
            history['ham'] += 1
        
        # Add to recent (keep last 10)
        history['recent'].insert(0, {
            'email': result['email_text'],
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'is_spam': result['is_spam']
        })
        
        if len(history['recent']) > 10:
            history['recent'] = history['recent'][:10]
        
        # Render result page with history
        return render_template('result.html', result=result, email_text=email_text, history=history)
    
    return render_template('predict.html', history=history)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/check-again')
def check_again():
    return redirect(url_for('predict'))

@app.route('/clear-history')
def clear_history():
    global history
    history = {
        'total': 0,
        'spam': 0,
        'ham': 0,
        'recent': []
    }
    flash('History cleared!', 'success')
    return redirect(url_for('predict'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Page not found!"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('index.html', error="Internal server error!"), 500

if __name__ == '__main__':
    if not os.path.exists('spam_model.pkl') or not os.path.exists('vectorizer.pkl'):
        print("\n" + "="*60)
        print("WARNING: Model files not found!")
        print("Please run 'python train_model.py' first!")
        print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)