#!/usr/bin/env python3
#==================================================================== 
# Create chromadb vector database from document files. The code is 
# muquit@muquit.com Sep-14-2024 
#==================================================================== 
"""
The code is based on:
https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt
I updated it because I could not make the original code work as it is 
using various old langchain imports and now deprecated calls. Please look at
ChangeLog for details on what is changed.
"""
import os
import sys
import glob
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
from functools import partial

# handle future depecate warning. suppress the warning
import warnings
from transformers import logging
warnings.filterwarnings("ignore", category=FutureWarning, message=".*`clean_up_tokenization_spaces`.*")
logging.set_verbosity_error()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from langchain_community.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter

# by default chromadb sends telemetry info
# turn it off
# muquit@muquit.com Sep-15-2024 
os.environ["ANONYMIZED_TELEMETRY"] = "false"

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from utils.load_config import load_config
from utils.logging import setup_logging

INGEST_VERSION="1.0.1"

# Custom document loaders
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"]="text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc


# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}

##---- new--- starts
def extract_basic_metadata(file_path: str, conf) -> dict:
    ext = "." + file_path.rsplit(".", 1)[-1]
    stat = os.stat(file_path)
    return {
        "source": file_path,
        "document_type": ext.lower(),
        "creation_date": stat.st_mtime,
        "content_hash": str(hash(file_path + str(stat.st_mtime)))
    }

def load_single_documentX(file_path: str, conf) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext not in LOADER_MAPPING:
        raise ValueError(f"unsupported file extension '{ext}'")
    
    loader_class, loader_args = LOADER_MAPPING[ext]
    loader = loader_class(file_path, **loader_args)
    docs = loader.load()
    
    if conf.METADATA_ENABLED:
        metadata = extract_basic_metadata(file_path, conf)
        for idx, doc in enumerate(docs):
            doc.metadata.update(metadata)
            doc.metadata["chunk_index"] = idx
            
    return docs

def load_documentsX(conf, source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(partial(load_single_document, conf=conf), filtered_files)):
                results.extend(docs)
                pbar.update()

    return results

def deduplicate_chunks(texts: List[Document], conf) -> List[Document]:
    seen_hashes = set()
    unique_texts = []
    
    for text in texts:
        if len(text.page_content) < conf.MIN_CHUNK_LENGTH:
            continue
            
        content_hash = str(hash(text.page_content))
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            text.metadata["content_hash"] = content_hash
            unique_texts.append(text)
            
    return unique_texts

def process_documentsX(conf, logger, ignored_files: List[str] = []) -> List[Document]:
    source_directory = conf.DOCUMENT_DIR
    logger.info(f"loading documents from {source_directory}")
    documents = load_documents(conf, source_directory, ignored_files)
    if not documents:
        logger.info("no new documents to load")
        exit(0)
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=conf.CHUNK_SIZE,
        chunk_overlap=conf.OVERLAP,
        length_function=len,
    )
    
    texts = text_splitter.split_documents(documents)
    
    if conf.METADATA_ENABLED and conf.DEDUP_ENABLED:
        texts = deduplicate_chunks(texts, conf)
        
    logger.info(f"split into {len(texts)} chunks (max. {conf.CHUNK_SIZE} tokens each)")
    return texts
##---- new--- end



def load_single_document(file_path: str) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")

def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(load_single_document, filtered_files)):
                results.extend(docs)
                pbar.update()

    return results

def process_documents(conf, logger, ignored_files: List[str] = []) -> List[Document]:
    """
    Load documents and split in chunks
    """
    source_directory = conf.DOCUMENT_DIR
    logger.info(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        logger.info("No new documents to load")
        exit(0)
    logger.info(f"Loaded {len(documents)} new documents from {source_directory}")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=conf.CHUNK_SIZE,
                                                   chunk_overlap=conf.OVERLAP)
    texts = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(texts)} chunks of text (max. {conf.CHUNK_SIZE} tokens each)")
    return texts

