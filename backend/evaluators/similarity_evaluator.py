import logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

class SimilarityEvaluator:

    def __init__(self):
        logger.info("Loading sentence transformer model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Sentence transformer loaded.")

    def score(self, expected: str, generated: str) -> float:
        try:
            if not expected.strip() or not generated.strip():
                return 0.0

            embeddings = self.model.encode([expected.strip(), generated.strip()])
            score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return round(float(score), 4)

        except Exception as e:
            logger.error(f"Similarity scoring failed: {e}")
            return 0.0

    def is_hallucination(self, expected: str, generated: str, threshold: float = 0.4) -> bool:
        score = self.score(expected, generated)
        return score < threshold

    def batch_score(self, pairs: list) -> list:
        """
        pairs: list of (expected, generated) tuples
        returns: list of float scores
        """
        results = []
        for expected, generated in pairs:
            results.append(self.score(expected, generated))
        return results