from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict
import numpy as np

class QdrantHandler:
    def __init__(self, collection_name: str = "medical_articles"):
        """
        Initialize Qdrant client and setup collection
        """
        self.client = QdrantClient("localhost", port=6333)
        self.collection_name = collection_name
        
    def create_collection(self, vector_size: int = 384):  # 384 is the size for 'all-MiniLM-L6-v2'
        """
        Create collection if it doesn't exist
        """
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size, 
                    distance=Distance.COSINE
                )
            )
            print(f"Collection '{self.collection_name}' created successfully")
        except Exception as e:
            print(f"Collection might already exist: {e}")

    def store_document(self, qdrant_data: Dict):
        """
        Store document vector and payload in Qdrant
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=qdrant_data['payload']['pmid'],  # Using PMID as ID
                        vector=qdrant_data['vector'],
                        payload=qdrant_data['payload']
                    )
                ]
            )
            print(f"Document {qdrant_data['payload']['pmid']} stored successfully")
        except Exception as e:
            print(f"Error storing document: {e}")

    def search_similar(self, query_vector: List[float], limit: int = 5):
        """
        Search for similar documents
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []