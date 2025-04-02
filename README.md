# Real-Time Sentiment Analysis with Flask-Based UI

A full-stack web application for real-time sentiment analysis of text using a pre-trained SVM model and TF-IDF vectorizer.

## Project Overview

This application allows users to:
- Enter text content (reviews, comments, feedback)
- Receive real-time sentiment analysis results (positive, negative, or neutral)
- View confidence scores for the analysis

## Features

- Flask-based backend
- Responsive Bootstrap frontend
- Machine Learning powered sentiment analysis
- Pre-trained SVM model and TF-IDF vectorizer
- Real-time analysis with confidence scores

## Project Structure

```
sentiment-analysis-app/
│
├── app.py                      # Main Flask application file
├── requirements.txt            # Dependencies list
├── README.md                   # Project documentation
│
├── models/                     # Folder for ML models
│   ├── svm_model.pkl           # Pre-trained SVM model
│   └── tfidf_vectorizer.pkl    # Pre-trained TF-IDF vectorizer
│
├── static/                     # Static files
│   ├── css/
│   │   └── styles.css          # Custom CSS
│   ├── js/
│   │   └── main.js             # Custom JavaScript
│   └── images/                 # Image assets
│
├── templates/                  # HTML templates
│   ├── layout.html             # Base template with navigation
│   ├── index.html              # Landing page
│   ├── analyze.html            # Sentiment analysis input form
│   ├── result.html             # Analysis results page
│   ├── about.html              # About the project page
│   └── contact.html            # Contact and developer info page
│
└── notebooks/                  # Reference notebooks
    └── resturents.ipynb        # Original notebook with model training
```

## Installation and Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/sentiment-analysis-app.git
cd sentiment-analysis-app
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Ensure model files are in the correct location
- Place `svm_model.pkl` in the `/models` directory
- Place `tfidf_vectorizer.pkl` in the `/models` directory

5. Run the application
```bash
python app.py
```

6. Open your browser and navigate to `http://127.0.0.1:5000/`

## Model Information

The sentiment analysis is powered by:
- **Algorithm**: Support Vector Machine (SVM)
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Training**: The model was trained on restaurant review data
- **Prediction**: Classifies text as positive, negative, or neutral with confidence scores

## Technologies Used

- **Backend**: Flask, Python, scikit-learn, joblib
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **ML**: SVM, TF-IDF vectorization
- **Development**: Git, Virtual Environment


## License

This project is licensed under the MIT License - see the LICENSE file for details.
