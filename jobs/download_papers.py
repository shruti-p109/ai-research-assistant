# arXiv
# ↓
# download PDFs
# ↓
# update metadata.json

# Creates entries like:
# {
#   "2508.09549.pdf": {
#     "title": "CS-Agent",
#     "published": "2025-08-12",
#     "authors": [
#       "Author A",
#       "Author B"
#     ]
#   }
# }
from repo.ingestion.arxiv_client import donwload_papers
from repo.storage.database import insert_document


donwload_papers('cs', 'speech emotion recognition', 5)