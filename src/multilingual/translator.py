"""
Translation module for NewsBot Intelligence System 2.0.

The completed notebook does not implement a standalone Translator
class. Translation functionality is demonstrated within the
multilingual workflow.

This module is included to match the required repository structure.
"""

from deep_translator import GoogleTranslator


class Translator:
    """Translate text between languages."""

    def translate(
        self,
        text: str,
        source_language: str = "auto",
        target_language: str = "en",
    ) -> str:
        """
        Translate text using GoogleTranslator.

        Parameters
        ----------
        text : str
            Input text.
        source_language : str
            Source language code (default: auto).
        target_language : str
            Target language code (default: en).

        Returns
        -------
        str
            Translated text.
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        try:
            return GoogleTranslator(
                source=source_language,
                target=target_language,
            ).translate(text)
        except Exception:
            # If translation fails, return the original text.
            return text
