"""
vector_store.py
----------------
Handles Chroma vector database operations for clinic FAQs.
"""

import os
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from .embeddings import get_embedding_function

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def get_vector_store():
    """Return or initialize Chroma vector store."""
    embedding_fn = get_embedding_function()
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_fn,
        collection_name="clinic_faqs"
    )

def add_faq_documents(faq_data):
    """
    Add FAQs to the Chroma database.
    faq_data = [{"question": "...", "answer": "..."}]
    """
    vector_store = get_vector_store()
    docs = [
        Document(page_content=item["question"], metadata={"answer": item["answer"]})
        for item in faq_data
    ]
    vector_store.add_documents(docs)
    vector_store.persist()
    print(f"Added {len(faq_data)} FAQ entries to Chroma.")

def query_faq(question: str, k: int = 1):
    """Query Chroma for most relevant FAQ entries."""
    vector_store = get_vector_store()
    results = vector_store.similarity_search(question, k=k)
    return results
