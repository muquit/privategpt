#!/usr/bin/env python3
#==================================================================== 
# Test loading an epub file. 
# created by Claude AI
# muquit@muquit.com Sep-15-2024 
#==================================================================== 
from langchain_community.document_loaders import UnstructuredEPubLoader

# Path to your EPUB file
epub_path = "ingest/documents/dracula.epub"

# Create the loader
loader = UnstructuredEPubLoader(epub_path)

# Load the document
documents = loader.load()

# Now you can work with the loaded documents
for doc in documents:
    print(doc.page_content[:100])  # Print the first 100 characters of each document
    print(doc.metadata)
    print("---")
