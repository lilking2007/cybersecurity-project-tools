"""
Machine Learning Classification Engine

Trains and uses ML models for phishing URL detection.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import xgboost as xgb
import joblib
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class PhishingClassifier:
    """ML classifier for phishing URL detection."""
    
    def __init__(self, model_type: str = 'ensemble'):
        """
        Initialize phishing classifier.
        
        Args:
            model_type: Type of model ('logistic', 'random_forest', 'xgboost', 'ensemble')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
    
    def _create_model(self):
        """Create ML model based on model_type."""
        if self.model_type == 'logistic':
            return LogisticRegression(max_iter=1000, random_state=42)
        
        elif self.model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        
        elif self.model_type == 'xgboost':
            return xgb.XGBClassifier(
                n_estimators=100,
                max_depth=10,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
        
        elif self.model_type == 'ensemble':
            # Ensemble of multiple models
            lr = LogisticRegression(max_iter=1000, random_state=42)
            rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1
            )
            xgb_model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=10,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
            
            return VotingClassifier(
                estimators=[
                    ('lr', lr),
                    ('rf', rf),
                    ('xgb', xgb_model)
                ],
                voting='soft'
            )
        
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def prepare_features(self, features_dict: Dict) -> np.ndarray:
        """
        Prepare features for model input.
        
        Args:
            features_dict: Dictionary of extracted features
            
        Returns:
            Numpy array of feature values
        """
        # Convert feature dict to ordered array
        if not self.feature_names:
            # First time - establish feature order
            self.feature_names = sorted([
                k for k, v in features_dict.items()
                if isinstance(v, (int, float, bool))
            ])
        
        # Extract feature values in consistent order
        feature_values = []
        for fname in self.feature_names:
            value = features_dict.get(fname, 0)
            # Convert boolean to int
            if isinstance(value, bool):
                value = int(value)
            feature_values.append(value)
        
        return np.array(feature_values).reshape(1, -1)
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Train the classifier.
        
        Args:
            X: Feature dataframe
            y: Target labels (0 = benign, 1 = phishing)
            
        Returns:
            Dictionary of training metrics
        """
        # Store feature names
        self.feature_names = list(X.columns)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Create and train model
        self.model = self._create_model()
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        # Cross-validation score
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, cv=5, scoring='f1'
        )
        metrics['cv_f1_mean'] = cv_scores.mean()
        metrics['cv_f1_std'] = cv_scores.std()
        
        self.is_trained = True
        
        return metrics
    
    def predict(self, features_dict: Dict) -> Tuple[int, float]:
        """
        Predict if URL is phishing.
        
        Args:
            features_dict: Dictionary of extracted features
            
        Returns:
            Tuple of (prediction, confidence)
            prediction: 0 = benign, 1 = phishing
            confidence: probability score
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load a trained model.")
        
        # Prepare features
        X = self.prepare_features(features_dict)
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.model.predict(X_scaled)[0]
        confidence = self.model.predict_proba(X_scaled)[0][1]  # Probability of phishing
        
        return int(prediction), float(confidence)
    
    def get_feature_importance(self, top_n: int = 20) -> List[Tuple[str, float]]:
        """
        Get feature importance scores.
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            List of (feature_name, importance) tuples
        """
        if not self.is_trained:
            raise ValueError("Model not trained.")
        
        # Get feature importances based on model type
        if self.model_type == 'ensemble':
            # For ensemble, use the random forest estimator
            importances = self.model.named_estimators_['rf'].feature_importances_
        elif self.model_type == 'random_forest':
            importances = self.model.feature_importances_
        elif self.model_type == 'xgboost':
            importances = self.model.feature_importances_
        else:
            # Logistic regression - use coefficient magnitudes
            importances = np.abs(self.model.coef_[0])
        
        # Sort by importance
        feature_importance = list(zip(self.feature_names, importances))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        return feature_importance[:top_n]
    
    def save(self, filepath: str):
        """Save model to disk."""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model.")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'model_type': self.model_type
        }
        
        joblib.dump(model_data, filepath)
    
    def load(self, filepath: str):
        """Load model from disk."""
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.model_type = model_data['model_type']
        self.is_trained = True
    
    def get_risk_level(self, confidence: float) -> str:
        """
        Convert confidence score to risk level.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            Risk level string
        """
        if confidence >= 0.8:
            return "HIGH"
        elif confidence >= 0.5:
            return "MEDIUM"
        elif confidence >= 0.3:
            return "LOW"
        else:
            return "SAFE"
