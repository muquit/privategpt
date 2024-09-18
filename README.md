# Introduction

An on-premises ML-powered Retrieval-Augmented Generation (RAG) application. It uses [ollama](https://ollama.com) for running Large Language Models (LLM). [ollama](https://ollama.com) runs on Linux, Mac and Windows on any system with CPU or GPU and performs very well.

This project is based on ollama example code at:
https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt

Please look at ChangeLog for details for what is changed.

# Requirements

- [ollama](https://ollama.com)
- python3

# How to use

## Install ollama

- First of all you have to install [ollama](https://ollama.com) on your system.
- Then install 2 Large Language Models (LLMS), I use mistral and llama3. Here is how to install and query a model

```
ollama pull mistral
ollama pull llama3
ollama list
ollama run mistral
/bye to exit
```

This list will be dynamic in future

## Install python modules

- Create python virtual environment first. Do not install the modules globally in your system, it can break things.

```
python3 -m venv pvenv
```

- Activate modules. In Linux, Mac

```
source pvenv/bin/activate
```

- If you need to deactive virtual env

```
deactivate
```

- Install python modules. The following modulles and their dependencies will be installed in the virtual environment.

```
$ cat requirements.txt
tqdm
langchain_community
langchain_huggingface
langchain-chroma
chromadb
sentence_transformers
pymupdf
streamlit
```

To install the modules:

```
pip3 install -r ./requirement.txt
```

# Configuration file

Update `config.py` if needed:

```
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
```

# Vectorize your documents

At this time I've noticed good results with PDF _text_ and reqular text documents. The instructions will be updated when I play with other document types.

- The project comes with a free PDF book [dracula.pdf](https://www.planetebook.com/free-ebooks/dracula.pdf) in `ingest/documents` directory. I noticed that the extracted texts from the PDF version of dracula gives much better results than the free dracula.txt and time [Project Guenberg](https://www.gutenberg.org/). If you want, copy some PDF files to `./ingest/documents` directory and vectorize them. If new documents are found, they will be appended to the vector database. 

```
copy file.pdf ./ingest/documents
```

- Vectorize

```
./ingest/ingest.py
```

# Query your document

Start the web ui

```
./run_assistant_ui.sh
```

It will start a browser in your local machine. `./run_assistant_ui.sh -h` for more info

# Screenshot of the web ui

A response for a question about one of the documents. Sources show the chunks found in the similarity search in the database. The chunks are then sent to the locall LLM and the model summerized the chunks as reponse at the top.

![dracula](./screenshots/dracula.png)

## EPUB document

I played with some epub documents from https://www.gutenberg.org/ and the results seems to vary based
on the type of documents. This is a work in progress ...

The following are needed to create EMBEDDINGS for EPUB files:

- pandoc binary
- langchain_community unstructured, "unstructured[epub]" and pacdoc python
  modules

In Mac, install pacdoc and related libraries

```
brew install libxml2 libxslt pandoc
```

In linux (ubuntu/debian family):

```
sudo apt-get update
sudo apt-get install -y libxml2-dev libxslt-dev pandoc
```

Install python modules:

```
pip3 install langchain_community unstructured
pip3 install "unstructured[epub]"
pip3 install pandoc
```

Copy documents in ./documents directory at the base of the project

# License

MIT License

Copyright (c) 2024 Muhammad Muquit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

This project is adapted from https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt
