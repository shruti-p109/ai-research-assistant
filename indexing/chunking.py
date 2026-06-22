# import nltk
# nltk.download("punkt")
# nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize
import re

# Text chunking is the process of splitting large documents into smaller, manageable segments
# (chunks) to help AI models like LLMs process text efficiently.

# Overlap is the technique of repeating a small amount of text from the end of one chunk
# at the beginning of the next to maintain contextual continuity
def clean_text(text:str) -> str:
    # print('inside clean_text')
    # normalize spaces
    text = re.sub(r"\s+", " ", text)
    # Remove things like: Refrences, Acknowledgements/Acknowledgments, Corresponding author information, Affiliations, Addresses, Copyright notices
    if "Acknowledgements" in text:
        # print('Acknowledgements found, removing everything after that')
        text = text.split("Acknowledgements")[0]
    if "References" in text:
        # print('References found, removing everything after that')
        text = text.split("References")[0]
    if "REFERENCES" in text:
        # print('REFERENCES found, removing everything after that')
        text = text.split("REFERENCES")[0]
    # remove tagline Author Manuscript
    text = re.sub(r'Author Manuscript\s*', '', text, flags=re.IGNORECASE)
    return text

def chunk_text(text:str, max_chunk_chars=1000) -> list:
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks