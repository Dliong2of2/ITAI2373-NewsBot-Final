"""
Integration tests for NewsBot Intelligence System 2.0.
"""

import unittest

from src.analysis.classifier import NewsClassifier
from src.data_processing.text_preprocessor import TextPreprocessor
from src.language_models.summarizer import IntelligentSummarizer


class TestNewsBotIntegration(unittest.TestCase):
    """Integration tests for the NewsBot pipeline."""

    def setUp(self):
        self.preprocessor = TextPreprocessor()
        self.classifier = NewsClassifier()
        self.summarizer = IntelligentSummarizer()

        train_texts = [
            "The stock market closed higher today.",
            "The football team won the championship.",
            "Scientists developed a new AI model.",
        ]

        train_labels = [
            "Business",
            "Sports",
            "Technology",
        ]

        self.classifier.train(
            train_texts,
            train_labels,
        )

    def test_preprocess_and_classify(self):
        """Verify preprocessing and classification work together."""

        article = (
            "Artificial intelligence is transforming healthcare."
        )

        processed = self.preprocessor.preprocess(article)

        prediction = self.classifier.predict(
            [" ".join(processed)]
        )

        self.assertEqual(len(prediction), 1)

    def test_summarization_pipeline(self):
        """Verify summarization returns expected information."""

        article = (
            "Artificial intelligence is rapidly changing healthcare. "
            "Hospitals are using machine learning to improve patient "
            "care and diagnosis."
        )

        result = self.summarizer.summarize_article(article)

        self.assertIn("summary", result)
        self.assertIn("method", result)

    def test_complete_pipeline(self):
        """Run a simple end-to-end workflow."""

        article = (
            "Scientists announced a breakthrough in renewable energy."
        )

        processed = self.preprocessor.preprocess(article)

        prediction = self.classifier.predict(
            [" ".join(processed)]
        )

        summary = self.summarizer.summarize_article(article)

        self.assertEqual(len(prediction), 1)
        self.assertIsInstance(summary, dict)


if __name__ == "__main__":
    unittest.main()
