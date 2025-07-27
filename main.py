#!/usr/bin/env python3
import os
import sys
import json
import logging
import time
import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analyzer import SemanticAnalyzer
from extractor import extract_sections_from_pdf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main execution function for the persona-driven document intelligence task.
    """
    total_start_time = time.time()
    
    # Define input and output paths
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- 1. Read Inputs ---
    try:
        with open(input_dir / "persona.txt", "r", encoding='utf-8') as f:
            persona = f.read().strip()
        with open(input_dir / "job.txt", "r", encoding='utf-8') as f:
            job = f.read().strip()
        pdf_files = list(input_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.error("No PDF files found in /app/input.")
            sys.exit(1)
            
        logger.info(f"Found {len(pdf_files)} PDFs. Persona: '{persona}'. Job: '{job}'.")

    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}. Ensure persona.txt, job.txt, and PDFs are in /app/input.")
        sys.exit(1)

    # --- 2. Extract Sections from all PDFs ---
    all_sections = []
    for pdf_path in pdf_files:
        logger.info(f"Extracting sections from {pdf_path.name}...")
        sections = extract_sections_from_pdf(str(pdf_path))
        for section in sections:
            section['document'] = pdf_path.name # Tag each section with its source document
        all_sections.extend(sections)
        logger.info(f"Found {len(sections)} sections in {pdf_path.name}.")

    if not all_sections:
        logger.error("No sections could be extracted from any PDF documents.")
        sys.exit(1)

    # --- 3. Perform Semantic Analysis and Ranking ---
    logger.info("Initializing semantic analyzer...")
    analyzer = SemanticAnalyzer()
    ranked_sections = analyzer.rank_sections(persona, job, all_sections)

    # --- 4. Format the Final Output ---
    # Prepare metadata
    output_metadata = {
        "input_documents": [p.name for p in pdf_files],
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    # Prepare extracted sections (top 5)
    output_extracted = []
    top_sections = ranked_sections[:5]
    for i, section in enumerate(top_sections):
        output_extracted.append({
            "document": section['document'],
            "section_title": section['section_title'],
            "importance_rank": i + 1,
            "page_number": section['page_number']
        })
        
    # Prepare subsection analysis (top 5)
    output_subsection = []
    for section in top_sections:
        output_subsection.append({
            "document": section['document'],
            "refined_text": section['full_text'],
            "page_number": section['page_number']
        })

    # Assemble the final JSON object
    final_output = {
        "metadata": output_metadata,
        "extracted_sections": output_extracted,
        "subsection_analysis": output_subsection
    }

    # --- 5. Save Output ---
    output_path = output_dir / "analysis_output.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    total_time = time.time() - total_start_time
    logger.info(f"Processing complete in {total_time:.2f} seconds.")
    logger.info(f"Output saved to {output_path}")

if __name__ == '__main__':
    main()