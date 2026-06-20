from sqlalchemy import create_engine
from datetime import date, datetime
from typing import List
from repo.storage.models import SessionLocal, Document, Author, Chunk
from logger_setup import logger
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, declarative_base, sessionmaker, event, insert
from config import DB_URL

# database connection, foreign key explicit enforcement
engine = create_engine(DB_URL, echo=True) # echo true will print raw sql

# sqlite - turn on foreign key enforcement on connect
@event.listens_for(Engine, "connect")
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
Base = declarative_base() 

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
                "title": item["title"],
                "published": item["published"]
            }
            for item in documents_metdata
        ]

        # bulk inser documents
        result = session.scalars(
            insert(Document).returning(Document.doc_id),
            documents_table_data
        )

        # convert result into list
        inserted_doc_ids  = list(result)

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
        logger.error(f"Database error occurred during document insertion: {e}", exc_info=True)
        raise e

# called in index_documents
def insert_chunks(
        session,
        doc_id: int,
        chunk_text:str
    ) -> int:
        try:
            new_chunk = Chunk(
                doc_id=doc_id,
                chunk_text=chunk_text
            )

            session.add(new_chunk)
            session.commit()

            return new_chunk.chunk_id
        except Exception as e:
            session.rollback()
            logger.error(f"Database error occurred during chunk insertion: {e}", exc_info=True)
            raise e

