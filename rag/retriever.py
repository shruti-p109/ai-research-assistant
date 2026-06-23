# retrieve relevant chunks for context for user query
from indexing.embedder import get_embeddings, get_embeddings_dimension
from storage.database import get_chunks_by_ids, SessionLocal
from indexing.vector_store import VectorStore
from logger_setup import logger

def retrieve(query: str, top_k: int) -> list:
    try:
        query_embedding = get_embeddings([query])[0]

        # load faiss index
        vector_store = VectorStore(get_embeddings_dimension())
    
        # retrieval
        relevant_chunk_ids = []
        relevant_chunk_ids = vector_store.search(query_embedding, top_k)
        
        # get chunks from ids
        relevant_chunks = []
        if relevant_chunk_ids.size != 0:
            with SessionLocal() as session:
                relevant_chunks = get_chunks_by_ids(session, relevant_chunk_ids.tolist())

        return [{'text':chunk[0], 'source':chunk[1]} for chunk in relevant_chunks]
    except Exception as e:
        logger.error(f"Error occurred during retrieval: {e}")