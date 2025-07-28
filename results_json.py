import os
import json
from datetime import datetime

# === PATHS ===
output_dir = "output"
sample_query_path = "sample_queries.json"
final_output_path = os.path.join(output_dir, "result.json")

# === Mappings for persona and job ===
persona_job_map = {
    "business_analysis_sample_queries": {
        "persona": "Investment Analyst",
        "job_to_be_done": "Analyze revenue trends, R&D investments, and market positioning strategies."
    },
    "academic_research_sample_queries": {
        "persona": "PhD Researcher in Computational Biology",
        "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks."
    },
    "educational_content_sample_queries": {
        "persona": "Undergraduate Chemistry Student",
        "job_to_be_done": "Identify key concepts and mechanisms for exam preparation on reaction kinetics."
    }
}

# === Load sample_queries to map queries to their persona group ===
with open(sample_query_path, "r", encoding="utf-8") as f:
    query_groups = json.load(f)

query_to_group = {}
for group_name, queries in query_groups.items():
    for q in queries:
        query_to_group[q["query"]] = group_name

# === Collect data from all individual output files ===
section_candidates = []
documents = []

for filename in os.listdir(output_dir):
    if not filename.endswith(".json") or filename == "result.json":
        continue

    filepath = os.path.join(output_dir, filename)
    documents.append(filename)

    with open(filepath, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for result in entries:
        query = result["query"]
        response = result["response"]
        score = result.get("top_score", 0.0)
        document = result["document"]
        refined_text = response

        # Compute page_number by matching response in relevant_sections
        relevant_texts = result.get("relevant_sections", [])
        try:
            para_index = relevant_texts.index(response)
            page_number = (para_index // 10) + 1
        except (ValueError, IndexError, TypeError):
            page_number = 1

        section_title = f"Relevant to: {query[:40]}..."

        section_candidates.append({
            "query": query,
            "document": document,
            "section_title": section_title,
            "refined_text": refined_text,
            "page_number": page_number,
            "score": score
        })

# === Determine persona & job from any query used ===
if section_candidates:
    sample_query = section_candidates[0]["query"]
    group_key = query_to_group.get(sample_query)
    persona = persona_job_map.get(group_key, {}).get("persona", "Unknown")
    job = persona_job_map.get(group_key, {}).get("job_to_be_done", "Unknown task")
else:
    persona = "Unknown"
    job = "Unknown task"

# === Final Output JSON ===
final_result = {
    "metadata": {
        "input_documents": sorted(documents),
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [],
    "subsection_analysis": []
}

# === Rank and Populate Sections ===
section_candidates = sorted(section_candidates, key=lambda x: x["score"], reverse=True)

for rank, sec in enumerate(section_candidates[:30], start=1):
    final_result["extracted_sections"].append({
        "document": sec["document"],
        "section_title": sec["section_title"],
        "importance_rank": rank,
        "page_number": sec["page_number"]
    })
    final_result["subsection_analysis"].append({
        "document": sec["document"],
        "refined_text": sec["refined_text"],
        "page_number": sec["page_number"]
    })

# === Write result.json ===
with open(final_output_path, "w", encoding="utf-8") as f:
    json.dump(final_result, f, indent=2, ensure_ascii=False)

print(f"✅ Combined result written to: {final_output_path}")