#######################################################################
# The function in ollama example no longer works. so, I'm
# adding tests after loking at my directory structure.
# Have to look at chromadb code to see the correct way to 
# check.
#######################################################################
def does_vectorstore_exist(persist_directory: str) -> bool:
    if not os.path.isdir(persist_directory):
        return False
    
    if not os.path.exists(os.path.join(persist_directory, 'chroma.sqlite3')):
        return False
    
    uuid_dirs = glob.glob(os.path.join(persist_directory, '*-*-*-*-*'))
    if not uuid_dirs:
        return False
    
    required_files = ['data_level0.bin', 'header.bin', 'length.bin', 'link_lists.bin']
    for uuid_dir in uuid_dirs:
        if all(os.path.exists(os.path.join(uuid_dir, file)) for file in required_files):
            return True
    
    return False

#==================================================================== 
# Use dynamic batch size. I've seen in some old windows sytem an
# exception is thrown:
#  ValueError: Batch size 2076 exceeds maximum batch size 166
# catch the erorr and adjust the batch size
#==================================================================== 
def create_or_update_db(texts, embeddings, persist_directory, initial_batch_size=1000):
    db = None
    batch_size = initial_batch_size
    i = 0

    with tqdm(total=len(texts), desc="Processing documents") as pbar:
        while i < len(texts):
            try:
                batch = texts[i:i+batch_size]
                if db is None:
                    db = Chroma.from_documents(batch, embeddings, persist_directory=persist_directory)
                else:
                    db.add_documents(batch)
                i += len(batch)
                pbar.update(len(batch))
            except ValueError as e:
                if "Batch size" in str(e) and "exceeds maximum batch size" in str(e):
                    # extract the maximum batch size from the error message
                    max_size = int(str(e).split("maximum batch size")[-1].strip())
                    batch_size = max_size
                    # the system cannot handle large batch size, adjust
                    # muquit@muquit.com Sep-29-2024 
                    logger.info(f"Adjusting batch size to {batch_size}")
                else:
                    raise  # re-raise if it's not a batch size error
            except Exception as e:
                logger.info(f"Error processing batch: {str(e)}")
                break
    return db

def main():
    conf = load_config()
    logger = setup_logging(conf.LOG_FILE_INGEST)
    logger.info(f"Running ingest.py v{INGEST_VERSION}")
    logger.info(f"Log file: {conf.LOG_FILE_INGEST}")

    document_dir = conf.DOCUMENT_DIR
    persist_directory = conf.PERSIST_DIRECTORY
    chunk_size = conf.CHUNK_SIZE
    overlap = conf.OVERLAP

    # Use the configuration in your ingest script
    logger.debug(f"Processing documents from: {document_dir}")
    logger.debug(f"Storing results in: {persist_directory}")
    logger.debug(f"Using chunk size: {chunk_size} and overlap: {overlap}")

    document_dir = conf.DOCUMENT_DIR
    logger.debug(f"Document dir: {document_dir}")
    if not os.path.exists(document_dir):
        logger.debug(f"Creating document directory: {document_dir}")
        os.makedirs(document_dir)
    logger.debug(f"Put your document files to {document_dir}\n")
    logger.debug(f"Embeddings model name {conf.EMBEDDINGS_MODEL_NAME}")
    
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=conf.EMBEDDINGS_MODEL_NAME)

    logger.info(f"persistent directory: {conf.PERSIST_DIRECTORY}")

    if does_vectorstore_exist(conf.PERSIST_DIRECTORY):
        # Update and store locally vectorstore
        logger.info(f"Appending to existing vectorstore at {persist_directory}")

        # remove client_setting, otherwise new document appending 
        # fails
        db = Chroma(persist_directory=conf.PERSIST_DIRECTORY,
                    embedding_function=embeddings)
                    
        collection = db.get()
        texts = process_documents(conf, logger, [metadata['source'] for metadata in collection['metadatas']])
        logger.info("Creating embeddings. It May take few minutes...")
        db = create_or_update_db(texts, embeddings, conf.PERSIST_DIRECTORY, initial_batch_size=2076)
    else:
        # create and store locally vectorstore
        logger.info("Creating new vectorstore")
        texts = process_documents(conf, logger)
        logger.info("Creating embeddings. It may take few minutes...")
        db = create_or_update_db(texts, embeddings, conf.PERSIST_DIRECTORY, initial_batch_size=2076)
    # no need to call db.persist() anymore, it is the default now
    db = None

    logger.info("Ingestion complete!")
    logger.info("Now you can run ./run_assistant_ui.sh to start the web ui")
    logger.info(" ./run_assistant.ui.sh -h for more info")


if __name__ == "__main__":
    main()
