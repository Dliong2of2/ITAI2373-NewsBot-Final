"""
Semantic embeddings module for NewsBot Intelligence System 2.0.
"""

from typing import Any, Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSearchEngine:
    """Semantic search engine using sentence embeddings."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

        self.article_embeddings = None
        self.documents = None

    def build_index(
        self,
        documents: List[str],
    ) -> None:
        """Generate embeddings for all documents."""

        self.documents = documents

        self.article_embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            show_progress_bar=True,
        )
          def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Perform semantic search using cosine similarity."""

        if self.article_embeddings is None:
            raise RuntimeError(
                "Index has not been built. Call build_index() first."
            )

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
        )

        similarities = cosine_similarity(
            query_embedding,
            self.article_embeddings,
        )[0]

        ranked_indices = np.argsort(similarities)[::-1][:top_k]

        results = []

        for idx in ranked_indices:
            results.append(
                {
                    "document": self.documents[idx],
                    "similarity": round(
                        float(similarities[idx]),
                        4,
                    ),
                }
            )

        return results

    def find_similar_articles(
        self,
        article_index: int,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Find articles most similar to a given article."""

        if self.article_embeddings is None:
            raise RuntimeError(
                "Index has not been built."
            )

        similarities = cosine_similarity(
            [self.article_embeddings[article_index]],
            self.article_embeddings,
        )[0]

        ranked_indices = np.argsort(similarities)[::-1]

        results = []

        for idx in ranked_indices:
            if idx == article_index:
                continue

            results.append(
                {
                    "document": self.documents[idx],
                    "similarity": round(
                        float(similarities[idx]),
                        4,
                    ),
                }
            )

            if len(results) >= top_k:
                break

        return results
      
