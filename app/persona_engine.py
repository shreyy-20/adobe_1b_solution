from app.utils import extract_text_from_pdf, extract_text_paragraphs, semantic_search, detect_persona

from typing import List, Tuple

def build_response(query: str, persona_hint: str, paragraphs: List[str], para_embeddings) -> dict:
    persona = detect_persona(persona_hint)
    matches = semantic_search(query, paragraphs, para_embeddings)

    response = matches[0][1] if matches else "No relevant section found."
    return {
        "persona": persona,
        "relevant_sections": [para for _, para in matches],
        "response": response,
        "confidence_scores": [round(score, 3) for score, _ in matches],
        "top_score": round(matches[0][0], 3) if matches else None,
        "reasoning": f"Used transformer embeddings to match query with document sections for persona '{persona}'"
    }
