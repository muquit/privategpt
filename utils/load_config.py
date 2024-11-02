import os
import sys
from types import SimpleNamespace

#====================================================================
# Load configuration using SimpleNamespace so that variables can be
# accessed with . notation. When new variables are introduced in
# ../config.py, update the config import and namespace.
#
# return configuration as SimpleNamespace
# muquit@muquit.com Sep-15-2024 
#====================================================================
def load_config():
    current_file_path = os.path.abspath(__file__)
    utils_dir = os.path.dirname(current_file_path)
    project_root = os.path.dirname(utils_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # import configuration variables from ../config.py
    # update this when new variables are introduced
    from config import (
        APP_TITLE,
        APP_DESCRIPTION,
        VERSION,
        DOCUMENT_DIR, 
        PERSIST_DIRECTORY, 
        PROJECT_ROOT, 
        CHUNK_SIZE, 
        OVERLAP,
        LOG_FILE_INGEST,
        LOG_FILE_CHAT,
        EMBEDDINGS_MODEL_NAME,
        TARGET_SOURCE_CHUNKS,
        OLLAMA_URL,
        PROJECT_URL,
        SHOW_PROJECT_URL,
        SHOW_SIDEBAR,
        DEFAULT_MODEL,
        EXCLUDE_MODELS,
        ASK_ME_TEXT,
        CUSTOM_PROMPT
    )

    # return configuration as a SimpleNamespace object
    return SimpleNamespace(
        APP_TITLE=APP_TITLE,
        APP_DESCRIPTION=APP_DESCRIPTION,
        VERSION=VERSION,
        DOCUMENT_DIR=DOCUMENT_DIR,
        PERSIST_DIRECTORY=PERSIST_DIRECTORY,
        PROJECT_ROOT=PROJECT_ROOT,
        CHUNK_SIZE=CHUNK_SIZE,
        OVERLAP=OVERLAP,
        LOG_FILE_INGEST=LOG_FILE_INGEST,
        LOG_FILE_CHAT=LOG_FILE_CHAT,
        EMBEDDINGS_MODEL_NAME=EMBEDDINGS_MODEL_NAME,
        TARGET_SOURCE_CHUNKS=TARGET_SOURCE_CHUNKS,
        OLLAMA_URL=OLLAMA_URL,
        PROJECT_URL=PROJECT_URL,
        SHOW_PROJECT_URL=SHOW_PROJECT_URL,
        SHOW_SIDEBAR=SHOW_SIDEBAR,
        DEFAULT_MODEL=DEFAULT_MODEL,
        EXCLUDE_MODELS=EXCLUDE_MODELS,
        ASK_ME_TEXT=ASK_ME_TEXT,
        CUSTOM_PROMPT=CUSTOM_PROMPT
    )

#====================================================================
# return the config as a dictionary
# @Deprecated use load_config() instead
# muquit@muquit.com Sep-15-2024 
#====================================================================
def load_config_dict():
    current_file_path = os.path.abspath(__file__)
    utils_dir = os.path.dirname(current_file_path)
    project_root = os.path.dirname(utils_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from config import (
        DOCUMENT_DIR, 
        PERSIST_DIRECTORY, 
        PROJECT_ROOT, 
        CHROMA_SETTINGS,
        CHUNK_SIZE, 
        OVERLAP
    )

    print("Successfully imported from configX")
    print(f"DOCUMENT_DIR: {DOCUMENT_DIR}")
    print(f"PERSIST_DIRECTORY: {PERSIST_DIRECTORY}")

    return {
        "DOCUMENT_DIR": DOCUMENT_DIR,
        "PERSIST_DIRECTORY": PERSIST_DIRECTORY,
        "PROJECT_ROOT": PROJECT_ROOT,
        "CHROMA_SETTINGS": CHROMA_SETTINGS,
        "CHUNK_SIZE": CHUNK_SIZE,
        "OVERLAP": OVERLAP
    }
