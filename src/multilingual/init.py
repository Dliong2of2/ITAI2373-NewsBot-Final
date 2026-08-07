"""
Multilingual processing package for NewsBot Intelligence System 2.0.
"""

from .language_detector import LanguageDetector
from .translator import Translator
from .cross_lingual_analyzer import CrossLingualAnalyzer

__all__ = [
    "LanguageDetector",
    "Translator",
    "CrossLingualAnalyzer",
]
