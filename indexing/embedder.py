# get_embeddings()
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

# lightweight + good enough
model = SentenceTransformer(EMBEDDING_MODEL)

def get_embeddings(text):
    # SentenceTransformer.encode() can accept either a single string OR a list of strings
    return model.encode(text)

def get_embeddings_dimension():
    return model.get_embedding_dimension()
