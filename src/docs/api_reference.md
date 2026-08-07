# NewsBot Intelligence System 2.0
## API Reference

---

# Data Processing

## DataProcessor

### clean_text(text)

Cleans and normalizes raw text by converting it to lowercase and removing
extra whitespace.

**Parameters**

- `text (str)` - Raw text.

**Returns**

- `str` - Cleaned text.

---

# Classification

## AdvancedNewsClassifier

### train(X_train, y_train)

Train the news classification model.

**Parameters**

- `X_train (List[str])`
- `y_train (List[str])`

---

### predict_with_confidence(texts)

Predicts article categories and confidence scores.

**Returns**

- Primary prediction
- Confidence score
- Alternative category predictions

---

### explain_prediction(article_text)

Returns an explanation of why a category was predicted.

---

# Topic Modeling

## TopicDiscoveryEngine

### fit_topics(documents)

Train the topic model.

---

### get_article_topics(article_text)

Returns the topic distribution for a single article.

---

### track_topic_trends(df)

Tracks how topics evolve over time.

---

### visualize_topic_trends_plotly(trend_df)

Creates an interactive Plotly visualization of topic trends.

---

# Sentiment Analysis

## SentimentEvolutionTracker

Provides sentiment analysis and sentiment trend tracking.

---

# Entity Relationship Mapping

## EntityRelationshipMapper

### extract_entities(article_text)

Extract named entities.

---

### extract_relationships(article_text)

Identify relationships between entities.

---

### build_knowledge_graph(articles)

Construct a knowledge graph from multiple articles.

---

### find_entity_connections(entity1, entity2)

Find the shortest relationship path between two entities.

---

### visualize_graph_plotly()

Generate an interactive knowledge graph visualization.

---

# Language Models

## IntelligentSummarizer

Generate concise summaries of news articles.

---

## SemanticSearchEngine

Perform semantic similarity search.

---

## ContentEnhancer

Enhance articles with contextual information.

---

# Multilingual Processing

## MultilingualProcessor

Supports:

- Language detection
- Translation
- Cross-language processing

---

# Conversational Interface

## ConversationalInterface

### process_query(query)

Routes natural-language questions to the appropriate NewsBot module.

Supported requests include:

- Article summaries
- Sentiment analysis
- Topic analysis
- Named entity recognition
- Semantic search

---

# Version

NewsBot Intelligence System 2.0

Version 2.0

Python 3.11+
