# save/load/search FAISS
import faiss
import numpy as np
from config import INDEX_PATH
import os
from config import TOP_K

class VectorStore:
    def __init__(self, dimensions):
        if os.path.exists(INDEX_PATH):
            # load existing index from disk
            self.index = faiss.read_index(INDEX_PATH)
        else:
            # create new index
            self.index = faiss.IndexIDMap(
                faiss.IndexFlatL2(dimensions)
            )
    
    def add(self, embeddings, chunk_ids):
        # adds in memory
        self.index.add_with_ids(
            np.array(embeddings, dtype=np.float32),
            np.array(chunk_ids, dtype=np.int64)
        )
    
    def save(self):
        # persist index on disk
        faiss.write_index(
            self.index,
            INDEX_PATH
        )

    def search(self, query_embedding, top_k = TOP_K):
        distances, chunk_ids = self.index.search(np.array([query_embedding], dtype=np.float32), top_k)
        return chunk_ids[0]