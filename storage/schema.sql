CREATE TABLE documents IF NOT EXISTS (
    doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pdf_name TEXT UNIQUE,
    file_path TEXT UNIQUE,
    source_link TEXT UNIQUE,
    source_name TEXT,
    title TEXT,
    published DATE,
    indexed_at TIMESTAMP
);

CREATE TABLE chunks IF NOT EXISTS (
    chunk_id INTEGER PRIMARY KEY AUTOINCREMENT, -- maps to faiss embedding id
    doc_id INTEGER,
    chunk_text TEXT,
    FOREIGN KEY (doc_id) REFERENCE documents (doc_id)
);

CREATE TABLE authors IF NOT EXISTS (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    doc_id INTEGER,
    author_name TEXT,
    FOREIGN KEY (doc_id) REFERENCE documents (doc_id)
);