"""
Sentiment analysis module for NewsBot Intelligence System 2.0.
"""

import re
from typing import Any, Dict, List, Optional


class SentimentEvolutionTracker:
    """Advanced multi-dimensional sentiment analysis engine with aspect extraction,

    temporal evolution tracking, and anomaly detection.
    """

    def __init__(self):
        # 1. Initialize NLTK VADER Analyzer
        try:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer

            self.vader = SentimentIntensityAnalyzer()
        except (ImportError, LookupError):
            import nltk

            nltk.download("vader_lexicon", quiet=True)
            from nltk.sentiment.vader import SentimentIntensityAnalyzer

            self.vader = SentimentIntensityAnalyzer()

        # 2. Emotion Lexicon Rules (Keyword sets for multi-dimensional affect mapping)
        self.emotion_lexicon = {
            "joy": {
                "happy",
                "excited",
                "growth",
                "success",
                "win",
                "triumph",
                "optimistic",
                "record",
                "celebrate",
                "gain",
            },
            "anger": {
                "outrage",
                "illegal",
                "protest",
                "furious",
                "scandal",
                "corrupt",
                "violation",
                "demand",
                "strike",
                "boycott",
            },
            "fear": {
                "risk",
                "threat",
                "crisis",
                "warning",
                "collapse",
                "danger",
                "panic",
                "inflation",
                "recession",
                "vulnerable",
            },
            "sadness": {
                "tragic",
                "loss",
                "death",
                "mourn",
                "decline",
                "devastating",
                "fail",
                "grief",
                "closure",
                "suffer",
            },
            "surprise": {
                "unexpected",
                "shocking",
                "breakthrough",
                "unprecedented",
                "sudden",
                "astonishing",
                "dramatic",
                "reveal",
            },
        }

    def _preprocess_text(self, text: str) -> str:
        """Sanitizes input text while preserving punctuation used by VADER."""
        if not isinstance(text, str):
            return ""
        return re.sub(r"\s+", " ", text).strip()

    def analyze_sentiment(
        self, article_text: str, aspects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Performs multi-dimensional sentiment scoring, emotion detection,

        aspect-based sentiment evaluation, and key phrase extractions.
        """
        clean_text = self._preprocess_text(article_text)
        if not clean_text:
            return {
                "sentiment": "neutral",
                "compound": 0.0,
                "emotions": {},
                "aspects": {},
            }

        # 1. Valence / Polarity Scoring via VADER
        scores = self.vader.polarity_scores(clean_text)
        compound = float(scores["compound"])

        # Categorize overall sentiment based on compound score
        if compound >= 0.05:
            sentiment_label = "positive"
        elif compound <= -0.05:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

        # Calculate confidence metric from raw polarity proportions
        confidence = round(
            float(abs(compound) if compound != 0 else scores["neu"]), 4
        )
              # 2. Emotional Dimensions Calculation
        tokens = set(re.findall(r"\b[a-z]{3,}\b", clean_text.lower()))
        doc_len = max(len(tokens), 1)

        emotion_scores = {}
        for emotion, keywords in self.emotion_lexicon.items():
            matches = tokens.intersection(keywords)
            # Normalized score relative to matched affect vocabulary count
            raw_score = len(matches) / math.sqrt(doc_len)
            emotion_scores[emotion] = round(float(min(raw_score, 1.0)), 3)

        # 3. Aspect-Based Sentiment Analysis (ABSA)
        aspect_results = {}
        if aspects:
            sentences = re.split(r"[.!?]+", clean_text)
            for aspect in aspects:
                aspect_lower = aspect.lower()

                # Find sentences containing target aspect keyword
                relevant_sents = [
                    s for s in sentences if aspect_lower in s.lower()
                ]

                if relevant_sents:
                    aspect_combined = " ".join(relevant_sents)
                    asp_compound = float(
                        self.vader.polarity_scores(aspect_combined)["compound"]
                    )

                    aspect_results[aspect] = {
                        "compound": round(asp_compound, 4),
                        "sentiment": (
                            "positive"
                            if asp_compound >= 0.05
                            else (
                                "negative"
                                if asp_compound <= -0.05
                                else "neutral"
                            )
                        ),
                        "mention_count": len(relevant_sents),
                    }

                else:
                    aspect_results[aspect] = {
                        "compound": 0.0,
                        "sentiment": "neutral",
                        "mention_count": 0,
                    }

        # 4. Key Phrase Drivers
        words = re.findall(r"\b[a-zA-Z]{3,}\b", clean_text)

        pos_drivers = [
            w for w in words
            if self.vader.polarity_scores(w)["compound"] > 0.3
        ]

        neg_drivers = [
            w
            for w in words
            if self.vader.polarity_scores(w)["compound"] < -0.3
        ]

        return {
            "text": clean_text,
            "overall_sentiment": sentiment_label,
            "compound_score": round(compound, 4),
            "confidence": confidence,
            "valences": {
                "positive": round(scores["pos"], 3),
                "neutral": round(scores["neu"], 3),
                "negative": round(scores["neg"], 3),
            },
            "emotions": emotion_scores,
            "aspect_sentiments": aspect_results,
            "key_drivers": {
                "positive_words": list(set(pos_drivers))[:5],
                "negative_words": list(set(neg_drivers))[:5],
            },
        }
          def track_sentiment_over_time(
        self,
        df: pd.DataFrame,
        text_column: str = "short_description",
        date_column: str = "date",
        freq: str = "ME",
    ) -> pd.DataFrame:
        """Aggregates compound sentiment and emotional profiles over time intervals."""
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])

        # Analyze each document
        compounds, pos_counts, neg_counts, neu_counts = [], [], [], []
        joys, fears, angers = [], [], []

        for text in df[text_column]:
            res = self.analyze_sentiment(str(text))
            compounds.append(res["compound_score"])
            pos_counts.append(1 if res["overall_sentiment"] == "positive" else 0)
            neg_counts.append(1 if res["overall_sentiment"] == "negative" else 0)
            neu_counts.append(1 if res["overall_sentiment"] == "neutral" else 0)
            joys.append(res["emotions"].get("joy", 0.0))
            fears.append(res["emotions"].get("fear", 0.0))
            angers.append(res["emotions"].get("anger", 0.0))

        df["compound"] = compounds
        df["is_pos"] = pos_counts
        df["is_neg"] = neg_counts
        df["is_neu"] = neu_counts
        df["emotion_joy"] = joys
        df["emotion_fear"] = fears
        df["emotion_anger"] = angers

        # Time Series Resampling
        timeline = (
            df.groupby(pd.Grouper(key=date_column, freq=freq))
            .agg(
                mean_compound=("compound", "mean"),
                std_compound=("compound", "std"),
                article_count=("compound", "count"),
                positive_articles=("is_pos", "sum"),
                negative_articles=("is_neg", "sum"),
                neutral_articles=("is_neu", "sum"),
                avg_joy=("emotion_joy", "mean"),
                avg_fear=("emotion_fear", "mean"),
                avg_anger=("emotion_anger", "mean"),
            )
            .reset_index()
        )

        timeline["mean_compound"] = (
            timeline["mean_compound"].fillna(0.0).round(4)
        )
        timeline["std_compound"] = (
            timeline["std_compound"].fillna(0.0).round(4)
        )

        return timeline

    def detect_sentiment_anomalies(
        self, timeline_df: pd.DataFrame, z_threshold: float = 2.0
    ) -> pd.DataFrame:
        """Identifies sentiment shift anomalies using statistical Z-Score thresholding."""
        df = timeline_df.copy()

        if len(df) < 3:
            df["is_anomaly"] = False
            df["z_score"] = 0.0
            return df

        mean_val = df["mean_compound"].mean()
        std_val = df["mean_compound"].std()

        if std_val == 0:
            df["z_score"] = 0.0
            df["is_anomaly"] = False
            return df

        df["z_score"] = (
            (df["mean_compound"] - mean_val) / std_val
        ).round(3)

        df["is_anomaly"] = df["z_score"].abs() >= z_threshold

        return df
          def visualize_sentiment_evolution_plotly(
        self, timeline_df: pd.DataFrame, date_column: str = "date"
    ) -> go.Figure:
        """Generates an interactive Plotly dual-axis chart showing compound sentiment curve

        and emotional dimension breakdown over time.
        """
        fig = go.Figure()

        # Line: Mean Compound Sentiment
        fig.add_trace(
            go.Scatter(
                x=timeline_df[date_column],
                y=timeline_df["mean_compound"],
                mode="lines+markers",
                name="Avg Sentiment Score",
                line=dict(color="#1f77b4", width=3),
            )
        )

        # Bar: Sentiment Breakdown (Positive vs Negative counts)
        fig.add_trace(
            go.Bar(
                x=timeline_df[date_column],
                y=timeline_df["positive_articles"],
                name="Positive Volume",
                marker_color="#2ca02c",
                opacity=0.5,
            )
        )

        fig.add_trace(
            go.Bar(
                x=timeline_df[date_column],
                y=timeline_df["negative_articles"],
                name="Negative Volume",
                marker_color="#d62728",
                opacity=0.5,
            )
        )

        fig.update_layout(
            title="🎭 Sentiment Evolution and Volume Trends Over Time",
            xaxis_title="Timeline Date",
            yaxis_title="Sentiment Metric / Article Count",
            barmode="group",
            template="plotly_white",
            hovermode="x unified",
        )

        return fig
