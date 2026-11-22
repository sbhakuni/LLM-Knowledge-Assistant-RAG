import os

from dotenv import load_dotenv

load_dotenv()

DOCS_DIR = "data/docs"
SOURCES_FILE = "data/sources.json"
CHROMA_DIR = "storage/chroma"
COLLECTION = "knowledge_base"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
TOP_K = 5
MAX_CHUNK_CHARS = 1500

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
