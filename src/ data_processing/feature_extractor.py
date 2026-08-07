"""
Feature extraction utilities for NewsBot 2.0.
"""

from sklearn.feature_extraction.text import TfidfVectorizer


class FeatureExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words="english",
            ngram_range=(1, 2)
        )

    def fit_transform(self, documents):
        return self.vectorizer.fit_transform(documents)

    def transform(self, documents):
        return self.vectorizer.transform(documents)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out()
