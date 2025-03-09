# ingestion/process_files.py

import os
import json
from tika import parser
from bs4 import BeautifulSoup
import requests
from prometheus_client import Counter
from utils import extract_keywords

# Prometheus metric: count of processed files
FILES_PROCESSED = Counter('files_processed_total', 'Total number of files processed')

def process_all_files(uploads_dir="uploads", processed_dir="processed"):
    data_collection = {}
    if not os.path.exists(uploads_dir):
        return {"error": f"Directory '{uploads_dir}' does not exist."}
    
    for file_name in os.listdir(uploads_dir):
        file_path = os.path.join(uploads_dir, file_name)
        # Skip the metadata file (used to store file descriptions)
        if file_name == "metadata.json":
            continue
        print(f"Processing: {file_name}")
        extracted_text = ""
        try:
            if file_name.lower().endswith(".pdf"):
                raw = parser.from_file(file_path)
                extracted_text = raw.get("content", "").strip()
            elif file_name.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    extracted_text = f.read()
            elif file_name.lower().startswith("http"):
                response = requests.get(file_name)
                soup = BeautifulSoup(response.content, "html.parser")
                extracted_text = soup.get_text(separator="\n")
            else:
                print(f"Unsupported file type: {file_name}")
                continue
            
            keywords = extract_keywords(extracted_text)
            data_collection[file_name] = {
                "text": extracted_text,
                "keywords": keywords
            }
            # Save processed text for review
            if not os.path.exists(processed_dir):
                os.makedirs(processed_dir)
            base_name = os.path.splitext(file_name)[0]
            output_file = os.path.join(processed_dir, f"{base_name}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"Saved processed text to: {output_file}")
            FILES_PROCESSED.inc()
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    
    # Save a summary JSON file
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data_collection, f, ensure_ascii=False, indent=4)
    print("Data ingestion complete. Processed files:", list(data_collection.keys()))
    return data_collection
