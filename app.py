from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import joblib
import json
import os
import numpy as np
import re
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, db
from absa import AspectBasedSentimentAnalyzer



app = Flask(__name__)
app.secret_key = "sentimentanalysiskey"  # Required for flash messages

# Load the model and vectorizer
MODEL_PATH = os.path.join('models', 'svm_model.pkl')
VECTORIZER_PATH = os.path.join('models', 'tfidf_vectorizer.pkl')

# Initialize Aspect-Based Sentiment Analyzer
absa_analyzer = AspectBasedSentimentAnalyzer()

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model and vectorizer loaded successfully!")
except Exception as e:
    print(f"Error loading model or vectorizer: {e}")
    model = None
    vectorizer = None

# Text preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

# Sentiment analysis function
# def analyze_sentiment(text):
#     if model is None or vectorizer is None:
#         return "Error: Model or vectorizer not loaded", "neutral"
    
#     # Preprocess the text
#     preprocessed_text = preprocess_text(text)
    
#     # Vectorize the text
#     text_vectorized = vectorizer.transform([preprocessed_text])
    
#     # Predict sentiment
#     prediction = model.predict(text_vectorized)[0]
    
#     # Get prediction probabilities
#     probabilities = model.predict(text_vectorized)[0]
#     confidence = round(np.max(probabilities) * 100, 2)
    
#     # Determine sentiment label and class
#     if prediction == 1:
#         sentiment = "Positive"
#         sentiment_class = "positive"
#     elif prediction == -1:
#         sentiment = "Negative"
#         sentiment_class = "negative"
#     # else:
#     #     sentiment = "Neutral"
#     #     sentiment_class = "neutral"
    
#     result = {
#         "sentiment": sentiment,
#         "confidence": confidence,
#         "sentiment_class": sentiment_class,
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
    
#     return result
def analyze_sentiment(text):
    if model is None or vectorizer is None:
        return "Error: Model or vectorizer not loaded", "neutral"
    
    # Preprocess the text
    preprocessed_text = preprocess_text(text)
    
    # Vectorize the text
    text_vectorized = vectorizer.transform([preprocessed_text])
    
    # Predict sentiment
    prediction = model.predict(text_vectorized)[0]
    
    # Get prediction probabilities
    probabilities = model.predict(text_vectorized)[0]
    confidence = round(np.max(probabilities) * 100, 2)
    
    # Determine sentiment label and class
    if prediction == 1:
        sentiment = "Positive"
        sentiment_class = "positive"
    elif prediction == -1:
        sentiment = "Negative"
        sentiment_class = "negative"
    else:
        # If neither positive nor negative, default to negative
        sentiment = "Negative"
        sentiment_class = "negative"
    
    result = {
        "sentiment": sentiment,
        "confidence": confidence,
        "sentiment_class": sentiment_class,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return result

# Routes
# @app.route('/')
# def home():
#     return render_template('index.html')



@app.route('/')
def home():
    return render_template('index.html')
    
    # return render_template('index.html', current_year=datetime.now().year)

# @app.route('/analyze', methods=['GET', 'POST'])
# def analyze():
#     if request.method == 'POST':
#         text = request.form.get('text', '')
        
#         if not text:
#             flash('Please enter some text to analyze', 'warning')
#             return redirect(url_for('analyze'))
        
#         result = analyze_sentiment(text)
#         return render_template('result.html', text=text, result=result)
    
#     return render_template('analyze.html')
# ... [Rest of the existing code remains the same]

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        text = request.form.get('text', '')
        
        if not text:
            flash('Please enter some text to analyze', 'warning')
            return redirect(url_for('analyze'))
        
        # Get overall sentiment
        result = analyze_sentiment(text)
        
        # Get aspect-based sentiments
        aspect_results = absa_analyzer.extract_aspect_sentiments(text)
        
        return render_template('result.html', text=text, result=result, aspect_results=aspect_results)
    
    return render_template('analyze.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/contact')
# def contact():
    # developers = [
    #     {
    #         "name": "Developer 1",
    #         "role": "Machine Learning Engineer",
    #         "bio": "Experienced in NLP and sentiment analysis with a focus on customer feedback analysis.",
    #         "github": "https://github.com/developer1",
    #         "linkedin": "https://linkedin.com/in/developer1"
    #     },
    #     {
    #         "name": "Developer 2",
    #         "role": "Full Stack Developer",
    #         "bio": "Specializing in Flask-based web applications with a strong background in UI/UX design.",
    #         "github": "https://github.com/developer2",
    #         "linkedin": "https://linkedin.com/in/developer2"
    #     }
    # ]
    # return render_template('contact.html', developers=developers)
    # return render_template('contact.html')

# Firebase initialization


def initialize_firebase():
    # Get Firebase credentials from environment variables
    load_dotenv()
    firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS_JSON')
    firebase_db_url = os.environ.get('FIREBASE_DATABASE_URL')
    
    if not firebase_credentials:
        raise ValueError("Firebase credentials not found in environment variables")
    
    if not firebase_db_url:
        raise ValueError("Firebase database URL not found in environment variables")
    
    # Parse the JSON string from environment variable
    try:
        cred_dict = json.loads(firebase_credentials)
        cred = credentials.Certificate(cred_dict)
        
        # Initialize with database URL
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': firebase_db_url
            })
            
        # Return both Firestore and Realtime Database clients
        firestore_client = firestore.client()
        rtdb_client = db.reference()
        
        return firestore_client, rtdb_client
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in FIREBASE_CREDENTIALS environment variable")
    except Exception as e:
        raise ValueError(f"Error initializing Firebase: {str(e)}")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Initialize Firebase
            firestore_db, rtdb = initialize_firebase()
            
            # Store in Firestore (only if you want to use Firestore)
            try:
                contact_ref = firestore_db.collection('contacts').document()
                contact_ref.set({
                    'name': name,
                    'email': email,
                    'message': message,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
            except Exception as firestore_error:
                print(f"Firestore error: {str(firestore_error)}")
                # Continue with Realtime Database even if Firestore fails
            
            # Store in Realtime Database
            try:
                rtdb_contact_ref = rtdb.child('contact_messages').push()  # Updated to match your rules
                rtdb_contact_ref.set({
                    'name': name,
                    'email': email,
                    'message': message,
                    'timestamp': {'.sv': 'timestamp'}  # Server timestamp for Realtime DB
                })
                success = True
            except Exception as rtdb_error:
                print(f"Realtime Database error: {str(rtdb_error)}")
                if not success:  # Only raise if both databases failed
                    raise
            
            if success:
                flash('Your message has been sent successfully!', 'success')
            
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('contact.html', success=success)

@app.route('/result')
def result():
    # This route is for direct access to result page (redirect to analyze)
    return redirect(url_for('analyze'))

# Custom error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# @app.errorhandler(500)
# def server_error(e):
#     return render_template('500.html'), 500

# if __name__ == '__main__':
#     app.run(debug=True)
# @app.errorhandler(500)
# def server_error(e):
#     app.logger.error(f"Server error: {e}")
#     return "Internal server error", 500
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', error_message=str(e))

    # return render_template('500.html', error_message=str(e)), 500

# At the end of your app file
# if __name__ == "__main__":
#     app.run(debug=True)  # Enable debug mode to see detailed error messages
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)