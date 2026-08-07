"""
Conversational interface for NewsBot Intelligence System 2.0.
"""

from typing import Any, Dict, List

import pandas as pd


class ConversationalInterface:
    """Natural language interface for interacting with the NewsBot
    Intelligence System."""

    def __init__(
        self,
        classifier=None,
        summarizer=None,
        topic_modeler=None,
        sentiment_tracker=None,
        entity_mapper=None,
        semantic_search=None,
        multilingual_processor=None,
    ):
        self.classifier = classifier
        self.summarizer = summarizer
        self.topic_modeler = topic_modeler
        self.sentiment_tracker = sentiment_tracker
        self.entity_mapper = entity_mapper
        self.semantic_search = semantic_search
        self.multilingual_processor = multilingual_processor

    def process_query(
        self,
        query: str,
        articles: pd.DataFrame = None,
    ) -> Dict[str, Any]:
        """Route a natural-language query to the appropriate NewsBot module."""

        query_lower = query.lower()

        # Summary requests
        if any(
            keyword in query_lower
            for keyword in [
                "summarize",
                "summary",
                "brief",
            ]
        ):
            return self._handle_summary_request(
                query,
                articles,
            )

        # Sentiment requests
        if any(
            keyword in query_lower
            for keyword in [
                "sentiment",
                "positive",
                "negative",
                "emotion",
            ]
        ):
            return self._handle_sentiment_request(
                query,
                articles,
            )

        # Topic requests
        if any(
            keyword in query_lower
            for keyword in [
                "topic",
                "trend",
                "theme",
            ]
        ):
            return self._handle_topic_request(
                query,
                articles,
            )

        # Entity requests
        if any(
            keyword in query_lower
            for keyword in [
                "person",
                "organization",
                "company",
                "entity",
            ]
        ):
            return self._handle_entity_request(
                query,
                articles,
            )

        # Search requests
        if any(
            keyword in query_lower
            for keyword in [
                "search",
                "find",
                "similar",
            ]
        ):
            return self._handle_search_request(
                query,
                articles,
            )

        return self._handle_general_request(
            query,
            articles,
        )
          def _handle_summary_request(
        self,
        query: str,
        articles: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Handle article summarization requests."""

        if self.summarizer is None:
            return {
                "status": "error",
                "message": "Summarization module is unavailable.",
            }

        if articles is None or articles.empty:
            return {
                "status": "error",
                "message": "No articles available for summarization.",
            }

        article_text = str(articles.iloc[0]["short_description"])

        summary = self.summarizer.summarize(article_text)

        return {
            "status": "success",
            "intent": "summary",
            "summary": summary,
        }

    def _handle_sentiment_request(
        self,
        query: str,
        articles: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Handle sentiment-related questions."""

        if self.sentiment_tracker is None:
            return {
                "status": "error",
                "message": "Sentiment analysis module is unavailable.",
            }

        if articles is None or articles.empty:
            return {
                "status": "error",
                "message": "No articles available for sentiment analysis.",
            }

        sentiment_results = self.sentiment_tracker.analyze_dataset(
            articles
        )

        return {
            "status": "success",
            "intent": "sentiment",
            "results": sentiment_results,
        }

    def _handle_topic_request(
        self,
        query: str,
        articles: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Handle topic modeling requests."""

        if self.topic_modeler is None:
            return {
                "status": "error",
                "message": "Topic modeling module is unavailable.",
            }

        if articles is None or articles.empty:
            return {
                "status": "error",
                "message": "No articles available for topic analysis.",
            }

        topics = self.topic_modeler.track_topic_trends(articles)

        return {
            "status": "success",
            "intent": "topics",
            "results": topics,
        }
          def _handle_entity_request(
        self,
        query: str,
        articles: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Handle named entity recognition requests."""

        if self.entity_mapper is None:
            return {
                "status": "error",
                "message": "Entity relationship module is unavailable.",
            }

        if articles is None or articles.empty:
            return {
                "status": "error",
                "message": "No articles available for entity analysis.",
            }

        article_text = str(articles.iloc[0]["short_description"])

        entities = self.entity_mapper.extract_entities(article_text)

        return {
            "status": "success",
            "intent": "entities",
            "results": entities,
        }

    def _handle_search_request(
        self,
        query: str,
        articles: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Handle semantic search requests."""

        if self.semantic_search is None:
            return {
                "status": "error",
                "message": "Semantic search module is unavailable.",
            }

        if articles is None or articles.empty:
            return {
                "status": "error",
                "message": "No articles available for searching.",
            }

        search_results = self.semantic_search.search(
            query,
            articles,
        )

        return {
            "status": "success",
            "intent": "search",
            "results": search_results,
        }

    def _handle_general_request(
        self,
        query: str,
        articles: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Fallback response for general NewsBot queries."""

        return {
            "status": "success",
            "intent": "general",
            "message": (
                "I can help summarize news, analyze sentiment, "
                "discover topics, extract entities, and perform "
                "semantic search. Try asking a more specific question."
            ),
        }
