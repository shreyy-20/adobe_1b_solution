# adobe_1b_solution

# Persona-Driven Document Intelligence

This project, submitted for the Adobe India Hackathon 2025 (Round 1B) under the theme "Connect What Matters — For the User Who Matters," presents a **persona-aware document intelligence system**.

---

## Challenge Overview

The core objective was to develop an offline, CPU-only system that can extract and rank the most relevant sections from a collection of PDF documents. This extraction is tailored to a specific **user role (persona)** and their **job-to-be-done**, ensuring the output is highly relevant to the user's needs.

### Requirements:

* **Offline Capability:** No internet access required.
* **CPU-only Operation:** No GPU dependencies.
* **Model Size:** Model footprint ≤ 1GB.
* **Performance:** Process 3-10 PDFs in ≤ 60 seconds.
* **Output Format:** Adherence to Adobe's specified evaluation schema.

---

## Key Features

* **Semantic Ranking:** Utilizes semantic understanding to rank relevant sections and paragraphs.
* **Dynamic Personas:** Supports three predefined dynamic personas and their associated jobs: **Analyst**, **Researcher**, and **Student**.
* **Flexible Output:** Generates per-document output files and a consolidated `result.json` in the Adobe evaluation format.
* **Query-Driven Extraction:** Extracts information based on user queries, with estimations for paragraph-to-page mapping.
* **Dockerized & Stateless:** Designed for easy deployment and scoring, ensuring reproducible results.

---

## Folder Structure

```

adobe_round1b_solution/
├── app/
│ ├── utils.py
│ ├── persona_engine.py
│ └── evaluate.py
│
├── input/                                            \# Input PDFs
├── model/                                            \# Pre-downloaded model (if needed)
├── output/
│ ├── result.json                                     \# ✅ Final consolidated output (Adobe format)
│ ├── file01.json                                     \# Individual file results
│ └── ... \# More per-file outputs
│
├── extractor_runner_1b.py                            \# Main pipeline script
├── results_json.py                                   \# Consolidates result.json
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── sample_queries.json
├── sample_references.json
├── approach_explanation.md
├── README.md

````

---

## Quickstart

### Local Python (for Development)

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Place PDFs:** Put your input PDF files into the `input/` folder.

3.  **Run Extraction Pipeline:**
    ```bash
    python extractor_runner_1b.py
    ```
4.  **Generate Final Output:**
    ```bash
    python results_json.py
    ```

### Docker (Windows PowerShell)

1.  **Build the Image:**
    ```powershell
    docker build -t persona_engine .
    ```
2.  **Run the Container:**
    ```powershell
    docker run --rm `
      -v "${PWD}\input:/app/input" `
      -v "${PWD}\output:/app/output" `
      -v "${PWD}\sample_queries.json:/app/sample_queries.json" `
      persona_engine
    ```

### Docker (Linux/macOS)

1.  **Build the Image:**
    ```bash
    docker build -t persona_engine .
    ```
2.  **Run the Container:**
    ```bash
    docker run --rm \
      -v $(pwd)/input:/app/input \
      -v $(pwd)/output:/app/output \
      -v $(pwd)/sample_queries.json:/app/sample_queries.json \
      persona_engine
    ```

### Output Format (`result.json`)

The consolidated output file is located at `output/result.json` and follows this structure:

```json
{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "processing_timestamp": "..."
  },
  "extracted_sections": [
    {
      "document": "filename.pdf",
      "page_number": 4,
      "section_title": "Title or Heading",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "filename.pdf",
      "page_number": 4,
      "refined_text": "Relevant refined paragraph"
    }
  ]
}
````
## IMPORTANT

## All 10 Input PDFs and Output results are excluded due to GitHub size limits. Please use input/ and models/ folders locally as needed.
##  Models     # Contains downloaded SentenceTransformer model files
To download the model locally:

```bash
from sentence_transformers import SentenceTransformer
SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./models")
```
## output      # Will be auto-generated after running



-----

## Supported Use Cases

| Test Case         | Persona                         | Job-to-Be-Done                                            |
| :---------------- | :------------------------------ | :-------------------------------------------------------- |
| Academic Research | PhD Researcher in Comp Bio      | Literature review: methods, datasets, benchmarks          |
| Business Analysis | Investment Analyst              | Compare revenue, R\&D, and market strategies across firms |
| Education         | Undergraduate Chemistry Student | Identify key exam concepts in reaction kinetics           |

-----

## System Constraints

| Constraint                    | Status |
| :-----------------------------| :----- |
| Model size ≤ 1$GB             | ✅     |
| CPU-only                      | ✅     |
| Processing time ≤ 60 sec      | ✅     |
| Internet access disabled      | ✅     |

-----

## Submission Instructions
- Repository: https://github.com/shreyy-20/adobe_1b_solution
- Docker Build Time (First Build): ~1200 seconds
- Runtime per File: <60 seconds
- All documents processing: <50 seconds
- Model: all-MiniLM-L6-v2 (SentenceTransformers)

-----

## Technical Highlights

  * **Lightweight Model:** Employs `all-MiniLM-L6-v2` for efficient text embeddings.
  * **Vectorized Scoring:** Utilizes batched cosine similarity for rapid information retrieval.
  * **Dual Output Mode:** Provides both individual per-file results and a combined Adobe-style JSON.
  * **Dockerized Execution:** Ensures stateless, offline, and reproducible environments.

-----


## Environment Setup

This project was developed and tested using a Python virtual environment:

- **Python Version:** 3.10
- **Virtual Environment:** `venv310` (excluded from Docker and Git via `.dockerignore`)

All dependencies are listed in `requirements.txt`, and the project can be run inside Docker for a consistent environment.

## Model Usage

We use the following pre-trained sentence transformer model:

- **Model Name:** `all-MiniLM-L6-v2`
- **Library:** `sentence-transformers`
- **Purpose:** Used for embedding both queries and document paragraphs for semantic similarity search.
- **Download Strategy:** The model is downloaded once (outside the Docker build) and mounted via volume at `/app/models` to avoid slow builds.

This strategy avoids re-downloading the model during each Docker build, improving build efficiency and enabling caching for repeated use.

-----

## Authors

  * **Shreyes Mohanty**
  * **Prakash Shaw**
  * **Madhumita Parida**

Our team brings expertise in Machine Learning, Natural Language Processing, pre-sales, backend development, embedding systems, and scalable Docker deployments.

```
```

