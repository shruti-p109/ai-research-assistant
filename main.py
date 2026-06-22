from rag.generator import generate_answer
from indexing.embedder import get_embeddings, get_embeddings_dimension
from indexing.vector_store import VectorStore
from config import TOP_K
from storage.database import get_chunks_by_ids, SessionLocal

# test query
query = "What is an execution-state capsule?"
query_embedding = get_embeddings([query])[0]

# load faiss index
vector_store = VectorStore(get_embeddings_dimension())

# retrieval
relevant_chunk_ids, scores = vector_store.search(query_embedding, TOP_K)

# get chunks from ids
with SessionLocal() as session:
    relevant_chunks = get_chunks_by_ids(session, relevant_chunk_ids.tolist())

# build context from retrieved chunks
context = "\n\n".join(f"""
(DOCUMENT: {r[1]})
{r[0]}
""" for r in relevant_chunks)

# generate answer
answer = generate_answer(query, context)
print("\nAnswer:")
print(answer)
