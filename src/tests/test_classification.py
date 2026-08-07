"""
Unit tests for the news classification module.
"""

import unittest

from src.analysis.classifier import NewsClassifier


class TestNewsClassifier(unittest.TestCase):
    """Tests for the NewsClassifier."""

    def setUp(self):
        self.classifier = NewsClassifier()

        self.train_texts = [
            "The stock market closed higher today.",
            "The football team won the championship.",
            "Scientists developed a new AI model.",
        ]

        self.train_labels = [
            "Business",
            "Sports",
            "Technology",
        ]

        self.classifier.train(
            self.train_texts,
            self.train_labels,
        )

    def test_training(self):
        """Model should train without errors."""
        self.assertIsNotNone(self.classifier.model)

    def test_prediction(self):
        """Model should predict one label."""
        prediction = self.classifier.predict(
            ["Artificial intelligence is transforming healthcare."]
        )

        self.assertEqual(len(prediction), 1)

    def test_prediction_probabilities(self):
        """Probability scores should be returned."""
        probabilities = self.classifier.predict_proba(
            ["Technology companies announced new products."]
        )

        self.assertEqual(len(probabilities), 1)

    def test_evaluation(self):
        """Evaluation should return a score."""
        score = self.classifier.evaluate(
            self.train_texts,
            self.train_labels,
        )

        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
