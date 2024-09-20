import os
import sys

# If new variables are added, do not forget to
# add it to utils/load_config.py

current_file_path = os.path.abspath(__file__)
VERSION="1.0.2"

# Change if ollama is running on a different system on 
# your network or somewhere in the cloud. Please look
# at ollama document and FAQ on how ollama can bind
# to all network interfaces.
# By default use localhost (127.0.0.1)
OLLAMA_URL = "http://127.0.0.1:11434"

PROJECT_ROOT = os.path.dirname(current_file_path)
PROJECT_URL = "https://muquit.com/muquit/software/software.html"
# Set it to False if you do not want to display the project
# URL in web app
SHOW_PROJECT_URL = True
# If you installed various LLMs, a specific model can be picked from 
# sidebar
SHOW_SIDEBAR = True
DOCUMENT_DIR = os.path.join(PROJECT_ROOT, 'ingest/documents')
PERSIST_DIRECTORY = os.path.join(PROJECT_ROOT, 'assistant/db')
CHUNK_SIZE = 500
OVERLAP = 50
TARGET_SOURCE_CHUNKS = 4
EMBEDDINGS_MODEL_NAME = "all-MiniLM-L6-v2"
LOG_FILE_INGEST = "/tmp/docs_ingest.log"
LOG_FILE_CHAT = "/tmp/private_gpt.log"

# LLM models
LLM_MODELS = ["mistral", "llama3", "qwen2:7b"]
