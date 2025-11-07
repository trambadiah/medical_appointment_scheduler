"""
faq_rag.py
-----------
LangChain-based RAG FAQ retriever for the scheduling agent.
"""

import os
import json
from typing import List, Dict
from .vector_store import add_faq_documents, get_vector_store

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "clinic_info.json")

def load_faq_data(force_reload: bool = False):
    """Load FAQs from clinic_info.json into Chroma."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"clinic_info.json not found at {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    vector_store = get_vector_store()
    existing_count = len(vector_store.get()['ids']) if vector_store.get()['ids'] else 0

    if existing_count == 0 or force_reload:
        add_faq_documents(faq_data)
        print(f"{len(faq_data)} FAQs loaded into Chroma.")
    else:
        print(f"Vector store already contains {existing_count} entries.")

def retrieve_answer(query: str) -> str:
    """Retrieve the most relevant FAQ answer using LangChain + Chroma."""
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=1)

    if not results:
        return "I'm not sure about that. Please contact the clinic directly."

    return results[0].metadata.get("answer", "Sorry, I don’t have that information.")

