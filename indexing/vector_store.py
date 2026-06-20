# build/load/search FAISS
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimensions):
        self.index = faiss.IndexIDMap(
            faiss.IndexFlatL2(dimensions)
        )
    
    def add(self, embeddings, chunk_ids):
        self.index.add_with_ids(
            np.array(embeddings, dtype=np.float32),
            np.array(chunk_ids, dtype=np.int64)
        )

    def search(self, query_embedding, top_k=5):
        distances, ids = self.index.search(np.array([query_embedding], dtype=np.float32), top_k)
        return ids[0], distances[0]