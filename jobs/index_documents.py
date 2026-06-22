# build index / incremental update

# logic
# load metadata
# load chunks
# load faiss

# for pdf in pdf_folder:

#     if pdf already indexed:
#         continue

#     process pdf

#     index.add(...)
#     chunks.extend(...)

#     metadata[pdf]["indexed_at"] = ...

# save
# faiss.index
# store chunks and update metadata in rag_system.db

# call chunking utility
from storage.database import (
    get_unindexed_documents,
    mark_document_indexed,
    insert_chunks
)
from ingestion.pdf_parser import extract_text
from indexing.chunking import (
    clean_text,
    chunk_text
)
from indexing.embedder import get_embeddings, get_embeddings_dimension
from indexing.vector_store import VectorStore
from storage.database import SessionLocal
from logger_setup import logger

def main():
    with SessionLocal() as session:
        documents = get_unindexed_documents(session)

    if not documents:
        logger.info("No new documents to index.")
        return
    
    vector_store = VectorStore(get_embeddings_dimension())
    
    for document in documents:
        try:
            logger.info(f"Processing new document {document.pdf_name}")
            # 1. extract text
            text = extract_text(document.file_path)
            # 2. cleaning and chunking
            cleaned_text = clean_text(text)
            chunks = chunk_text(cleaned_text)
            logger.info(f"Generated {len(chunks)} chunks.")
            # 4. generate embeddings
            embeddings = get_embeddings(chunks)

            with SessionLocal() as session:
                # 3. save chunks to db
                chunk_ids = insert_chunks(session, document.doc_id, chunks)

                # 5. save embeddings in FAISS
                vector_store.add(
                    embeddings,
                    chunk_ids
                )
                vector_store.save()

                # 6. mark document as indexed
                mark_document_indexed(session, document.doc_id)
                
                logger.info(f"Indexed {document.pdf_name}")
        except Exception as e:
            logger.error(f"Error during indexing new documents: {e}")
            
        logger.info("Indexing completed for new batch")

if __name__ == '__main__':
    main()
    
