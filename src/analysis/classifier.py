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

        # 1. Feature Extractor
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
            stop_words="english",
            sublinear_tf=True,
        )

        # 2. Base Classifier with Class Weighting (Handles Imbalance)
        # Using SGDClassifier (Linear SVM/LogReg) for scalable training on 200k+ rows
        base_model = SGDClassifier(
            loss="log_loss",
            penalty="l2",
            alpha=1e-5,
            class_weight="balanced",  # Critical for imbalanced news categories
            random_state=42,
            max_iter=1000,
        )

        # 3. Probability Calibration (Ensures confidence scores are true probabilities)
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
        text = re.sub(r"https?://\S+|www\.\S+", "", text)  # Remove URLs
        text = re.sub(
            r"[^a-zA-Z\s]", "", text
        )  # Remove non-alphanumeric characters
        return re.sub(r"\s+", " ", text).strip()

    def train(
        self,
        X_train: List[str],
        y_train: List[str],
    ) -> Dict[str, Any]:
        """Trains the vectorizer and probability-calibrated ensemble model."""
        print("⚙️ Preprocessing training data...")
        cleaned_X = [self._preprocess_text(text) for text in X_train]

        print("📐 Vectorizing text features...")
        X_vec = self.vectorizer.fit_transform(cleaned_X)

        print("🏋️ Training Calibrated SGD Model (Class Weight: Balanced)...")
        self.model.fit(X_vec, y_train)

        self.classes_ = self.model.classes_
        self.is_trained = True

        print("✅ Training complete!")

        return {
            "status": "trained",
            "num_classes": len(self.classes_),
        }
            def predict_with_confidence(
        self,
        texts: List[str],
    ) -> List[Dict[str, Any]]:
        """Predicts news categories with calibrated confidence scores and
        alternative category suggestions."""

        if not self.is_trained:
            raise RuntimeError(
                "Classifier has not been trained. Call train() first."
            )

        # Preprocess incoming texts
        cleaned = [self._preprocess_text(text) for text in texts]
        X_vec = self.vectorizer.transform(cleaned)

        # Predict probabilities
        probabilities = self.model.predict_proba(X_vec)
        predictions = self.model.predict(X_vec)

        results = []

        for i in range(len(texts)):
            probs = probabilities[i]

            # Sort probabilities from highest to lowest
            ranked = np.argsort(probs)[::-1]

            prediction = predictions[i]
            confidence = float(probs[ranked[0]])

            alternatives = []
            for idx in ranked[1 : self.top_k_alternatives + 1]:
                alternatives.append(
                    {
                        "category": self.classes_[idx],
                        "confidence": round(float(probs[idx]), 4),
                    }
                )

            results.append(
                {
                    "prediction": prediction,
                    "confidence": round(confidence, 4),
                    "alternatives": alternatives,
                }
            )

        return results
            def explain_prediction(
        self, article_text: str, top_n_words: int = 5
    ) -> Dict[str, Any]:
        """Provides feature-importance explanations based on TF-IDF term weights."""
        if not self.is_trained:
            raise RuntimeError("Model must be trained to explain predictions.")

        cleaned = self._preprocess_text(article_text)
        vec = self.vectorizer.transform([cleaned])

        # Extract non-zero TF-IDF terms from the text
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        non_zero_indices = vec.nonzero()[1]
        scores = vec.data

        # Pair words with their TF-IDF scores and sort
        word_score_pairs = list(
            zip(feature_names[non_zero_indices], scores)
        )
        sorted_pairs = sorted(
            word_score_pairs, key=lambda x: x[1], reverse=True
        )

        top_influential_terms = [
            {"term": term, "tfidf_weight": round(float(score), 4)}
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
                f"{', '.join([item['term'] for item in top_influential_terms])}."
            ),
        }
