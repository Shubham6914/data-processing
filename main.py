import json
import os
from typing import List, Dict
from datetime import datetime
from tqdm import tqdm  # For progress bar

from models.data_models import MedicalArticle
from processor.text_processor import TextProcessor
from processor.embedding_generator import EmbeddingGenerator
from processor.storage_handler import QdrantHandler

class MedicalDataProcessor:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.embedding_generator = EmbeddingGenerator()
        self.storage_handler = QdrantHandler()
        
    def setup(self):
        """Initialize storage and required setup"""
        print("Initializing Qdrant collection...")
        self.storage_handler.create_collection()
        
    def process_single_file(self, file_path: str) -> bool:
        """Process a single JSON file"""
        try:
            # Read JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Validate data using Pydantic model
            article = MedicalArticle(**data)
            
            # Process text
            processed_data = self.text_processor.process_article(article)
            
            # Generate embeddings
            qdrant_data = self.embedding_generator.generate_embeddings(processed_data)
            
            # Store in Qdrant
            self.storage_handler.store_document(qdrant_data)
            
            return True
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return False

    def process_directory(self, directory_path: str, limit: int = 1000):
        """Process all JSON files in directory"""
        # Get all JSON files
        json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
        
        if limit:
            json_files = json_files[:limit]
        
        print(f"Processing {len(json_files)} files...")
        
        # Process files with progress bar
        successful = 0
        failed = 0
        
        for file in tqdm(json_files):
            file_path = os.path.join(directory_path, file)
            if self.process_single_file(file_path):
                successful += 1
            else:
                failed += 1
        
        return {
            "total": len(json_files),
            "successful": successful,
            "failed": failed
        }
   
def main():
    # Initialize processor
    processor = MedicalDataProcessor()
    
    # Setup storage
    processor.setup()
    
    # Your specific JSON files directory
    data_directory = "/home/cyberium/shubham/cancerguru-crawler/ONCOLOGY_CATEGORIES/CANCER_CATEGORIES/Breast cancer"
    
    # Verify directory exists and contains JSON files
    if not os.path.exists(data_directory):
        print(f"Error: Directory not found: {data_directory}")
        exit()
        
    json_files = [f for f in os.listdir(data_directory) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files in directory")
    
    # Process files
    print("Starting data processing...")
    results = processor.process_directory(data_directory)
    
    # Print results
    print("\nProcessing Complete!")
    print(f"Total files processed: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")

if __name__ == "__main__":
    main()
    
