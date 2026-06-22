# arXiv -> download PDFs -> update metadata

from ingestion.arxiv_client import donwload_papers

donwload_papers('cs', 'agentic ai', 5)