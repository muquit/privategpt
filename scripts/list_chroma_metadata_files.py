#!/usr/bin/env python3
########################################################################
# List the file paths and names in chromadb collections in JSON
# muquit@muquit.com Sep-25-2024 
########################################################################
import chromadb
import os
import json

def get_unique_file_paths_from_chroma(persistence_directory):
    client = chromadb.PersistentClient(path=persistence_directory)
    collections = client.list_collections()

    unique_file_paths = set()

    for collection in collections:
        results = collection.get(include=['metadatas'])
        for metadata in results['metadatas']:
            if 'file_path' in metadata:
                unique_file_paths.add(metadata['file_path'])

    return list(unique_file_paths)

def process_file_paths(file_paths):
    result = []
    for file_path in file_paths:
        result.append({
            "full_path": file_path,
            "filename": os.path.basename(file_path)
        })
    return result

if __name__ == "__main__":
    # change if needed
    db_path = "./db"
    file_paths = get_unique_file_paths_from_chroma(db_path)
    output = {
        "total_unique_files": len(file_paths),
        "files": process_file_paths(file_paths)
    }

    print(json.dumps(output, indent=2))
