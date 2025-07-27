import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)

class SemanticAnalyzer:
    """
    Handles the semantic analysis of document sections based on a query.
    """
    def __init__(self, model_path: str = '/app/models/all-MiniLM-L6-v2'):
        """
        Initializes the analyzer with a pre-trained sentence transformer model.
        The model is loaded from a local path within the Docker container.
        """
        try:
            self.model = SentenceTransformer(model_path)
            logger.info(f"SentenceTransformer model loaded successfully from {model_path}.")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model from {model_path}: {e}")
            raise

    def rank_sections(self, persona: str, job: str, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranks document sections based on their relevance to the persona and job.

        Args:
            persona: The user persona description.
            job: The job-to-be-done description.
            sections: A list of sections, where each must have a 'full_text' key.

        Returns:
            A list of sections sorted by relevance, with an added 'importance_score'.
        """
        if not sections:
            return []

        # Combine persona and job for a comprehensive query
        query = f"Persona: {persona}. Task: {job}"
        logger.info(f"Generating embeddings for query: {query}")
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        section_texts = [section.get('full_text', '') for section in sections]
        logger.info(f"Generating embeddings for {len(section_texts)} document sections.")
        section_embeddings = self.model.encode(section_texts, convert_to_tensor=True)

        # Calculate cosine similarity between the query and all sections
        similarities = util.cos_sim(query_embedding, section_embeddings)[0].cpu().tolist()

        # Add the score to each section dictionary
        for i, section in enumerate(sections):
            section['importance_score'] = similarities[i]

        # Sort sections by the new importance score in descending order
        ranked_sections = sorted(sections, key=lambda x: x['importance_score'], reverse=True)
        logger.info(f"Successfully ranked {len(ranked_sections)} sections.")
        
        return ranked_sections