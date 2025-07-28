# Approach Explanation – Adobe Hackathon Round 1B  
## Theme: Connect What Matters — For the User Who Matters

---

### 🔍 Problem Overview

This challenge involved developing a **persona-driven document intelligence system** that identifies and ranks the most relevant sections from a variety of documents — such as research papers, corporate financial reports, or educational textbooks — based on a user's specific role and task (the "job-to-be-done").

The system needed to handle:
- Multiple document types (PDFs)
- Multiple personas (e.g., Analyst, Researcher, Student)
- Strict execution constraints (CPU-only, <1GB model, <60s runtime)

---

### ⚙️ System Architecture Overview

We designed a **modular semantic retrieval pipeline**, capable of generating both:
- Individual outputs per input PDF (for traceability), and
- A consolidated `result.json` output that conforms to Adobe’s grounded format.

The pipeline is fully Dockerized, CPU-optimized, and robust to scale across document collections.

---

### 🧠 Key Pipeline Components

#### 1. **PDF Preprocessing & Chunking**
- All PDFs are parsed into clean, page-aware paragraphs using `PyMuPDF`.
- Paragraphs are stored along with pseudo-page mappings based on index heuristics.

#### 2. **Persona & Query Inference**
- The system loads **`sample_queries.json`**, containing grouped queries by domain:
  - `business_analysis_sample_queries` → *Investment Analyst*
  - `academic_research_sample_queries` → *PhD Researcher in Computational Biology*
  - `educational_content_sample_queries` → *Undergraduate Chemistry Student*
- The appropriate **persona and job-to-be-done** are automatically inferred by mapping each query to its originating group.

#### 3. **Lightweight Transformer Embedding**
- Uses `all-MiniLM-L6-v2` from `sentence-transformers` (≈90MB, CPU-friendly).
- Paragraphs and queries are embedded in the same vector space.

#### 4. **Batched Semantic Similarity Scoring**
- Cosine similarity is computed between each paragraph and query embedding.
- Top-matching sections are scored, ranked, and selected globally (across all documents).
- These are reported in `extracted_sections`, with metadata like:
  - `document`, `section_title`, `importance_rank`, `page_number`

#### 5. **Subsection-Level Refinement**
- The top semantic match (refined text) per section is saved in `subsection_analysis`.
- Page numbers are heuristically estimated from paragraph index.
- Outputs are structured and written to:
  - `output/<file_name>.json` (per file)
  - `output/result.json` (final combined output in Adobe format)

---

### 🚀 Optimization & Design Constraints

- ✅ **Model size < 100MB**, runs fully on CPU
- ✅ **Processing time < 60 seconds** for 3–5 input PDFs
- ✅ Batch processing of embeddings for speed
- ✅ Stateless execution via Docker, no internet required
- ✅ Works with diverse documents without manual tuning

---

### 💡 Generalization Strength

- Queries and personas are abstracted and data-driven — allowing simple reusability for new domains
- Works equally well for business reports, academic papers, and educational textbooks
- Fully modular: query config, model, and scoring logic can all be independently extended

---

### ✅ Outcome

Our system produces:
- 🔹 Per-document JSON outputs for explainability
- 🔹 A consolidated, persona-aware `result.json` for Adobe scoring
- 🔹 Ranked `extracted_sections` and `subsection_analysis` tailored to each persona’s job

This ensures we not only extract **what matters in the document**, but also **deliver it in a form that truly matters to the user**.

