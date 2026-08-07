"""
Unit tests for the topic modeling module.
"""

import unittest

from src.analysis.topic_modeler import TopicDiscoveryEngine


class TestTopicDiscoveryEngine(unittest.TestCase):
    """Tests for the TopicDiscoveryEngine."""

    def setUp(self):
        self.topic_modeler = TopicDiscoveryEngine(n_topics=2)

        self.documents = [
            "Artificial intelligence is transforming healthcare.",
            "Machine learning improves medical diagnosis.",
            "The football team won the championship game.",
            "Fans celebrated the exciting sports victory.",
        ]

    def test_initialization(self):
        """Engine should initialize correctly."""
        self.assertEqual(self.topic_modeler.n_topics, 2)
        self.assertFalse(self.topic_modeler.is_fitted)

    def test_preprocess_documents(self):
        """Documents should be tokenized and cleaned."""
        processed = self.topic_modeler.preprocess_documents(
            self.documents
        )

        self.assertEqual(len(processed), len(self.documents))
        self.assertIsInstance(processed[0], list)

    def test_fit_topics(self):
        """Topic model should fit successfully."""
        results = self.topic_modeler.fit_topics(self.documents)

        self.assertTrue(self.topic_modeler.is_fitted)
        self.assertIn("coherence_cv", results)

    def test_get_article_topics(self):
        """Topic distribution should be returned for an article."""
        self.topic_modeler.fit_topics(self.documents)

        topics = self.topic_modeler.get_article_topics(
            "Artificial intelligence is improving hospitals."
        )

        self.assertIsInstance(topics, list)

    def test_track_topic_trends(self):
        """Method should exist after fitting the model."""
        self.topic_modeler.fit_topics(self.documents)

        self.assertTrue(
            hasattr(
                self.topic_modeler,
                "track_topic_trends",
            )
        )


if __name__ == "__main__":
    unittest.main()
