import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
try:
    from src.utils import load_data
except ImportError:
    from utils import load_data

MODEL_PATH = 'models/phishing_model.pkl'

def train_model():
    """
    Trains the phishing detection model and saves it.
    """
    print("Loading data...")
    df = load_data()
    
    X = df['body']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training model...")
    # Create a pipeline that first vectorizes the text, then applies the classifier
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=3000)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    print(f"Saving model to {MODEL_PATH}")
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline, accuracy

def load_model():
    """
    Loads the trained model from disk.
    """
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("Model not found. Training new model...")
        model, _ = train_model()
        return model

def predict_email(model, email_text):
    """
    Predicts whether an email is phishing or safe.
    Returns: prediction (0 or 1), probability
    """
    prediction = model.predict([email_text])[0]
    probability = model.predict_proba([email_text])[0][1] # Probability of class 1 (Phishing)
    return prediction, probability

if __name__ == "__main__":
    train_model()
