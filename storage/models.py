from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, DateTime, Date, Text, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"

    doc_id: Mapped[int] = mapped_column(primary_key=True)
    pdf_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    source_link: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    source_name: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[date] = mapped_column(Date, nullable=False)
    indexed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # relationships
    # look inside the Chunk class. Find the attribute named "document".
    chunks: Mapped[List["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    authors: Mapped[List["Author"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    

class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.doc_id"), nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)

    # Back-reference to the parent document
    document: Mapped['Document'] = relationship(back_populates='authors')

class Chunk(Base):
    __tablename__ = 'chunks'

    chunk_id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.doc_id"), nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Back-reference to the parent document
    document: Mapped['Document'] = relationship(back_populates='chunks')

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
