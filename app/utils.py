import os
import fitz  
import torch
import re
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict
torch.set_num_threads(2)  
import warnings
warnings.filterwarnings("ignore", message=".*numpy.*")

model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder="/app/models")

def extract_text_from_pdf(pdf_path):
    """
    Extract raw text from a PDF file using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text("text") for page in doc)

def extract_text_paragraphs(text, max_length=300, max_paragraphs=200):
    
    sentences = re.split(r'(?<=[.?!])\s+', text)
    paragraphs, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_length:
            current += " " + sentence
        else:
            paragraphs.append(current.strip())
            current = sentence
        if len(paragraphs) >= max_paragraphs:
            break

    if current and len(paragraphs) < max_paragraphs:
        paragraphs.append(current.strip())

    return paragraphs or []

def get_paragraph_embeddings(paragraphs, batch_size=32):
    if not paragraphs:
        return torch.empty((0, model.get_sentence_embedding_dimension()))
    
    
    torch.cuda.empty_cache()
    with torch.no_grad():
        return model.encode(paragraphs, batch_size=batch_size, 
                          show_progress_bar=False, 
                          convert_to_tensor=True)

def semantic_search(query, paragraphs, para_embeddings=None, top_k=5):
    """
    Perform semantic search using precomputed paragraph embeddings.
    """
    query_embedding = model.encode(query, convert_to_tensor=True)

    if para_embeddings is None:
        para_embeddings = get_paragraph_embeddings(paragraphs)

    actual_k = min(top_k, para_embeddings.shape[0])
    hits = util.semantic_search(query_embedding, para_embeddings, top_k=actual_k)[0]

    return [(float(hit['score']), paragraphs[hit['corpus_id']]) for hit in hits]

def detect_persona(query):
    """
    Very basic rule-based persona classification.
    """
    query_lower = query.lower()
    if any(word in query_lower for word in ["you", "your", "i", "me", "my"]):
        return "user-centric"
    elif any(word in query_lower for word in ["team", "business", "organization", "company"]):
        return "business"
    elif any(word in query_lower for word in ["developer", "code", "software", "app"]):
        return "technical"
    elif any(word in query_lower for word in ["legal", "law", "compliance", "regulation"]):
        return "legal"
    elif any(word in query_lower for word in ["summary", "overview", "document", "report"]):
        return "general"
    else:
        return "general"
