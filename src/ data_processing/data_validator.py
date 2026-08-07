"""
Data validation utilities for NewsBot Intelligence System 2.0.

The current notebook performs data validation within the individual
processing modules before training and inference rather than through
a standalone DataValidator class.

This module is included to match the required repository structure.
"""


class DataValidator:
    """Basic data validation helper."""

    @staticmethod
    def validate_text(text):
        """Return True if the input is a non-empty string."""
        return isinstance(text, str) and len(text.strip()) > 0

    @staticmethod
    def validate_dataset(df, required_columns=None):
        """Check that a DataFrame contains the required columns."""
        if required_columns is None:
            return True

        return all(column in df.columns for column in required_columns)
