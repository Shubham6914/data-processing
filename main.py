import json
import os
from typing import List, Dict
from datetime import datetime
from tqdm import tqdm

from models.data_models import MedicalArticle
from processor.text_processor import TextProcessor
from processor.storage_handler import QdrantHandlerLangChain
from utils.logger import logger, setup_logging

class MedicalDataProcessor:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.storage_handler = QdrantHandlerLangChain()
        self.logger = logger

    def setup(self):
        """Initialize storage and required setup"""
        self.logger.info("Setting up storage handler...")
        print("Initializing Qdrant collection...")

    def process_single_file(self, file_path: str) -> bool:
        """Process a single JSON file"""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            article = MedicalArticle(**data)

            processed_data = self.text_processor.process_article(article)
            print(f"processed_data\n: {processed_data}")

            self.storage_handler.store_document(processed_data)

            self.logger.info(f"Successfully processed file: {file_path}")
            return True

        except Exception as e:
            error_msg = f"Error processing file {file_path}: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            return False

    def process_directory(self, directory_path: str, limit: int = 1000):
        """Process JSON files in directory up to the given limit with progress and logging"""

        json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
        if limit:
            json_files = json_files[:limit]

        total_files = len(json_files)
        print(f"Processing {total_files} files...")

        successful = 0
        failed = 0

        for idx, file in enumerate(json_files, start=1):
            file_path = os.path.join(directory_path, file)
            success = self.process_single_file(file_path)
            if success:
                successful += 1
            else:
                failed += 1

            remaining = total_files - idx
            status_msg = (f"Processed {idx}/{total_files} files. "
                          f"Success: {successful}, Failed: {failed}, Remaining: {remaining}")
            print(status_msg)
            self.logger.info(status_msg)

        print("\nAll files processed.")
        summary_msg = f"Total files: {total_files}, Successful: {successful}, Failed: {failed}"
        print(summary_msg)
        self.logger.info(summary_msg)

        return {
            "total": total_files,
            "successful": successful,
            "failed": failed
        }


def main():
    setup_logging()
    processor = MedicalDataProcessor()
    processor.setup()

    # TODO: Set your data directory path here
    data_directory = "/home/cyberium/shubham/cancerguru-crawler/ONCOLOGY_CATEGORIES/CANCER_CATEGORIES/Breast cancer"

    # TODO: Set limit on number of files to process
    limit = 500 

    if not os.path.exists(data_directory):
        print(f"Error: Directory not found: {data_directory}")
        logger.error(f"Directory not found: {data_directory}")
        return

    json_files = [f for f in os.listdir(data_directory) if f.endswith('.json')]
    if not json_files:
        print(f"No JSON files found in directory: {data_directory}")
        logger.error(f"No JSON files found in directory: {data_directory}")
        return

    print(f"Found {len(json_files)} JSON files in directory.")

    print("Starting data processing...")
    results = processor.process_directory(data_directory, limit=limit)

    print("\nProcessing Complete!")
    print(f"Total files processed: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")


if __name__ == "__main__":
    main()
