"""
Language detection module for NewsBot Intelligence System 2.0.

The completed notebook does not implement a standalone LanguageDetector
class. Language detection is handled as part of the multilingual
processing workflow.

This module is included to match the required repository structure.
"""

from langdetect import detect, DetectorFactory

# Make language detection reproducible
DetectorFactory.seed = 42


class LanguageDetector:
    """Detect the language of text."""

    def detect_language(self, text: str) -> str:
        """
        Detect the language of a text string.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        str
            ISO language code (e.g., 'en', 'es', 'fr').
        """
        if not isinstance(text, str) or not text.strip():
            return "unknown"

        try:
            return detect(text)
        except Exception:
            return "unknown"

    def is_english(self, text: str) -> bool:
        """
        Check whether the text is English.
        """
        return self.detect_language(text) == "en"
