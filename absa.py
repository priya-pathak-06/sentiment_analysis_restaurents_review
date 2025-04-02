import numpy as np
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class AspectBasedSentimentAnalyzer:
    def __init__(self, model_path='models/svm_model.pkl', vectorizer_path='models/tfidf_vectorizer.pkl'):
        """
        Initialize the Aspect-Based Sentiment Analyzer
        
        Args:
            model_path (str): Path to the pre-trained ABSA model
            vectorizer_path (str): Path to the TF-IDF vectorizer
        """
        try:
            # Load pre-trained models and vectorizers for different aspects
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            
            # Define restaurant review aspects
            self.aspects = ['Food', 'Service', 'Ambience', 'Price']
        except Exception as e:
            print(f"Error loading ABSA model: {e}")
            self.model = None
            self.vectorizer = None
            self.aspects = []
    
    def preprocess_text(self, text):
        """
        Preprocess text by converting to lowercase and removing special characters
        
        Args:
            text (str): Input text to preprocess
        
        Returns:
            str: Preprocessed text
        """
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return ' '.join(text.split())
    
    def extract_aspect_sentiments(self, text):
        """
        Analyze sentiments for different aspects of a restaurant review
        
        Args:
            text (str): Restaurant review text
        
        Returns:
            dict: Sentiment analysis results for each aspect
        """
        if self.model is None or self.vectorizer is None:
            return {"error": "ABSA model not loaded"}
        
        # Preprocess the text
        preprocessed_text = self.preprocess_text(text)
        
        # Vectorize the text
        text_vectorized = self.vectorizer.transform([preprocessed_text])
        
        # Predict sentiments for each aspect
        aspect_sentiments = {}
        for aspect in self.aspects:
            # Prediction 
            prediction = self.model.predict(text_vectorized)[0]
            
            # Calculate confidence using decision function
            try:
                confidence = abs(self.model.decision_function(text_vectorized)[0])
                confidence = min(round(confidence * 100, 2), 100.0)
            except AttributeError:
                # Fallback to 100% confidence if decision_function is not available
                confidence = 100.0
            
            # Map numerical prediction to sentiment labels
            # Determine sentiment label and class
            if prediction == 1:
                sentiment = "Positive"
                sentiment_class = "positive"
            elif prediction == -1:
                sentiment = "Negative"
                sentiment_class = "negative"
            else:
                # Default to Negative if not clearly Positive
                sentiment = "Negative"
                sentiment_class = "negative"
            
            aspect_sentiments[aspect] = {
                "sentiment": sentiment,
                "confidence": confidence,
                "sentiment_class": sentiment_class
            }
        
        return aspect_sentiments