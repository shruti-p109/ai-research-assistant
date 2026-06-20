#pip install sentence-transformers faiss-cpu
from ingestion.pdf_loader import (load_pdf, pdf_dir)
from ingestion.chunking import chunk_text, clean_text
from embeddings.embedder import get_embeddings
from embeddings.vector_store import VectorStore
from rag.generator import generate_answer
import os

all_chunks = []
for file in os.listdir(pdf_dir):
    print(file)
    if file.endswith('.pdf'):
        print(f'Processing file {file}')
        file_path = os.path.join(pdf_dir, file)
        text = load_pdf(file_path)
        # print('Text length:', len(text))
        text = clean_text(text)
        chunks = chunk_text(text)
        # print('No. of chunks:', len(chunks))
        chunk_id = 0
        for chunk in chunks:
            # you need to later embed chunk by chunk
            all_chunks.append(
                {
                    'id': chunk_id,
                    'source': file,
                    'text': chunk
                }
            )
            chunk_id += 1
        print('Total chunks:',len(all_chunks))
print('chunking done')
# for i,chunk in enumerate(chunks[:3]):
#     print(f'\nChunk {i}:\n{chunk[:200]}')

# Extract only texts
texts = [chunk['text'] for chunk in all_chunks]
print("Generating Embeddings")
embeddings = get_embeddings(texts)

# Initiaze vector store.
dimension = len(embeddings[0])
store = VectorStore(dimension)
store.add(embeddings, texts)
print("Embeddings stored")

# test query
query = "What evidence suggests output bias is a fundamental issue rather than a model-specific issue in the CS-Agent?"
query_embedding = get_embeddings([query])[0]
results = store.search(query_embedding)
# print("Query Results:")
# for i,res in enumerate(results):
#     print(f"Result {i+1}:")
#     print('similarity score:',res['score'])
#     print(res['text'][:500])
for i,result in enumerate(results):
    chunk_metadata = all_chunks[result['idx']]
    results[i]['source'] = chunk_metadata['source']

# build context from retrieved chunks
context = "\n\n".join(f"""
(DOCUMENT: {r['source']})
{r['text']}
""" for r in results)
print('context', context) 

# generate answer
# print(context[:2000])
answer = generate_answer(query, context)
print("\nAnswer:")
print(answer)