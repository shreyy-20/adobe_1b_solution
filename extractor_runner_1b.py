import os
import json
import time
import torch
from concurrent.futures import ThreadPoolExecutor
from app.persona_engine import build_response
from app.evaluate import evaluate_response
from app.utils import extract_text_from_pdf, extract_text_paragraphs, get_paragraph_embeddings

class PDFProcessor:
    def __init__(self, input_dir="input", output_dir="output"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def load_queries(self, query_file="sample_queries.json"):
        with open(query_file, "r", encoding="utf-8") as f:
            query_groups = json.load(f)
        return [query for group in query_groups.values() for query in group]
    
    def process_pdf(self, pdf_name, queries, ref_dict):
        print(f"🔁 Processing: {pdf_name}")
        pdf_path = os.path.join(self.input_dir, pdf_name)
        
        
        text = extract_text_from_pdf(pdf_path)
        paragraphs = extract_text_paragraphs(text)
        
        
        with torch.cuda.amp.autocast():
            para_embeddings = get_paragraph_embeddings(paragraphs)
        
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(
                lambda q: self.process_query(q, paragraphs, para_embeddings, pdf_name, ref_dict),
                queries
            ))
        
        
        file_id = os.path.splitext(pdf_name)[0]
        output_path = os.path.join(self.output_dir, f"{file_id}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        return output_path
    
    def process_query(self, query_obj, paragraphs, para_embeddings, pdf_name, ref_dict):
        query = query_obj["query"]
        persona_hint = query_obj.get("persona_hint", "")
        
        result = build_response(query, persona_hint, paragraphs, para_embeddings)
        result.update({
            "query": query,
            "document": pdf_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        if query in ref_dict:
            scores = evaluate_response(result["response"], ref_dict[query])
            result.update(scores)
        
        return result

if __name__ == "__main__":
    start_time = time.time()
    processor = PDFProcessor()
    
    try:
        with open("sample_references.json", "r", encoding="utf-8") as f:
            references = json.load(f)
        ref_dict = {r["query"]: r["reference"] for r in references}
    except FileNotFoundError:
        ref_dict = {}
    
    queries = processor.load_queries()
    pdf_files = [f for f in os.listdir(processor.input_dir) if f.lower().endswith(".pdf")]
    print(f"🔍 Found {len(pdf_files)} PDFs to process")
    
    for pdf_name in pdf_files:
        output_path = processor.process_pdf(pdf_name, queries, ref_dict)
        print(f"✅ Saved: {output_path}")
    
    print(f"✅ All documents processed in {time.time() - start_time:.2f} seconds")