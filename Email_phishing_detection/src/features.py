import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin

class TextSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.key]

class MetadataExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for text in X:
            row = {}
            # URL count
            row['url_count'] = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
            
            # Suspicious Keywords
            suspicious_keywords = ['verify', 'urgent', 'bank', 'account', 'security', 'suspended', 'lottery', 'winner', 'click']
            row['keyword_count'] = sum(1 for word in suspicious_keywords if word in text.lower())
            
            # Length
            row['length'] = len(text)
            
            features.append(list(row.values()))
            
        return features

def get_feature_pipeline():
    return FeatureUnion([
        ('text', TfidfVectorizer(stop_words='english', max_features=1000)),
        # We can integrate metadata here if needed, but for simplicity 
        # and compatibility with TfidfVectorizer in a FeatureUnion directly
        # might require a more complex custom structure if we want to mix dense and sparse.
        # For this prototype, let's keep it simple: 
        # We will use TfidfVectorizer as the main feature set for the pipeline.
        # Metadata will be handled separately if we decide to create a more complex ensemble, 
        # but for sklearn `Pipeline`, sticking to one main content path is often easier for a start.
        # However, to be robust, let's just return the TF-IDF vectorizer for the text part.
        # We will keep MetadataExtractor for future improvements or manual analysis.
    ])

# Simplified approach for the first iteration: Just use Tfidf
# Metadata features can be added by concatenating sparse matrices, 
# but let's stick to text content for the baseline model to ensure it runs smoothly without shape mismatches.
# We will incorporate metadata if the text-only model is insufficient.
