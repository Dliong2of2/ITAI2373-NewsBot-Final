"""
Text preprocessing utilities for NewsBot Intelligence System 2.0.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required resources if missing
try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    STOP_WORDS = set(stopwords.words("english"))

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet", quiet=True)

lemmatizer = WordNetLemmatizer()


class TextPreprocessor:
    """Preprocess raw news text for NLP analysis."""

    def clean_text(self, text: str) -> str:
        """Lowercase text and remove extra whitespace."""
        if not isinstance(text, str):
            return ""

        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def tokenize(self, text: str):
        """Extract alphabetic tokens."""
        return re.findall(r"\b[a-z]{3,}\b", text.lower())

    def remove_stopwords(self, tokens):
        """Remove common English stop words."""
        return [word for word in tokens if word not in STOP_WORDS]

    def lemmatize(self, tokens):
        """Lemmatize tokens."""
        return [lemmatizer.lemmatize(word) for word in tokens]

    def preprocess(self, text: str):
        """Complete preprocessing pipeline."""
        text = self.clean_text(text)
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.lemmatize(tokens)
        return tokens
