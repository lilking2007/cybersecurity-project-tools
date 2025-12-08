"""
Model Training Script

Train the phishing detection model on labeled dataset.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models.classifier import PhishingClassifier
from preprocessing.url_parser import URLPreprocessor
from features.lexical_features import FeatureExtractor
from utils.config_loader import get_config


def load_sample_data():
    """Create sample training data for demonstration."""
    # In production, load from PhishTank, OpenPhish, etc.
    
    # Sample phishing URLs
    phishing_urls = [
        'http://paypal-verify-account.tk/login.php',
        'http://192.168.1.1/amazon/signin',
        'http://secure-banking-update.xyz/verify',
        'http://microsoft-account-locked.ml/unlock',
        'http://apple-id-suspended.cf/restore',
        'http://facebook-security-check.gq/verify',
        'http://netflix-payment-failed.tk/update',
        'http://instagram-verify-badge.ml/confirm',
    ]
    
    # Sample benign URLs
    benign_urls = [
        'https://www.google.com',
        'https://www.github.com',
        'https://www.stackoverflow.com',
        'https://www.wikipedia.org',
        'https://www.amazon.com',
        'https://www.microsoft.com',
        'https://www.apple.com',
        'https://www.facebook.com',
    ]
    
    # Create dataframe
    urls = phishing_urls + benign_urls
    labels = [1] * len(phishing_urls) + [0] * len(benign_urls)
    
    return pd.DataFrame({'url': urls, 'label': labels})


def extract_features_from_urls(urls):
    """Extract features from list of URLs."""
    preprocessor = URLPreprocessor()
    extractor = FeatureExtractor()
    
    all_features = []
    
    for url in urls:
        try:
            # Parse URL
            parsed = preprocessor.parse(url)
            
            # Extract features
            features = extractor.extract_all(url, parsed)
            
            # Convert to numeric only
            numeric_features = {
                k: v for k, v in features.items()
                if isinstance(v, (int, float, bool))
            }
            
            # Convert booleans to int
            numeric_features = {
                k: int(v) if isinstance(v, bool) else v
                for k, v in numeric_features.items()
            }
            
            all_features.append(numeric_features)
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
            all_features.append({})
    
    return pd.DataFrame(all_features)


def train_model(data_path=None, model_output_path=None):
    """
    Train the phishing detection model.
    
    Args:
        data_path: Path to training data CSV (optional)
        model_output_path: Path to save trained model
    """
    print("=" * 60)
    print("Phishing URL Detector - Model Training")
    print("=" * 60)
    
    # Load configuration
    config = get_config()
    
    # Load data
    if data_path and Path(data_path).exists():
        print(f"\nLoading data from: {data_path}")
        df = pd.read_csv(data_path)
    else:
        print("\nNo data file provided. Using sample data for demonstration.")
        print("[WARNING] For production, provide a labeled dataset with 'url' and 'label' columns.")
        df = load_sample_data()
    
    print(f"Loaded {len(df)} URLs")
    print(f"  - Phishing: {sum(df['label'] == 1)}")
    print(f"  - Benign: {sum(df['label'] == 0)}")
    
    # Extract features
    print("\nExtracting features...")
    X = extract_features_from_urls(df['url'].tolist())
    y = df['label']
    
    print(f"Extracted {len(X.columns)} features")
    
    # Handle missing values
    X = X.fillna(0)
    
    # Initialize classifier
    model_type = config.get('model.type', 'ensemble')
    print(f"\nInitializing {model_type} classifier...")
    classifier = PhishingClassifier(model_type=model_type)
    
    # Train model
    print("\nTraining model...")
    metrics = classifier.train(X, y)
    
    # Display results
    print("\n" + "=" * 60)
    print("Training Results")
    print("=" * 60)
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1_score']:.4f}")
    print(f"ROC AUC:   {metrics['roc_auc']:.4f}")
    print(f"\nCross-validation F1: {metrics['cv_f1_mean']:.4f} (+/- {metrics['cv_f1_std']:.4f})")
    
    # Feature importance
    print("\n" + "=" * 60)
    print("Top 10 Most Important Features")
    print("=" * 60)
    
    try:
        feature_importance = classifier.get_feature_importance(top_n=10)
        for i, (feature, importance) in enumerate(feature_importance, 1):
            print(f"{i:2d}. {feature:40s} {importance:.4f}")
    except:
        print("Feature importance not available for this model type.")
    
    # Save model
    if model_output_path is None:
        model_output_path = config.get('model.path', 'data/models/phishing_model.pkl')
    
    # Create directory if needed
    Path(model_output_path).parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\nSaving model to: {model_output_path}")
    classifier.save(model_output_path)
    
    print("\n[SUCCESS] Training complete!")
    print("=" * 60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train phishing detection model')
    parser.add_argument(
        '--data',
        type=str,
        help='Path to training data CSV file with "url" and "label" columns'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Path to save trained model'
    )
    
    args = parser.parse_args()
    
    train_model(data_path=args.data, model_output_path=args.output)
