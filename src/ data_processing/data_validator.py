"""
Data validation utilities for NewsBot 2.0.
"""

from typing import List


def validate_text(text):
    """Validate a single text input."""

    if text is None:
        raise ValueError("Input text cannot be None.")

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if not text.strip():
        raise ValueError("Input text cannot be empty.")

    return True


def validate_documents(documents: List[str]):
    """Validate a collection of documents."""

    if not isinstance(documents, list):
        raise TypeError("Documents must be provided as a list.")

    if len(documents) == 0:
        raise ValueError("Document list cannot be empty.")

    for doc in documents:
        validate_text(doc)

    return True
