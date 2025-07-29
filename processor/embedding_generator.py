from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize with a specific model
        Default: all-MiniLM-L6-v2 (good balance of speed and accuracy)
        """
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def generate_embeddings(self, processed_data: Dict) -> Dict:
        """
        Generate embeddings from processed text data
        """
        # Combine processed text with medical terms for better context
        text_to_embed = f"{processed_data['processed_text']} {' '.join(processed_data['medical_terms'])}"
        
        # Generate embedding
        embeddings = self.model.embed_query(text_to_embed)

        # Prepare data for Qdrant storage
        qdrant_data = {
            "vector": embeddings,
            "payload": {
                "pmid": processed_data["pmid"],
                "title": processed_data["title"],
                "abstract": processed_data["abstract"],
                "medical_terms": processed_data["medical_terms"],
                "year": processed_data["publication_year"],
                "journal": processed_data["journal"]
            }
        }
        
        return qdrant_data