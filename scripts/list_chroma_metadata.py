#!/usr/bin/env python3

import chromadb

def list_chroma_metadata(persistence_directory):
    client = chromadb.PersistentClient(path=persistence_directory)
    collections = client.list_collections()
    print(f"Total number of collections: {len(collections)}")

    for collection in collections:
        print(f"\nCollection: {collection.name}")
        print(f"  Number of documents: {collection.count()}")
        results = collection.get(limit=5)
        print(f"  Sample document metadata:")
        for i, metadata in enumerate(results['metadatas'], 1):
            print(f"    Document {i}: {metadata}")

        if 'embeddings' in results and results['embeddings']:
            print(f"  Embedding dimension: {len(results['embeddings'][0])}")

if __name__ == "__main__":
    # Replace with the path to your Chroma database
    # default is ./db in config.py
    db_path = "./db"
    list_chroma_metadata(db_path)
