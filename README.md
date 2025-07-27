

# Persona-Driven Document Intelligence

An advanced semantic analysis system developed for the Adobe India Hackathon 2025. This tool intelligently extracts and ranks the most relevant sections from a collection of PDF documents based on a specific user persona and their job-to-be-done.

## Overview

This project tackles the challenge of information overload by moving beyond simple structural extraction. It acts as an intelligent document analyst, using a hybrid approach that combines **heuristic-based sectioning** with **semantic relevance ranking**. The system processes a collection of documents and a user query (persona + job) to pinpoint the exact information that matters most.

## 🚀 Quick Start

### Prerequisites

  - Git
  - Docker

### Installation & Usage

1.  **Clone the repository**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Prepare Directories**

    ```bash
    mkdir input output
    ```

3.  **Set Up Input Data**
    Place the following files inside the `input/` directory:

      - All of your PDF documents (e.g., `doc1.pdf`, `doc2.pdf`).
      - A `persona.txt` file containing the role description.
      - A `job.txt` file containing the task to be accomplished.

4.  **Run with Docker**

    **Build the container image** (This will also download the offline model)

    ```bash
    docker build -t doc-analyzer:1b .
    ```

    **Run the analysis**
    Use the command for your operating system:

    **Linux / macOS / Git Bash on Windows**

    ```bash
    docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output doc-analyzer:1b
    ```

    **Windows (Command Prompt)**

    ```bash
    docker run --rm -v "%cd%\input":/app/input -v "%cd%\output":/app/output doc-analyzer:1b
    ```

    **Windows (PowerShell)**

    ```bash
    docker run --rm -v "${pwd}\input":/app/input -v "${pwd}\output":/app/output doc-analyzer:1b
    ```

5.  **View Results**
    The output will be a single file in the `output/` directory.

    ```bash
    cat output/analysis_output.json
    ```

## 🏗️ Architecture

The system uses a modular, two-stage pipeline:

```
├── src/
│   ├── extractor.py        # Heuristic section extraction
│   ├── analyzer.py         # Semantic relevance ranking engine
│   ├── utils.py            # Text processing utilities
│   ├── ...                 # Other heuristic modules
├── main.py                 # Application entry point
├── Dockerfile              # Containerization with offline model
└── requirements.txt        # Dependencies
```

## 🎯 Technical Approach

The solution employs a powerful hybrid strategy to achieve accurate, context-aware results.

### 1\. Heuristic Section Extraction

First, the system leverages the robust heuristic engine from Round 1A. It processes each PDF to identify and extract logical content blocks (a heading and its subsequent text). This breaks down unstructured PDFs into a list of meaningful, self-contained sections.

### 2\. Semantic Relevance Ranking

Next, the core intelligence layer takes over:

  - **Query Formulation**: The `persona` and `job` descriptions are combined into a single, comprehensive query.
  - **Vector Embeddings**: Using a pre-trained `sentence-transformers` model, both the query and the text of each extracted section are converted into numerical vectors (embeddings) that capture their semantic meaning.
  - **Similarity Scoring**: The system calculates the **cosine similarity** between the query vector and each section vector. This score represents how relevant the section's content is to the user's task.
  - **Ranking**: Sections from all documents are ranked based on their similarity score, and the top results are presented to the user.

## 📊 Output Format

The system generates a single JSON file containing the complete analysis.

```json
{
    "metadata": {
        "input_documents": ["doc1.pdf", "doc2.pdf"],
        "persona": "Travel Planner",
        "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
        "processing_timestamp": "2025-07-27T17:22:47.12345Z"
    },
    "extracted_sections": [
        {
            "document": "South of France - Things to Do.pdf",
            "section_title": "Coastal Adventures",
            "importance_rank": 1,
            "page_number": 2
        }
    ],
    "subsection_analysis": [
        {
            "document": "South of France - Things to Do.pdf",
            "refined_text": "The South of France is renowned for its beautiful coastline...",
            "page_number": 2
        }
    ]
}
```

## 🎨 Design Decisions

### Why a Hybrid Approach?

I chose a hybrid model to leverage the strengths of both heuristics and semantic analysis:

  - **Structure from Heuristics**: Rule-based methods are fast and effective at identifying the logical structure and boundaries of sections within a PDF.
  - **Meaning from Semantics**: NLP models (sentence transformers) are unparalleled at understanding the context and meaning of text, enabling accurate relevance ranking.
  - **Combined Power**: By first using heuristics to create clean sections and then using semantic analysis to rank them, the system achieves highly accurate and context-aware results that neither method could achieve alone.

## 🛠️ Technical Stack

  - **Semantic Analysis**: `sentence-transformers` (with PyTorch backend)
  - **PDF Processing**: `PyMuPDF` for fast and reliable document parsing
  - **Containerization**: `Docker` for a portable, self-contained, and reproducible environment

## 📋 Requirements

  - Python 3.9+
  - Docker (highly recommended)
  - Dependencies listed in `requirements.txt` (PyMuPDF, sentence-transformers, etc.)

## 🔍 Troubleshooting

**Error during `docker run`?**

  - Ensure Docker Desktop is running.
  - Verify you are using the correct command for your OS (CMD vs. PowerShell vs. Linux).

**No output file generated?**

  - Confirm that `persona.txt`, `job.txt`, and at least one PDF exist in the `input` directory before running the container.
  - Check the container logs for any error messages.

-----

*This project demonstrates a powerful, modern approach to document intelligence, providing users with precisely the information they need from large collections of documents.*