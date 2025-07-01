from __future__ import annotations
import os
from typing import Tuple, Optional

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.settings import settings
from src.database.database import Database

async def search_faq(question: str, return_score: bool = False) -> Optional[Tuple[dict, float]]:
    """Busca en el índice FAISS la FAQ más similar a la pregunta."""
    index_path = "faqs_index"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.API_KEY)

    if not os.path.exists(index_path):
        db = Database()
        created = await db.update_faq_vectors()
        if not created:
            return (None, 0.0) if return_score else None

    store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    docs = store.similarity_search_with_score(question, k=1)
    
    if not docs:
        return (None, 0.0) if return_score else None

    doc, distance = docs[0]
    for k,v in doc.metadata.items():
        print(f"{k}: {v}")
    similarity = 1 / (1 + distance)
    if return_score:
        return doc.metadata, similarity
    return doc.metadata