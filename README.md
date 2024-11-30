## Page Contents
- [Introduction](#introduction)
- [Background and Motivation](#background-and-motivation)
- [How it works](#how-it-works)
- [Contributing](#contributing)
- [Version](#version)
- [Supported Platforms](#supported-platforms)
- [Requirements (ollama and python3)](#requirements-ollama-and-python3)
  - [Python Version](#python-version)
- [Installation](#installation)
  - [Clone the  repo](#clone-the--repo)
  - [Install ollama](#install-ollama)
  - [Install python modules](#install-python-modules)
  - [Python Version](#python-version-1)
    - [Create Python Virtual Environment](#create-python-virtual-environment)
    - [Linux/MacOS](#linuxmacos)
    - [Windows](#windows)
    - [Install the Python Modules](#install-the-python-modules)
- [Contains exact versions that are known to work together](#contains-exact-versions-that-are-known-to-work-together)
- [Test environment: Python 3.12](#test-environment-python-312)
- [If you want to try the latest versions (may introduce compatibility ](#if-you-want-to-try-the-latest-versions-may-introduce-compatibility-)
- [issues):](#issues)
- [1. pip install -r requirements.txt --upgrade](#1-pip-install--r-requirementstxt---upgrade)
- [2. If it works: Please create an issue with your versions (run:](#2-if-it-works-please-create-an-issue-with-your-versions-run)
- [./scripts/check_versions.py)](#scriptscheck_versionspy)
- [3. If it breaks: Fall back to pinned versions, do the follwing:](#3-if-it-breaks-fall-back-to-pinned-versions-do-the-follwing)
- [deactive](#deactive)
- [rm -rf pvenv](#rm--rf-pvenv)
- [python3 -m venv pvenv](#python3--m-venv-pvenv)
- [source pvenv/bin/activate](#source-pvenvbinactivate)
- [pip install -r requirements_pinned.txt](#pip-install--r-requirements_pinnedtxt)
- [Generated with: ./scripts/check_versions.py](#generated-with-scriptscheck_versionspy)
- [Last verified: Nov-29-2024](#last-verified-nov-29-2024)
  - [Common Issues](#common-issues)
  - [Troubleshotting](#troubleshotting)
- [Configuration file](#configuration-file)
- [Vectorize your documents](#vectorize-your-documents)
  - [Make your documents available](#make-your-documents-available)
    - [Copy your PDF, text files etc to ./documents folder. ](#copy-your-pdf-text-files-etc-to-documents-folder-)
  - [Vectorize](#vectorize)
- [Query your documents](#query-your-documents)
  - [Web UI](#web-ui)
    - [Start the web ui](#start-the-web-ui)
  - [CLI](#cli)
- [Custom Prompts](#custom-prompts)
  - [Basic Usage](#basic-usage)
  - [Example Prompt Templates](#example-prompt-templates)
    - [Default Simple Prompt](#default-simple-prompt)
    - [No BS strict prompt](#no-bs-strict-prompt)
    - [Language-Specific Prompts](#language-specific-prompts)
      - [German Response](#german-response)
      - [Vietnamese Response](#vietnamese-response)
      - [Bangla Response](#bangla-response)
    - [Technical Documentation Prompts](#technical-documentation-prompts)
      - [API Documentation](#api-documentation)
      - [Troubleshooting Guide](#troubleshooting-guide)
      - [Code Examples](#code-examples)
  - [Note](#note)
    - [Language Support](#language-support)
    - [Customizing Prompts](#customizing-prompts)
    - [Testing Your Prompts](#testing-your-prompts)
- [Screenshot of the web ui](#screenshot-of-the-web-ui)
- [Run web ui as a service](#run-web-ui-as-a-service)
  - [Linux Systemd](#linux-systemd)
  - [Linux sysv](#linux-sysv)
  - [MacOS](#macos)
  - [Windows ](#windows-)
- [Various Utility Scripts](#various-utility-scripts)
  - [List documents](#list-documents)
  - [Convert PDF to Text](#convert-pdf-to-text)
- [Known Issues](#known-issues)
- [Roadmap/TODO](#roadmaptodo)
- [License](#license)

**privategpt** is an OpenSource Machine Learning (ML) application that 
lets you query your local documents using natural language with Large 
Language Models (LLM) running through [ollama](https://ollama.com) locally 
or over network. Everything runs on your local machine or network so your 
documents stay private. It has both web and command line interface that 
you can use to ask questions about your documents.

The project is under heavy development, please try it out give and us your 
feedback. Thanks.

# Introduction

It uses [ollama](https://ollama.com) for running Large Language Models (LLM).
[ollama](https://ollama.com) runs on Linux, Mac and Windows on any system 
with CPU or GPU and performs very well.

The license is [MIT](#license).

# Background and Motivation
I started this project to learn about
[RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)
applications using local Large Language Models (LLMs).
RAG is a fancy acronym for finding similar document fragments (chunks)
using machine learning algorithm in your local documents and send the chunks to a
Large Language Model (LLM) to make sense out them by summarizing the chunks.

My goal was to use RAG technology, but without spending time and resources
to train or fine-tune LLMs. Privacy was essential - keeping documents private by not
sending them to the cloud.

The project was initially based on the
[privateGPT](https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt)
example from the ollama github repo, which worked great for querying local
documents. When the original example became outdated and stopped working, 
fixing and improving it became the next step.

Running the app across Linux, Mac, and Windows platforms was important, along with
improving documentation on RAG functionality. Adding a web interface replaced
the original CLI-only version, while cleaning up the code, adding
configs, logging etc. made it more organized and production-ready.

My plan is to keep the project simple and easy to understand. Hope you find
the project useful too.

Please look at [ChangeLog](ChangeLog.md) for details about what changed.
Please look at the [Roadmap/TODO](#roadmaptodo) section for future plans.

# How it works

![alt privategpt](images/privategpt.drawio.png "privategpt")

This diagram is created by Claude AI in mermaid format from my description 
then I used [draw.io](https://app.diagrams.net/) on desktop to tweak it little bit.


# Contributing

Please send a pull request if you add features, fix bugs or update the documentation. 

If you want to update the documentation, **please do not update README.md directly**, 
rather update the Markdown files in _markdowns/_ directory and send the pull request. I will
generate the README.md.

# Version

The current version of the tools is 1.0.4.

Please look at [ChangeLog](ChangeLog.md) for what has changed in the
current version.  It is possible, new python modules need to be installed.

# Supported Platforms

The document assistant and document ingestion code run on:

* Linux
* MacOS (Tested on Intel and M2 Macs)
* Windows


# Requirements (ollama and python3)

- [ollama](https://ollama.com) - you have to install, read below.
- python3

Check if python3 is installed by typing `python3 --version`. If not, you have to install it.
Please look at [https://www.python.org/](https://www.python.org/) for information.

## Python Version

- Required: python 3.12.x (Currently tested with python 3.12.x)

- ❌ Not yet compatible with Python 3.13 

- ⚠️  It should work but not tested with Python versions below 3.12


If the system where [ollama](https://ollama.com) will be running has a GPU, queries and 
responses will be fast. Without a GPU, it will still work but will be 
slower. You can run [ollama](https://ollama.com) on another system with a GPU or even in the 
cloud with a GPU by specifying the URL in [config.py](#configuration-file).

# Installation

## Clone the  repo

You must have [git](https://git-scm.com/downloads/win)  instlled at this time. Open a Terminal on Mac/Linux, use a command prompt on Windows,
then type:

    git clone https://github.com/muquit/privategpt.git
    cd privategpt

## Install ollama

- First of all you have to install [ollama](https://ollama.com) on your system. Please follow 
the instructions at https://ollama.com
- To check if ollama is running, point your browser to `http://127.0.0.1:11434`. You should see:

```
Ollama is running
```

```
➤ ollama --version
ollama version is 0.4.6
```

- Then install say 2 Large Language Models (LLMS), I use mistral and llama3. 
You can install as many as you like provided your system has plenty of memory.
Here is how to install and query models. You can run any large language model from 
[ollama models](https://ollama.com/library) page. It is also possible to 
convert any GGUF models from huggingface to ollama models and use them. I 
will add instructions on how to do that ...

```
ollama pull mistral
ollama pull llama3
ollama list
ollama run mistral
/bye to exit
```

In my system:

```
$ ollama list
NAME                    ID              SIZE    MODIFIED
qwen2:7b                dd314f039b9d    4.4 GB  2 days ago
nomic-embed-text:latest 0a109f422b47    274 MB  4 weeks ago
llama3:latest           365c0bd3c000    4.7 GB  8 weeks ago
mistral:latest          f974a74358d6    4.1 GB  8 weeks ago
```

The models will be displayed in the select list in the sidebar of the web ui. To ignore 
any model, add it in the list in `config.py` with `EXCLUDE_MODELS`

[ollama](https://ollama.com) will use GPU if your system has it. To check do this:

```
ollama run mistral
/bye
ollama ps
```
If your system does not have GPU, the output will look like:

```
ollama ps
NAME              ID              SIZE      PROCESSOR    UNTIL
mistral:latest    f974a74358d6    5.9 GB    100% CPU     4 minutes from now
```

If your system has GPU, the output might look like:

```
NAME              ID              SIZE      PROCESSOR    UNTIL
mistral:latest    f974a74358d6    6.4 GB    100% GPU     4 minutes from now
```

If your system has GPU, the inference will be faster.


## Install python modules

## Python Version

- Required: python 3.12.x (Currently tested with python 3.12.x)

- ❌ Not yet compatible with Python 3.13

- ⚠️  It should work but not tested with Python versions below 3.12

If you use [homebrew](https://brew.sh/) and if it installed python 3.13, do
the following (this is the procedure on a Mac M2). Please note, this is my
suggestion, you decide if you want to do it or not. If you need Python 3.13,
you might not want to do that.

- Check if python3.13 is installed
```
 brew list|grep python
```
- If python 3.12 is also there, do the following:

```
 brew unlink python@3.13
 brew link python@3.12
 brew pin python@3.12
```

- When doing `brew updgrade`, you can be more selective:

```
 brew upgrade --ignore-pinned    
```

- Set PATH in your `~/.zshrc` or `~/.bash_profile`

```
 export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"
 source ~/.zshrc 
or
 source ~/.bash_profile
 which python3
 python3 -V
 or
 python3.12 -V
 pip3 -V
 which pip3
```

- If the virtual env is created with python 3.13, `deactivate`, remove the directory and start again.

### Create Python Virtual Environment

- Create python virtual environment first. **Do not install the modules globally in your system, it can break things.**

### Linux/MacOS
```
python3 -m venv pvenv
```

If virtual environemnt module is not installed, follow the help message to install it and then create the envionment. In Ubuntu, you might see the message to install `apt install python3.12-venv`. So, do that first and then go back to the previous step to create the python3 virtual environment.

- Activate virtual environment

```
source pvenv/bin/activate
```

- If you need to deactive virtual env

```
deactivate
```

### Windows
```
python3 -m venv pvenv
```

- Activate virtual environment

```
pvenv\Scripts\activate
```

- If you need to deactive virtual env

```
pvenv\Scripts\deactivate
```

### Install the Python Modules

- Install python modules. The following modulles and their dependencies will be installed in the virtual environment.

```
$ more requirements_pinned.txt
# Contains exact versions that are known to work together
# Test environment: Python 3.12
#
# If you want to try the latest versions (may introduce compatibility 
# issues):
#   1. pip install -r requirements.txt --upgrade
#   2. If it works: Please create an issue with your versions (run:
#      ./scripts/check_versions.py)
#   3. If it breaks: Fall back to pinned versions, do the follwing:
#      deactive
#      rm -rf pvenv
#      python3 -m venv pvenv
#      source pvenv/bin/activate
#      pip install -r requirements_pinned.txt
#
# Generated with: ./scripts/check_versions.py
tqdm==4.67.1
ollama==0.4.2
langchain_community==0.3.8
langchain_huggingface==0.1.2
langchain-chroma==0.1.4
langchain-ollama==0.2.0
chromadb==0.5.20
sentence_transformers==3.3.1
pymupdf==1.24.14
streamlit==1.40.2
#
# Last verified: Nov-29-2024
```

To install the modules:

```
pip3 install -r requirements_pinned.txt
```

If you want to try the latest versions of the modules (may introduce 
compatibility issues)

```
deactivate
rm -rf pvenv
python3 -m venv pvenv
source vnenv/bin/activate # Linux/Unix
pvenv\Scripts\deactivate  # Windows
pip3 install -r requirements.txt --upgrade
```

If you are using python 3.13, it will fail and you will see the following
error:

```
  Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error

  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [6 lines of output]

      Cargo, the Rust package manager, is not installed or is not on PATH.
      This package requires Rust and Cargo to compile extensions. Install it through
      the system's package manager or via https://rustup.rs/

      Checking for Rust toolchain....
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
```

Install python 3.12 as described above.

The versions I used are shown below:

On a Mac M2

```
➤ python3 -V
Python 3.12.5
➤ ./scripts/check_versions.py
tqdm==4.66.6
ollama==0.3.3
langchain_community==0.3.5
langchain_huggingface==0.1.2
langchain-chroma==0.1.4
langchain-ollama==0.2.0
chromadb==0.5.17
sentence_transformers==3.2.1
pymupdf==1.24.13
streamlit==1.39.0

--
Updated: Nov-03-2024
```

On an Intel Mac running Sonoma 14.6.1

```
➤ python3 -V
Python 3.12.7
➤ ./scripts/check_versions.py
tqdm==4.66.6
ollama==0.3.3
langchain_community==0.3.5
langchain_huggingface==0.1.2
langchain-chroma==0.1.4
langchain-ollama==0.2.0
chromadb==0.5.17
sentence_transformers==3.2.1
pymupdf==1.24.13
streamlit==1.39.0

--
Updated: Nov-03-2024
```

On a Lenovo T490 with 16GB memory, Ubuntu 24.04.1 LTS

```
➤ python3 -V
Python 3.12.3
➤ ./scripts/check_versions.py
tqdm==4.66.6
ollama==0.3.3
langchain_community==0.3.5
langchain_huggingface==0.1.2
langchain-chroma==0.1.4
langchain-ollama==0.2.0
chromadb==0.5.17
sentence_transformers==3.2.1
pymupdf==1.24.13
streamlit==1.39.0

--
Updated: Nov-03-2024
```

## Common Issues

1. Wrong python version

Check your Python version

```
python3 --version
```
Make sure it shows Python 3.12.x

2. Module Installation Issues:

- Use a fresh virtual environment
- Make sure you're using the correct Python version
- Update pip before installing requirements

3. Homebrew Python Updates:

- Pin Python 3.12 to prevent unwanted updates:

```
brew pin python@3.12
```

## Troubleshotting

If you encounter installation issues:

1. Check Python version:

```
python3 --version
which python3
```

2. Verify package versions:

Run the included version checker

```
python3 scripts/check_versions.py
```

3. Common Solutions:

- Delete and recreate virtual environment

# Configuration file
Please update as needed

    import os
    import sys
    
    # If new variables are added, do not forget to
    # add it to utils/load_config.py
    
    current_file_path = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(current_file_path)
    VERSION="1.0.4"
    
    APP_TITLE = "Private Documents Assistant"
    APP_DESCRIPTION = "An on-premises private documents assistant with ollama"
    PROJECT_URL = "https://github.com/muquit/privategpt"
    SHOW_PROJECT_URL = True
    SHOW_SIDEBAR = True
    ASK_ME_TEXT = "Ask me anything about your documents"
    
    # Default system prompt. Please look at Custom Prompts section
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
    
    ## No BS strict prompt
    ## LLMs like to talk too much, use strict prompt if you want
    #CUSTOM_PROMPT = """
    #Use the following context to answer the given question. Be direct and concise.
    
    #Rules:
    #1. Only use information from the provided context
    #2. For factual questions, provide direct answers without analysis
    #3. For complex questions, structure your response clearly
    #4. If the answer isn't in the context, respond with "I cannot answer this based on the provided context"
    #5. Don't include phrases like "According to the context" or "Based on the provided information"
    #6. Don't speculate or infer beyond what's directly stated
    
    #Context:
    #{context}
    
    #Question: {question}
    
    #Answer:"""
    
    # Change if ollama is running on a different system on 
    # your network or somewhere in the cloud. Please look
    # at ollama document and FAQ on how ollama can bind
    # to all network interfaces.
    # By default use localhost (127.0.0.1)
    OLLAMA_URL = "http://127.0.0.1:11434"
    
    
    # put your documents in ./documents directory
    DOCUMENT_DIR = os.path.join(PROJECT_ROOT, 'documents')
    #DOCUMENT_DIR = os.path.join(PROJECT_ROOT, 'test_docs')
    
    # database will be created in ./db directory
    PERSIST_DIRECTORY = os.path.join(PROJECT_ROOT, 'db')
    
    # metadata and document processing config
    METADATA_ENABLED = True          # enable/disable enhanced metadata
    DEDUP_ENABLED = True             # enable/disable deduplication checking
    
    # metadata fields to extract/generate
    METADATA_FIELDS = [
        "source",                   # original filename (you already have this)
        "chunk_index",              # position of chunk in document
        "document_type",            # pdf, txt, etc.
        "creation_date",            # document creation date
        "section_title",            # section/heading if available
        "content_hash"              # for similarity detection
    ]
    
    # similarity detection settings
    SIMILARITY_THRESHOLD = 0.95     # threshold for considering chunks similar
    MIN_CHUNK_LENGTH = 50           # minimum characters in a chunk to consider
    
    CHUNK_SIZE = 500
    OVERLAP = 50
    TARGET_SOURCE_CHUNKS = 5
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
    

# Vectorize your documents

This project uses [chroma db](https://docs.trychroma.com/) for storing
document embeddings/vectors.

TODO: explain how Embedding/vectorizing works and why it is needed.

At this time I've noticed good results with PDF _text_ and regular text 
documents. The instructions will be updated when I play with other 
document types.

- The project comes with a free PDF book [dracula.pdf](https://www.planetebook.com/free-ebooks/dracula.pdf) in `./documents` directory. I noticed that the extracted texts from the PDF version of dracula gives much better results than the free dracula.txt and time [Project Gutenberg](https://www.gutenberg.org/). If you want, copy some PDF files to `./documents` directory and vectorize them. If new documents are found, they will be appended to the vector database.

## Make your documents available

### Copy your PDF, text files etc to ./documents folder. 

## Vectorize

```
python3 ./ingest/ingest.py
```

Please vectorize again when new documents are added. After that, make sure to
restart the web ui. At this time, please look [List documents](#list-documents) 
section to list what documents are in the chromadb. In future, the documents
will be listed in the sidebar.

The vector database will be created in `./db` directory as configured in `config.py`.

If you already ingested your documents and got the newer version of
**privategpt** and if you see deprecation warning about
[chroma db](https://docs.trychroma.com/), please remove the `./db` directory
and re-ingest your documents.

# Query your documents

The documents can be queried from a web ui or from command line


## Web UI

### Start the web ui

```
streamlit run ./assistant/assistant_ui.py
```

It will start a browser in your local machine. If you do not want to   start a browser, run:

```
streamlit run ./assistant/assistant_ui.py --server.headless true
Starting streamlit without opening a browser

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8502
  Network URL: http://192.168.1.151:8502
  External URL: http://xxx.xxx.xxx.xxx:8502
```

## CLI

```
usage: assistant_cli.py [-h] [--hide-source] [--mute-stream] [--model MODEL]

privategpt: Ask questions to your documents without an internet connection,
using the power of LLMs.

options:
  -h, --help            show this help message and exit
  --hide-source, -S     Use this flag to disable printing of source documents
                        used for answers.
  --mute-stream, -M     Use this flag to disable the streaming StdOut callback
                        for LLMs.
  --model MODEL, -m MODEL
                        Specify the model to use. Defaults to the value set in
                        config.py.
```

# Custom Prompts

Custom prompts are powerful tools that shape how Large Language Models (LLMs)
respond to questions. Think of prompts as instructions to the AI - they 
control the style, format, language, and depth of the answers. For example,
you can make the AI explain things like a teacher, write code like a 
developer, or troubleshoot like a system administrator.

This section provides different prompt examples that you can use with 
**privategpt**.  Whether you need responses in specific languages, 
technical documentation, code examples, or structured analysis, these 
prompts will help you get the exact type of response you want from your 
LLM.


## Basic Usage

The prompts help control how the LLM responds to questions. You can 
customize aspects like:
- Response language (English, German, Vietnamese, Bangla etc.)
- Response structure (free-form, bullet points, sections)
- Technical detail level
- Special instructions (like code examples, troubleshooting steps)

Make sure your LLM supports the target language before using language-specific
prompts. The quality of translations might vary depending on the model 
used. Please look at [Ollama Model Libary](https://ollama.com/library)
for finding better multilingual models.

Please define your custom prompt with variable **CUSTOM_PROMPT** in
[Configuration file](#configuration-file)

## Example Prompt Templates

### Default Simple Prompt

This is the basic prompt template that works for most cases:
```python
CUSTOM_PROMT = """
Given the following context, answer the question using only the provided
information. If the answer isn't found in the context, respond with
'I cannot answer this based on the provided context.'

Context:
{context}

Question: {question}

Answer: Let me analyze the context and provide a detailed response.
"""
```

### No BS strict prompt
```python
CUSTOM_PROMPT = """
Use the following context to answer the given question. Be direct and concise.

Rules:
1. Only use information from the provided context
2. For factual questions, provide direct answers without analysis
3. For complex questions, structure your response clearly
4. If the answer isn't in the context, respond with "I cannot answer this based on the provided context"
5. Don't include phrases like "According to the context" or "Based on the provided information"
6. Don't speculate or infer beyond what's directly stated

Context:
{context}

Question: {question}

Answer:"""
```

### Language-Specific Prompts
These prompts tell the LLM to respond in specific languages.


#### German Response
```python
CUSTOM_PROMPT = """Use the following pieces of context to answer the question.
IMPORTANT: Provide your answer in German language only.

Context:
{context}

Question: {question}

Please provide a helpful answer in German:"""
```

#### Vietnamese Response

[Bug #1](../../issues/1)

```python
CUSTOM_PROMPT = """Sử dụng các thông tin ngữ cảnh sau đây để trả lời câu hỏi.
QUAN TRỌNG: Chỉ trả lời bằng tiếng Việt.

Ngữ cảnh:
{context}

Câu hỏi: {question}

Vui lòng cung cấp câu trả lời hữu ích bằng tiếng Việt:"""
```

#### Bangla Response
Native বাংলা script:
```python
CUSTOM_PROMPT = """এই তথ্যগুলো দেখে প্রশ্নের উত্তর দাও।
জরুরি কথা: শুধু বাংলায় উত্তর দিতে হবে।

তথ্য:
{context}

প্রশ্ন: {question}

দয়া করে বাংলায় উত্তর দাও:"""
```

### Technical Documentation Prompts

#### API Documentation
Useful for explaining APIs and their usage:
```python
CUSTOM_PROMPT = """Using the provided context, explain the API usage.
Include examples of common use cases and parameter descriptions.

Context:
{context}

Question: {question}

API Documentation:
1. Overview:
2. Parameters:
3. Usage Examples:
4. Common Patterns:
5. Notes:"""
```

#### Troubleshooting Guide
Helps in diagnosing and solving issues:
```python
CUSTOM_PROMPT = """Using the context provided, help diagnose or solve the issue.
If the exact solution isn't in the context, suggest the most relevant troubleshooting steps.

Context:
{context}

Question: {question}

Analysis and Solution:
1. Problem identification:
2. Relevant context:
3. Solution/Workaround:
4. Prevention tips (if applicable):"""
```

#### Code Examples
Focuses on code explanation with comments:
```python
CUSTOM_PROMPT = """Based on the context, provide an explanation with emphasis on code examples.
Format any code snippets clearly and include comments for better understanding.

Context:
{context}

Question: {question}

Explanation and Code Examples:"""
```

The prompt examples are generated by Claude AI from my desription.

## Note

### Language Support
Make sure your LLM supports the target language before using language-specific prompts.
The quality of translations might vary depending on the model used.

### Customizing Prompts
Feel free to mix elements from different prompts to create your own.
Some key points to consider:
- Keep instructions clear and specific
- Include any formatting preferences
- Specify the desired language if needed
- Add structure hints if you want organized responses

### Testing Your Prompts
Always test new prompts with various types of:
- Questions (simple, complex, technical)
- Contexts (short, long, mixed languages)
- Response requirements (code, explanations, troubleshooting)


# Screenshot of the web ui

A response for a question about one of the documents. Sources show the chunks found in the similarity search in the database. The chunks are then sent to the locall LLM and the model summerized the chunks as reponse at the top.

from [mistral 7.2B](https://ollama.com/library/mistral) model without GPU:

![dracula_mistral](./screenshots/dracula_mistral.png)

from [llama3 8b](https://ollama.com/library/llama3) model without GPU:

![dracula_llama3](./screenshots/dracula_llama3.png)

![dracula_qwen2](./screenshots/dracula_qwen2.png)

# Run web ui as a service
## Linux Systemd

Please look at `systemd/` directory. It needs some cleaning up but it works. An installation script
will be provided in future.

## Linux sysv

TODO

## MacOS

TODO

## Windows 

TODO

# Various Utility Scripts

## List documents

To list documents in chromadb, use the following scripts

```
scripts/list_chroma_metadata.py
scripts/list_chroma_metadata_files.py
scripts/list_chroma_metadata_json.py
scripts/list_chroma_metadata_pretty.py
```
## Convert PDF to Text

```
scripts/pdf2txt.py
```



List loaded models in ollama (for testign Bug #3)
```
scripts/list_loaded_models.py
```

# Known Issues

Currently all the documents in the chromadb are searched for similarity, 
which can return wrong information if documents contain similar texts. 
Please look at the returned **Source** to make sure the response is correct.

[Roadmap/TODO](#roadmaptodo) is to allow to select documents to 
search for similarity and use chromadb's filtering mechanism to perform the 
similarity search before sending the chunks to LLM.


# Roadmap/TODO
* Currently all the documents in the chromadb are searched which can return wrong
information if documents contain similar texts. Allow to select
one or more documents to search and use chromadb's filtering mechanism to perform the
similarity search before sending the chunks to LLM.

* Suport [vLLM](https://github.com/vllm-project/vllm?tab=readme-ov-file)

* Add an option to use custom system prompt template ✅ (v1.0.3 - Nov-02-2024)

* Support other OpenSource vector database like [qdrant](https://github.com/qdrant/qdrant)

* Add readline like history to CLI

* Create a docker image

* Run the web ui as a service for Linux, MacOS and Windows. systemd unit file
and script are in systemd directory, needs some modifying for your needs, like
change user and group.
* 
* etc...

You're welcome to contribute to any of these.

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
    
    This project is adapted from:
    https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt

---
* This file is assembled from markdowns/*.md with [markdown_helper](https://github.com/BurdetteLamar/markdown_helper)
