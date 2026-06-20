# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "storage"
PDF_DIR =  DATA_DIR / "pdfs" / "arxiv"
INDEX_PATH = DB_DIR / "faiss.index"

DB_PATH = DB_DIR / "rag_system.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}" # three forward slashes for absolute path

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 5

OLLAMA_MODEL = "llama3.1:8b"

ARXIV_BASE_URL = "http://export.arxiv.org/api/query?"
