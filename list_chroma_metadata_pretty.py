#!/usr/bin/env
#====================================================================
# requires 'pip install rich'
# muquit@muquit.com Sep-25-2024 
#====================================================================
import chromadb
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def list_chroma_metadata(persistence_directory):
    client = chromadb.PersistentClient(path=persistence_directory)
    collections = client.list_collections()
    console = Console()

    console.print(Panel(f"[bold cyan]Total number of collections: {len(collections)}[/bold cyan]"))

    for collection in collections:
        table = Table(title=f"Collection: {collection.name}")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Number of documents", str(collection.count()))

        results = collection.get(limit=5)
        for i, metadata in enumerate(results['metadatas'], 1):
            table.add_row(f"Document {i} metadata", str(metadata))

        if 'embeddings' in results and results['embeddings']:
            table.add_row("Embedding dimension", str(len(results['embeddings'][0])))

        console.print(Panel(table))

if __name__ == "__main__":
    db_path = "./db"
    list_chroma_metadata(db_path)
