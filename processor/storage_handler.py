from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.schema import Document  # Used for storing payloads in vector store
from qdrant_client.models import VectorParams, Distance
from utils.logger import logger
class QdrantHandlerLangChain:
    def __init__(self, collection_name: str = "medical_articles", model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.collection_name = collection_name
        self.client = QdrantClient("localhost", port=6333)
        
        # Initialize LangChain embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        
        # Default vector size for embeddings, can be adjusted based on model
        vector_size = 384

        # Create collection if not exists, set vector size from embeddings
        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"Collection '{self.collection_name}' created.")
        else:
            print(f"Collection '{self.collection_name}' already exists.")
            
        # Initialize LangChain QdrantVectorStore wrapper
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings
        )
    def store_document(self, processed_data: dict):
        """
        Store a document in the vector store.
        processed_data: dict containing processed text and metadata.
        """
        if 'processed_text' not in processed_data:
            print(f"processed_text is \n{processed_data.get('processed_text', '')}")
            raise ValueError("'processed_text' is missing from input data")

        # Combine title, abstract, processed text and medical terms for embedding
        text_to_embed = " ".join([
            processed_data["processed_text"],
            " ".join(processed_data["medical_terms"])
        ])

        doc = Document(
            page_content=text_to_embed,
            metadata={
                "pmid": processed_data["pmid"],
                "title": processed_data["title"],
                "abstract": processed_data["abstract"],
                "medical_terms": processed_data["medical_terms"],
                "year": processed_data["publication_year"],
                "journal": processed_data["journal"]
            }
    )

        self.vector_store.add_documents([doc])
        logger.info("Document stored successfully in Qdrant.")
        print("Document stored successfully in Qdrant.")
    def search_similar(self, query_text: str, limit: int = 5):
        """
        Search similar documents given a query string.
        Returns list of Document with similarity scores.
        """
        results = self.vector_store.similarity_search(query_text, k=limit)
        return results
