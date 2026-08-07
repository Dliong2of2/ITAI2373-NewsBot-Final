"""
Text summarization module for NewsBot Intelligence System 2.0.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class IntelligentSummarizer:
    """Advanced Text Summarization Engine providing hybrid
    extractive/abstractive pipelines, multi-document synthesis,
    headline generation, and quality evaluation metrics.
    """

    def __init__(
        self,
        use_abstractive: bool = False,
        hf_model_name: str = "facebook/bart-large-cnn",
    ):
        self.use_abstractive = use_abstractive
        self.abstractive_pipeline = None

        # Optionally load HuggingFace summarization pipeline
        if self.use_abstractive:
            try:
                from transformers import pipeline

                print(
                    f"⚙️ Loading abstractive HuggingFace transformer pipeline: {hf_model_name}..."
                )

                self.abstractive_pipeline = pipeline(
                    "summarization",
                    model=hf_model_name,
                )

            except Exception as e:
                print(
                    f"⚠️ Could not load abstractive model ({e}). "
                    "Defaulting to TF-IDF extractive summarization."
                )
                self.use_abstractive = False

    def _split_sentences(
        self,
        text: str,
    ) -> List[str]:
        """Split raw text into individual sentences."""

        if not isinstance(text, str) or not text.strip():
            return []

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text.strip(),
        )

        return [
            sentence.strip()
            for sentence in sentences
            if len(sentence.strip()) > 10
        ]

    def _extractive_summarize(
        self,
        article_text: str,
        top_n: int = 3,
    ) -> str:
        """Generate an extractive TF-IDF summary."""

        sentences = self._split_sentences(article_text)

        if not sentences:
            return ""

        if len(sentences) <= top_n:
            return " ".join(sentences)

        vectorizer = TfidfVectorizer(stop_words="english")

        try:
            tfidf_matrix = vectorizer.fit_transform(sentences)
        except ValueError:
            return " ".join(sentences[:top_n])

        sentence_scores = np.asarray(
            tfidf_matrix.sum(axis=1)
        ).flatten()

        # Positional weighting
        sentence_scores[0] *= 1.2

        if len(sentence_scores) > 1:
            sentence_scores[-1] *= 1.1

        top_indices = np.argsort(
            sentence_scores
        )[::-1][:top_n]

        top_indices = sorted(top_indices)

        summary_sentences = [
            sentences[idx]
            for idx in top_indices
        ]

        return " ".join(summary_sentences)
          def summarize_article(
        self,
        article_text: str,
        max_length: int = 130,
        min_length: int = 30,
        top_n: int = 3,
    ) -> Dict[str, Any]:
        """Generate a summary for a single news article."""

        if (
            self.use_abstractive
            and self.abstractive_pipeline is not None
        ):
            try:
                summary = self.abstractive_pipeline(
                    article_text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                )[0]["summary_text"]

                method = "abstractive"

            except Exception:
                summary = self._extractive_summarize(
                    article_text,
                    top_n=top_n,
                )
                method = "extractive"

        else:
            summary = self._extractive_summarize(
                article_text,
                top_n=top_n,
            )
            method = "extractive"

        return {
            "summary": summary,
            "method": method,
            "original_length": len(article_text.split()),
            "summary_length": len(summary.split()),
            "compression_ratio": round(
                len(summary.split())
                / max(len(article_text.split()), 1),
                3,
            ),
        }

    def summarize_dataset(
        self,
        articles: List[str],
        top_n: int = 3,
    ) -> List[Dict[str, Any]]:
        """Summarize multiple news articles."""

        summaries = []

        for article in articles:
            summaries.append(
                self.summarize_article(
                    article,
                    top_n=top_n,
                )
            )

        return summaries
          def generate_headline(
        self,
        article_text: str,
        max_words: int = 10,
    ) -> str:
        """Generate a simple headline from an article."""

        summary = self._extractive_summarize(
            article_text,
            top_n=1,
        )

        words = summary.split()

        if len(words) > max_words:
            return " ".join(words[:max_words]) + "..."

        return summary

    def evaluate_summary(
        self,
        original_text: str,
        summary: str,
    ) -> Dict[str, float]:
        """Compute basic summary quality metrics."""

        original_words = len(original_text.split())
        summary_words = len(summary.split())

        compression_ratio = (
            summary_words / max(original_words, 1)
        )

        sentence_count = len(
            self._split_sentences(summary)
        )

        return {
            "original_words": original_words,
            "summary_words": summary_words,
            "compression_ratio": round(
                compression_ratio,
                3,
            ),
            "summary_sentences": sentence_count,
        }
