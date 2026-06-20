from ..config import DB_URL
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, DateTime, Date, event, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

# base declaration and models
class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"

    doc_id: Mapped[int] = mapped_column(primary_key=True)
    pdf_name: Mapped[str] = mapped_column(Text, unique=True)
    title: Mapped[str] = mapped_column(Text)
    published: Mapped[date] = mapped_column(Date)
    indexed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # relationships
    # look inside the Chunk class. Find the attribute named "document".
    chunks: Mapped[List["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    authors: Mapped[List["Author"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    

class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.doc_id"))
    author_name: Mapped[str] = mapped_column(Text)

    # Back-reference to the parent document
    document: Mapped['Document'] = relationship(back_populates='authors')

class Chunk(Base):
    __tablename__ = 'chunks'

    chunk_id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.doc_id"))
    chunk_text: Mapped[str] = mapped_column(Text)

    # Back-reference to the parent document
    document: Mapped['Document'] = relationship(back_populates='chunks')
    

# database connection, foreign key explicit enforcement
engine = create_engine(DB_URL, echo=True) # echo true will print raw sql
# sqlite - turn on foreign key enforcement on connect
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# db initialization, session
Base.metadata.create_all(engine)
# configure session factory
# autocommit false to turn off changing data on session.data, only on session.commit()
# Flush - draft, on flush sqlalchemy sends data to engine, but does not save permenantly, its held in temp draft state (allows checking for syntax errors and generate automatic ids, you can use them in code)
# flush is trigged on select() to make sure results come out to be accurate (in case you changed anything before select())
# example: select after session.add(), you will get empty if autoflush is False
# by default autoflush is True
# autosyncing by autoflush is convenient but can cause performance issues when doing heavy data processing (parsing pdfs into 100 FAISS chunks)
# commit - save on drive, you can see updates
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) 

# testing sample insertion
# if __name__ == '__main__':
#     print("Testing db insertion")

#     with SessionLocal() as session:
#         new_doc = Document(
#             pdf_name="test document",
#             title="Test Document",
#             published=date(2026, 6, 12),
#             chunks=[
#                 Chunk(chunk_text="sample chunk 1"),
#                 Chunk(chunk_text="sample chunk 2")
#             ],
#             authors=[
#                 Author(author_name="author 1"),
#                 Author(author_name="author 2")
#             ]
#         )

#         session.add(new_doc) # added in python memory
#         session.commit() # save in db
#         print('added sample doc, chunks and authors successfully')

#     # test foreign_key enforcement
#     print("testing foreign key enforcement")
#     with SessionLocal() as session:
#         # try to add orphaned chunk
#         orphaned_chunk = Chunk(doc_id=99, chunk_text="doesnt matter")
#         session.add(orphaned_chunk)

#         try:
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             print('foreign key constraint working')
