from rag.generator import generate_answer
from rag.retriever import retrieve

# test query
query = "How is an execution-state capsule different from vLLM's PagedAttention?"

# retrieval
relevant_chunks = retrieve(query, 5)

# build context from retrieved chunks
if relevant_chunks:
    context = "\n\n".join(
        f"(DOCUMENT: {chunk['source']})\n{chunk['text']}"
        for chunk in relevant_chunks
    )
 
    # generate answer
    answer = generate_answer(query, context)
    print("\nAnswer:")
    print(answer)
