from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DIR, COLLECTION, EMBED_MODEL


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(EMBED_MODEL)


def get_collection():
    client = chromadb.PersistentClient(CHROMA_DIR)
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
