"""
News classification module for NewsBot Intelligence System 2.0.
"""

import re
from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier


class AdvancedNewsClassifier:
    """Enhanced news classification with calibrated confidence scoring,
    multi-category output, and TF-IDF feature importance explanations.
    """

    def __init__(
        self,
        max_features: int = 15000,
        ngram_range: Tuple[int, int] = (1, 2),
        top_k_alternatives: int = 3,
    ):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.top_k_alternatives = top_k_alternatives

        # Feature Extractor
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
            stop_words="english",
            sublinear_tf=True,
        )

        # Base classifier
        base_model = SGDClassifier(
            loss="log_loss",
            penalty="l2",
            alpha=1e-5,
            class_weight="balanced",
            random_state=42,
            max_iter=1000,
        )

        # Probability calibration
        self.model = CalibratedClassifierCV(
            estimator=base_model,
            cv=2,
        )

        self.is_trained = False
        self.classes_ = None

    def _preprocess_text(self, text: str) -> str:
        """Standardized text cleaning routine."""
        if not isinstance(text, str):
            return ""

        text = text.lower()
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def train(self, X_train: List[str], y_train: List[str]) -> Dict[str, Any]:
        """Train the vectorizer and probability-calibrated classifier."""
        print("⚙️ Preprocessing training data...")
        cleaned_X = [self._preprocess_text(text) for text in X_train]

        print("📐 Vectorizing text features...")
        X_vec = self.vectorizer.fit_transform(cleaned_X)

        print("🏋️ Training Calibrated SGD Model...")
        self.model.fit(X_vec, y_train)

        self.classes_ = self.model.classes_
        self.is_trained = True

        print("✅ Training complete!")

        return {
            "status": "trained",
            "num_classes": len(self.classes_),
        }

    def predict_with_confidence(self, article_text: str) -> Dict[str, Any]:
        """Predict the primary category and confidence score."""
        if not self.is_trained:
            raise RuntimeError(
                "Model has not been trained yet. Call `.train()` first."
            )

        cleaned = self._preprocess_text(article_text)
        vec = self.vectorizer.transform([cleaned])

        probs = self.model.predict_proba(vec)[0]
        top_indices = np.argsort(probs)[::-1]

        primary_idx = top_indices[0]
        primary_category = self.classes_[primary_idx]
        primary_confidence = float(probs[primary_idx])

        alternatives = []

        for idx in top_indices[1:self.top_k_alternatives + 1]:
            alternatives.append(
                {
                    "category": str(self.classes_[idx]),
                    "confidence": float(round(probs[idx], 4)),
                }
            )

        return {
            "primary_category": primary_category,
            "confidence": round(primary_confidence, 4),
            "alternative_categories": alternatives,
        }

    def explain_prediction(
        self,
        article_text: str,
        top_n_words: int = 5,
    ) -> Dict[str, Any]:
        """Provide TF-IDF feature importance explanation."""
        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained to explain predictions."
            )

        cleaned = self._preprocess_text(article_text)
        vec = self.vectorizer.transform([cleaned])

        feature_names = np.array(
            self.vectorizer.get_feature_names_out()
        )

        non_zero_indices = vec.nonzero()[1]
        scores = vec.data

        word_score_pairs = list(
            zip(feature_names[non_zero_indices], scores)
        )

        sorted_pairs = sorted(
            word_score_pairs,
            key=lambda x: x[1],
            reverse=True,
        )

        top_influential_terms = [
            {
                "term": term,
                "tfidf_weight": round(float(score), 4),
            }
            for term, score in sorted_pairs[:top_n_words]
        ]

        prediction_info = self.predict_with_confidence(article_text)

        return {
            "primary_category": prediction_info["primary_category"],
            "confidence": prediction_info["confidence"],
            "key_influential_terms": top_influential_terms,
            "explanation": (
                f"The article was classified as "
                f"'{prediction_info['primary_category']}' "
                f"due to the presence and high importance of key phrases: "
                f"{', '.join(item['term'] for item in top_influential_terms)}."
            ),
        }
