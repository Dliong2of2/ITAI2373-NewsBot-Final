"""
Unit tests for the text preprocessing module.
"""

import unittest

from src.data_processing.text_preprocessor import TextPreprocessor


class TestTextPreprocessor(unittest.TestCase):
    """Tests for the TextPreprocessor."""

    def setUp(self):
        self.preprocessor = TextPreprocessor()

    def test_clean_text(self):
        """Text should be converted to lowercase and trimmed."""

        text = "  Hello WORLD!  "

        cleaned = self.preprocessor.clean_text(text)

        self.assertEqual(cleaned, "hello world!")

    def test_tokenize(self):
        """Tokenization should return alphabetic tokens."""

        text = "Artificial Intelligence is amazing."

        tokens = self.preprocessor.tokenize(text)

        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)

    def test_remove_stopwords(self):
        """Common stop words should be removed."""

        tokens = [
            "this",
            "is",
            "artificial",
            "intelligence",
        ]

        filtered = self.preprocessor.remove_stopwords(tokens)

        self.assertIn("artificial", filtered)
        self.assertIn("intelligence", filtered)

    def test_lemmatize(self):
        """Words should be lemmatized."""

        tokens = [
            "running",
            "cars",
        ]

        lemmas = self.preprocessor.lemmatize(tokens)

        self.assertIsInstance(lemmas, list)

    def test_preprocess_pipeline(self):
        """The full preprocessing pipeline should return a token list."""

        text = (
            "Artificial Intelligence is transforming healthcare."
        )

        tokens = self.preprocessor.preprocess(text)

        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)


if __name__ == "__main__":
    unittest.main()
