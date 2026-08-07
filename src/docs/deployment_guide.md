# NewsBot Intelligence System 2.0
# Deployment Guide

## Overview

This guide explains how to set up and run the NewsBot Intelligence
System 2.0.

---

# System Requirements

- Python 3.11 or later
- pip
- Git
- Jupyter Notebook or Google Colab

---

# Clone the Repository

```bash
git clone https://github.com/<username>/ITAI2373-NewsBot-Final.git
cd ITAI2373-NewsBot-Final
```

---

# Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

Required libraries include:

- pandas
- numpy
- scikit-learn
- nltk
- gensim
- spacy
- plotly
- matplotlib
- textblob
- networkx
- kagglehub

---

# Download Required Resources

Run once:

```python
import nltk

nltk.download("stopwords")
nltk.download("wordnet")
```

If using spaCy:

```bash
python -m spacy download en_core_web_sm
```

---

# Dataset

The project uses the Kaggle News Category Dataset.

The notebook loads the dataset directly through KaggleHub.

No manual download is required if KaggleHub is configured correctly.

---

# Running the Project

Open the completed notebook:

```
group_4_newsbot2_student_guidance_notebook.ipynb
```

Run every cell from top to bottom.

The notebook performs:

- Data preprocessing
- News classification
- Topic modeling
- Sentiment analysis
- Named entity recognition
- Semantic search
- Multilingual processing
- Conversational querying

---

# Repository Structure

```
src/
│
├── analysis/
├── conversation/
├── data/
├── data_processing/
├── docs/
├── language_models/
├── multilingual/
└── utils/
```

---

# Generated Outputs

The notebook displays:

- Classification results
- Topic analysis
- Sentiment reports
- Knowledge graphs
- Interactive Plotly visualizations
- Generated summaries

Results are displayed inside the notebook and are not automatically saved.

---

# Troubleshooting

## Missing Python package

Install the missing package using:

```bash
pip install package_name
```

---

## NLTK LookupError

Download the required resource:

```python
import nltk
nltk.download("stopwords")
nltk.download("wordnet")
```

---

## spaCy Model Error

Install the English language model:

```bash
python -m spacy download en_core_web_sm
```

---

## Dataset Loading Error

Verify that KaggleHub is installed:

```bash
pip install kagglehub
```

Ensure your Kaggle credentials are configured correctly.

---

# Authors

Group 4

Houston Community College

ITAI 2373 – NLP in Cybersecurity

NewsBot Intelligence System 2.0
