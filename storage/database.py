from typing import List
from storage.models import Document, Author, Chunk
from logger_setup import logger
from sqlalchemy import create_engine, event, insert, select, update
from sqlalchemy.orm import sessionmaker
from config import DB_URL
from datetime import datetime, timezone

# database connection, foreign key explicit enforcement
engine = create_engine(DB_URL, echo=True) # echo true will print raw sql

# sqlite - turn on foreign key enforcement on connect
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# configure session factory
# autocommit false to turn off changing data on session.data, only on session.commit()
# Flush - draft, on flush sqlalchemy sends data to engine, but does not save permenantly, its held in temp draft state (allows checking for syntax errors and generate automatic ids, you can use them in code)
# flush is trigged on select() to make sure results come out to be accurate (in case you changed anything before select())
# example: select after session.add(), you will get empty if autoflush is False
# by default autoflush is True
# autosyncing by autoflush is convenient but can cause performance issues when doing heavy data processing (parsing pdfs into 100 FAISS chunks)
# commit - save on drive, you can see updates
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# called in download_papers
def bulk_insert_documents(
    session,
    documents_metdata: List[dict]
):
    # create db session
    try:
        # separate out documents table data
        documents_table_data = [
            {
                "pdf_name": item["pdf_name"],
                "file_path":item["file_path"],
                "source_link":item["source_link"],
                "source_name":item["source_name"],
                "title": item["title"],
                "published": item["published"]
            }
            for item in documents_metdata
        ]

        # bulk insert documents
        inserted_doc_ids = session.scalars(
            insert(Document).returning(Document.doc_id),
            documents_table_data
        ).all()

        # build list dicts for authors table insert
        author_dicts = []
        for index,doc_id in enumerate(inserted_doc_ids):
            authors = documents_metdata[index]['authors']
            
            for author_name in authors:
                author_dicts.append(
                    {
                        'doc_id': doc_id,
                        'author_name': author_name
                    }
                )
        
        # bulk insert authors
        if author_dicts:
            session.execute(
                insert(Author),
                author_dicts
            )

        session.commit()
        return inserted_doc_ids
    except Exception  as e:
        session.rollback()
        logger.error(f"Database error during document insertion: {e}", exc_info=True)
        raise e

# called in index_documents
def insert_chunks(
        session,
        doc_id: int,
        chunks: list
    ) -> list:
        try:
           chunks_dicts = []
           for chunk in chunks:
               chunks_dicts.append(
                   {
                       'doc_id': doc_id,
                       'chunk_text': chunk 
                   }
               )

           chunk_ids = session.scalars(
                insert(Chunk).returning(Chunk.chunk_id),
                chunks_dicts
            ).all()
           session.commit()

           return chunk_ids
        except Exception as e:
            session.rollback()
            logger.error(f"Database error during chunks insertion: {e}", exc_info=True)
            raise e

def get_unindexed_documents(session):
    try:
        select_query = select(Document.doc_id, Document.pdf_name, Document.file_path).where(Document.indexed_at == None)
        unindexed_documents = session.execute(select_query).all()
        session.commit()

        return unindexed_documents
    except Exception as e:
        session.rollback()
        logger.error(f"Database error when geting unindexed documents: {e}", exc_info=True)
        raise e

def mark_document_indexed(session, doc_id: int):
    try:
        update_query = update(Document).where(Document.doc_id == doc_id).values(
            indexed_at = datetime.now(timezone.utc)
        )
        session.execute(update_query)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error when marking document {doc_id} indexed: {e}", exc_info=True)
        raise e

def get_chunks_by_ids(session, chunk_ids: list):
    try:
        select_query = select(
            Chunk.chunk_text,
            Document.pdf_name
        ).join(
            Document,
            Chunk.doc_id == Document.doc_id
        ).where(
            Chunk.chunk_id.in_(chunk_ids)
        )
        chunk_texts = session.execute(select_query).all()
        session.commit()

        return chunk_texts
    except Exception as e:
        session.rollback()
        logger.error(f"Database error retrieving chunks by ids: {e}", exc_info=True)
        raise e   