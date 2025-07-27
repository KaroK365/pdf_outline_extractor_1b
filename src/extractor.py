# src/extractor.py
import fitz  # PyMuPDF
import logging
from typing import Dict, List, Any, Optional

# Assuming utils.py and detector.py are in the same directory (src)
from utils import get_text_for_section, clean_heading_text
from detector import HeuristicDetector

logger = logging.getLogger(__name__)

def extract_sections_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts structured sections (heading, page, full_text) from a PDF.
    This is an evolution of the Round 1A logic.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logger.error(f"Failed to open or process PDF {pdf_path}: {e}")
        return []

    detector = HeuristicDetector()
    all_sections = []
    
    # We will iterate page by page to extract headings and their content
    for page_num, page in enumerate(doc):
        # Extract all text blocks with metadata
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_LIGATURES)["blocks"]
        if not blocks:
            continue
        
        # Identify potential headings on the page
        page_headings = []
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                if "spans" not in line or not line["spans"]:
                    continue
                
                # Simple heading detection logic (can be expanded with Round 1A detector)
                span = line["spans"][0]
                text = clean_heading_text("".join(s["text"] for s in line["spans"]))
                
                # A simplified heuristic: bold text or text with larger font size
                if len(text) > 3 and (("bold" in span["font"].lower()) or (span["size"] > 14)):
                    page_headings.append({
                        "text": text,
                        "page_number": page_num + 1,
                        "bbox": line["bbox"]
                    })

        # For each heading, extract its full text content
        for i, heading in enumerate(page_headings):
            next_heading_bbox = page_headings[i+1]["bbox"] if i + 1 < len(page_headings) else None
            full_text = get_text_for_section(page, heading["bbox"], next_heading_bbox)
            
            # A section needs substantial text to be useful
            if len(full_text) > 50:
                 all_sections.append({
                    "section_title": heading["text"],
                    "page_number": heading["page_number"],
                    "full_text": f"{heading['text']}\n{full_text}"
                })

    doc.close()
    return all_sections