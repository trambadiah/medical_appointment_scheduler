"""
embeddings.py
--------------
Generates vector embeddings using the OpenAI-compatible API
(OpenRouter or local Ollama embedding endpoint).
"""

import os
from openai import OpenAI
from typing import List
from langchain_community.embeddings import OllamaEmbeddings

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")


def get_embedding_function():
    """
    Return an Ollama embedding function for LangChain.
    Uses a local embedding model (e.g., nomic-embed-text).
    """
    return OllamaEmbeddings(model=EMBEDDING_MODEL)
