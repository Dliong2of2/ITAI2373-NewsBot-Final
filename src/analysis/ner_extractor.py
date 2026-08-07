"""
Named Entity Recognition (NER) and Relationship Extraction module
for NewsBot Intelligence System 2.0.
"""

from typing import Any, Dict, List, Tuple, Union

import networkx as nx
import plotly.graph_objects as go
import spacy


class EntityRelationshipMapper:
    """Advanced Named Entity Recognition (NER) and Relationship Extraction Engine.

    Constructs multi-article knowledge graphs, identifies entity roles,
    and calculates graph traversal connections using NetworkX.
    """

    def __init__(self, spacy_model: str = "en_core_web_sm"):
        # 1. Load spaCy NLP Pipeline
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            import subprocess

            print(
                f"⚠️ spaCy model '{spacy_model}' not found. Attempting download..."
            )
            subprocess.run(["python", "-m", "spacy", "download", spacy_model])
            self.nlp = spacy.load(spacy_model)

        # 2. Knowledge Graph Storage
        self.graph = nx.DiGraph()

        # Taxonomy label map for clean entity categorization
        self.entity_type_map = {
            "PERSON": "Person",
            "ORG": "Organization",
            "GPE": "Location (Geo-Political)",
            "LOC": "Location (Physical)",
            "DATE": "Temporal Event",
            "TIME": "Temporal Event",
            "PRODUCT": "Product/Technology",
            "EVENT": "Event",
            "MONEY": "Financial Quantity",
        }

    def extract_entities(self, article_text: str) -> List[Dict[str, Any]]:
        """Extracts named entities along with their syntactic label categories and context phrases."""
        doc = self.nlp(article_text)
        extracted = []

        for ent in doc.ents:
            category = self.entity_type_map.get(ent.label_, ent.label_)
            extracted.append(
                {
                    "text": ent.text.strip(),
                    "label": ent.label_,
                    "category": category,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                    "root_verb": ent.root.head.text
                    if ent.root.head.pos_ == "VERB"
                    else None,
                }
            )

        return extracted
            def extract_relationships(
        self, article_text: str
    ) -> List[Dict[str, Any]]:
        """Extracts (Subject, Relation/Verb, Object) triples using dependency parse trees."""
        doc = self.nlp(article_text)
        relationships = []

        for sent in doc.sents:
            # Find main verbs acting as relational predicates
            verbs = [token for token in sent if token.pos_ == "VERB"]

            for verb in verbs:
                subjects = [
                    w
                    for w in verb.lefts
                    if w.dep_ in ("nsubj", "nsubjpass", "compound")
                ]
                objects = [
                    w
                    for w in verb.rights
                    if w.dep_ in ("dobj", "pobj", "attr", "oprd")
                ]

                # Resolve full sub-tree entities for subjects and objects
                for subj in subjects:
                    for obj in objects:
                        subj_entity = " ".join([t.text for t in subj.subtree])
                        obj_entity = " ".join([t.text for t in obj.subtree])

                        # Keep clean relations with sufficient token length
                        if len(subj_entity) > 1 and len(obj_entity) > 1:
                            relationships.append(
                                {
                                    "subject": subj_entity.strip(),
                                    "relation": verb.lemma_.lower(),
                                    "object": obj_entity.strip(),
                                    "sentence_context": sent.text.strip(),
                                }
                            )

        return relationships

    def build_knowledge_graph(
        self, articles: List[str]
    ) -> Dict[str, Union[int, List[Tuple[str, str, str]]]]:
        """Builds a directed Knowledge Graph across multiple articles by aggregating nodes and relation edges."""
        self.graph.clear()
        edge_count = 0

        for article in articles:
            # 1. Add Entity Nodes
            entities = self.extract_entities(article)
            for ent in entities:
                if not self.graph.has_node(ent["text"]):
                    self.graph.add_node(
                        ent["text"],
                        label=ent["label"],
                        category=ent["category"],
                    )

            # 2. Add Relationship Edges
            relations = self.extract_relationships(article)
            for rel in relations:
                subj = rel["subject"]
                obj = rel["object"]
                predicate = rel["relation"]

                # Add nodes if missing
                if not self.graph.has_node(subj):
                    self.graph.add_node(
                        subj,
                        label="ENTITY",
                        category="Entity",
                    )

                if not self.graph.has_node(obj):
                    self.graph.add_node(
                        obj,
                        label="ENTITY",
                        category="Entity",
                    )

                # Add weighted directed edge
                if self.graph.has_edge(subj, obj):
                    self.graph[subj][obj]["weight"] += 1
                else:
                    self.graph.add_edge(
                        subj,
                        obj,
                        relation=predicate,
                        weight=1,
                    )

                edge_count += 1

        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "graph_density": round(float(nx.density(self.graph)), 4),
        }
            def find_entity_connections(
        self, entity1: str, entity2: str
    ) -> Dict[str, Any]:
        """Discovers direct or indirect connections (shortest paths) between two entities in the knowledge graph."""
        if not self.graph.has_node(entity1) or not self.graph.has_node(entity2):
            return {
                "connected": False,
                "reason": "One or both entities do not exist in the current knowledge graph.",
            }

        try:
            # Undirected search for structural path discovery
            undirected_g = self.graph.to_undirected()
            path = nx.shortest_path(undirected_g, source=entity1, target=entity2)

            path_details = []
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge_data = self.graph.get_edge_data(u, v) or self.graph.get_edge_data(v, u)
                rel_type = edge_data.get("relation", "connected_to") if edge_data else "related"
                path_details.append(f"({u}) --[{rel_type}]--> ({v})")

            return {
                "connected": True,
                "path_length": len(path) - 1,
                "path_nodes": path,
                "connection_chain": " -> ".join(path_details),
            }

        except nx.NetworkXNoPath:
            return {
                "connected": False,
                "reason": f"No relational path found connecting '{entity1}' and '{entity2}'.",
            }

    def visualize_graph_plotly(self) -> go.Figure:
        """Generates an interactive 2D node-link network visualization using Plotly."""
        if self.graph.number_of_nodes() == 0:
            raise ValueError("Knowledge graph is empty. Call build_knowledge_graph() first.")

        # Compute Spring Layout Positions
        pos = nx.spring_layout(self.graph, k=0.5, seed=42)

        # Edges Plot
        edge_x, edge_y = [], []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        # Nodes Plot
        node_x, node_y, node_text = [], [], []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            cat = self.graph.nodes[node].get("category", "Entity")
            node_text.append(f"Entity: {node}<br>Category: {cat}")

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            hoverinfo="text",
            text=[node for node in self.graph.nodes()],
            textposition="top center",
            hovertext=node_text,
            marker=dict(
                size=12,
                color="#1f77b4",
                line=dict(width=2, color="DarkSlateGrey"),
            ),
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title="🕸️ Entity Relationship Knowledge Graph",
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                template="plotly_white",
            ),
        )
        return fig
