#!/usr/bin/env python3
#====================================================================
# dump chroma db metadata in pure json
# muquit@muquit.com Sep-25-2024 
#====================================================================
import chromadb
import json

def get_chroma_metadata(persistence_directory):
    client = chromadb.PersistentClient(path=persistence_directory)
    collections = client.list_collections()

    metadata = {
        "total_collections": len(collections),
        "collections": []
    }

    for collection in collections:
        collection_data = {
            "name": collection.name,
            "document_count": collection.count(),
            "sample_documents": []
        }

        results = collection.get(limit=5)
        for i, doc_metadata in enumerate(results['metadatas'], 1):
            collection_data["sample_documents"].append({
                "document_id": i,
                "metadata": doc_metadata
            })

        if 'embeddings' in results and results['embeddings']:
            collection_data["embedding_dimension"] = len(results['embeddings'][0])

        metadata["collections"].append(collection_data)

    return metadata

if __name__ == "__main__":
    db_path = "./db"
    metadata = get_chroma_metadata(db_path)
    print(json.dumps(metadata, indent=2))
