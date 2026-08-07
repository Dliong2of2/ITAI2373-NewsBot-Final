"""
Topic modeling module for NewsBot Intelligence System 2.0.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gensim import corpora
from gensim.models import CoherenceModel, LdaModel


class TopicDiscoveryEngine:
    """Advanced Topic Modeling and Temporal Trend Discovery Engine.

    Extracts latent themes, computes topic coherence (c_v),
    assigns topic probability distributions to articles,
    and tracks temporal shifts across dates.
    """

    def __init__(self, n_topics: int = 10, method: str = "lda"):
        self.n_topics = n_topics
        self.method = method.lower()

        # Gensim artifacts
        self.dictionary: Optional[corpora.Dictionary] = None
        self.corpus: Optional[List[List[Tuple[int, int]]]] = None
        self.model: Optional[LdaModel] = None
        self.coherence_score: Optional[float] = None
        self.is_fitted: bool = False

    def preprocess_documents(self, documents: List[str]) -> List[List[str]]:
        """Tokenization, cleaning, stop-word removal, and short-token filtering."""
        from nltk.corpus import stopwords

        try:
            stop_words = set(stopwords.words("english"))
        except LookupError:
            import nltk

            nltk.download("stopwords", quiet=True)
            stop_words = set(stopwords.words("english"))

        # Add domain-specific news boilerplate to stop words
        stop_words.update(
            [
                "said",
                "news",
                "report",
                "according",
                "new",
                "year",
                "one",
                "two",
            ]
        )

        tokenized_docs = []

        for doc in documents:
            if not isinstance(doc, str):
                continue

            doc = doc.lower()
            tokens = re.findall(r"\b[a-z]{3,}\b", doc)

            cleaned = [
                word
                for word in tokens
                if word not in stop_words
            ]

            if cleaned:
                tokenized_docs.append(cleaned)

        return tokenized_docs

    def fit_topics(
        self,
        documents: List[str],
        passes: int = 10,
        eval_coherence: bool = True,
    ) -> Dict[str, Any]:
        """Builds dictionary, converts corpus to Bag-of-Words, trains the LDA model,
        and computes topic coherence."""

        print(f"⚙️ Preprocessing {len(documents)} documents for topic discovery...")
        processed_tokens = self.preprocess_documents(documents)

        # Create dictionary & corpus
        self.dictionary = corpora.Dictionary(processed_tokens)
        self.dictionary.filter_extremes(no_below=2, no_above=0.85)

        self.corpus = [
            self.dictionary.doc2bow(doc)
            for doc in processed_tokens
        ]

        if not self.corpus:
            raise ValueError(
                "Corpus is empty after preprocessing. Check input text."
            )

        print(
            f"🏋️ Fitting {self.method.upper()} model "
            f"with {self.n_topics} topics..."
        )

        if self.method == "lda":
            self.model = LdaModel(
                corpus=self.corpus,
                id2word=self.dictionary,
                num_topics=self.n_topics,
                random_state=42,
                update_every=1,
                chunksize=100,
                passes=passes,
                alpha="auto",
                per_word_topics=True,
            )
        else:
            raise NotImplementedError(
                f"Method '{self.method}' is not implemented. Use 'lda'."
            )

        self.is_fitted = True

        if eval_coherence:
            print("📊 Computing Topic Coherence Score (c_v)...")

            coherence_model = CoherenceModel(
                model=self.model,
                texts=processed_tokens,
                dictionary=self.dictionary,
                coherence="c_v",
            )

            self.coherence_score = round(
                float(coherence_model.get_coherence()),
                4,
            )

            print(
                f"✅ Topic Coherence (c_v): "
                f"{self.coherence_score}"
            )

        return {
            "num_topics": self.n_topics,
            "vocab_size": len(self.dictionary),
            "coherence_cv": self.coherence_score,
            "status": "fitted",
        }

    def get_article_topics(
        self,
        article_text: str,
    ) -> List[Dict[str, Any]]:
        """Infers topic distribution for a single unseen article."""

        if (
            not self.is_fitted
            or self.model is None
            or self.dictionary is None
        ):
            raise RuntimeError(
                "Engine must be fitted before calling get_article_topics()."
            )

        tokens = self.preprocess_documents([article_text])

        if not tokens:
            return []

        bow = self.dictionary.doc2bow(tokens[0])
        topic_distribution = self.model.get_document_topics(bow)

        results = []

        for topic_id, probability in sorted(
            topic_distribution,
            key=lambda x: x[1],
            reverse=True,
        ):
            topic_terms = [
                word
                for word, _ in self.model.show_topic(topic_id, topn=4)
            ]

            results.append(
                {
                    "topic_id": int(topic_id),
                    "probability": round(float(probability), 4),
                    "topic_name": (
                        f"Topic #{topic_id}: "
                        + ", ".join(topic_terms)
                    ),
                }
            )

        return results

    def track_topic_trends(
        self,
        df: pd.DataFrame,
        text_column: str = "short_description",
        date_column: str = "date",
        freq: str = "ME",
    ) -> pd.DataFrame:
        """Tracks dominant topic evolution over time."""

        if not self.is_fitted:
            raise RuntimeError(
                "Engine must be fitted before tracking trends."
            )

        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])

        dominant_topics = []

        for text in df[text_column]:
            topics = self.get_article_topics(str(text))
            dominant_topic = topics[0]["topic_id"] if topics else -1
            dominant_topics.append(dominant_topic)

        df["dominant_topic"] = dominant_topics

        trend_df = (
            df.groupby(
                [
                    pd.Grouper(key=date_column, freq=freq),
                    "dominant_topic",
                ]
            )
            .size()
            .reset_index(name="article_count")
        )

        return trend_df

    def visualize_topic_trends_plotly(
        self,
        trend_df: pd.DataFrame,
        date_column: str = "date",
    ) -> go.Figure:
        """Generates an interactive Plotly visualization of topic evolution."""

        labels = {}

        for topic_id in trend_df["dominant_topic"].unique():
            if topic_id == -1:
                labels[topic_id] = "Unknown/Unclassified"
            elif self.model:
                terms = [
                    word
                    for word, _ in self.model.show_topic(topic_id, topn=3)
                ]
                labels[topic_id] = (
                    f"Topic {topic_id}: "
                    + ", ".join(terms)
                )

        trend_df["topic_label"] = trend_df["dominant_topic"].map(labels)

        fig = px.line(
            trend_df,
            x=date_column,
            y="article_count",
            color="topic_label",
            title="📈 Topic Evolution Over Time",
            labels={
                "article_count": "Articles Count",
                "topic_label": "Topic Keyword Group",
            },
            markers=True,
        )

        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
        )

        return fig
