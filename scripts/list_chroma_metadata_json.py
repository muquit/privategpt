#!/usr/bin/env python3
#====================================================================
# dump chroma db metadata in pure json
# muquit@muquit.com Sep-25-2024 
# - show all documents, group chunks by soruce file, so new
# meta data fields (document_type, creation_date, chunk_index, content_hash),
# add a toltal chunk count.
# muquit@muquit.com Nov-10-2024 
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
            "documents": []
        }
        
        # get all documents instead of just 5
        results = collection.get()
        
        # add source file grouping
        files = {}
        for i, doc_metadata in enumerate(results['metadatas']):
            source = doc_metadata.get('source', 'unknown')
            if source not in files:
                files[source] = []
            files[source].append({
                "chunk_index": doc_metadata.get('chunk_index'),
                "metadata": doc_metadata
            })
            
        collection_data["files"] = files
        collection_data["total_chunks"] = len(results['metadatas'])
        
        if 'embeddings' in results and results['embeddings']:
            collection_data["embedding_dimension"] = len(results['embeddings'][0])
            
        metadata["collections"].append(collection_data)
    
    return metadata

if __name__ == "__main__":
    db_path = "./db"
    metadata = get_chroma_metadata(db_path)
    print(json.dumps(metadata, indent=2))
