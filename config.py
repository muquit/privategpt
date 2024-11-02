import os
import sys

# If new variables are added, do not forget to
# add it to utils/load_config.py

current_file_path = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(current_file_path)
VERSION="1.0.3"

APP_TITLE = "Private Documents Assistant"
APP_DESCRIPTION = "An on-premises private documents assistant with ollama"
PROJECT_URL = "https://github.com/muquit/privategpt"
SHOW_PROJECT_URL = True
SHOW_SIDEBAR = True
ASK_ME_TEXT = "Ask me anything about your documents"

# Custom system prompt. Please look at Custom Prompts section
# in README.md for examples
# added in v1.0.3
CUSTOM_PROMPT = """
Given the following context, answer the question using only the provided 
information. If the answer isn't found in the context, respond with
'I cannot answer this based on the provided context.'

Context:
{context}

Question: {question}

Answer: Let me analyze the context and provide a detailed response.
"""

# Change if ollama is running on a different system on 
# your network or somewhere in the cloud. Please look
# at ollama document and FAQ on how ollama can bind
# to all network interfaces.
# By default use localhost (127.0.0.1)
OLLAMA_URL = "http://127.0.0.1:11434"


# put your documents in ./documents directory
DOCUMENT_DIR = os.path.join(PROJECT_ROOT, 'documents')

# database will be created in ./db directory
PERSIST_DIRECTORY = os.path.join(PROJECT_ROOT, 'db')

CHUNK_SIZE = 500
OVERLAP = 50
TARGET_SOURCE_CHUNKS = 4
EMBEDDINGS_MODEL_NAME = "all-MiniLM-L6-v2"

# Log files, Change
LOG_FILE_INGEST = os.path.join(PROJECT_ROOT, 'docs_ingest.log')
LOG_FILE_CHAT = os.path.join(PROJECT_ROOT, 'private_gpt.log')

# default LLM  for console app. web app list the loaded models
# dynamically
DEFAULT_MODEL = "mistral"

# All the loaded models will be displayed on the sidebar. To exclude
# any model, add in the list below, for example, there is no
# reason to display an embedding model in the list for example.
#EXCLUDE_MODELS = []
EXCLUDE_MODELS = ["nomic-embed-text:latest", "qwen2:7b"]

