"""
Text preprocessing module for NewsBot Intelligence System 2.0.
"""

import re


class DataProcessor:
    """Preprocesses text for classical NLP, transformer models, and topic modeling."""

    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = text.lower()
        return re.sub(r"\s+", " ", text).strip()
