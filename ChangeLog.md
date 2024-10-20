## Contents
- [v1.0.2](#v102)

<!-- TOC -->

- [v1.0.2](#v102)

<!-- /TOC -->

# v1.0.2

* Could not make the code in ollama to work, so I updated the code and also
using newer versions of python modules. 

* Use config file 

* Add logging

* Use latest langchain and langchain_community modules and API

* create streamlit based web app

(Sep-15-2024)

* In an old Windows system without GPU, during ingestion, I've seen an error
ValueError: Batch size 2076 exceeds maximum batch size 166. Therefore,
dynamically adjust batch size if this kind of exception occurs.

* Detection of existing chromadb code is buggy, It was creating duplicate
entries with each ingestion.

(Sep-29-2024)

* In assistant ui, use ollama client to list models instead of ollama.list().
Specify OLLAMA_URL from config.py for the client.

(Sep-29-2024)

* Add command line client assistant/assistant_console.py

(Oct-12-2024)

* Use langchain RetrievalQA's invoke() method instead of run(), otherwise 
a waring '__call__ method is deprecated, use invoke instead.' is shown.
config key had to be used to invoke() otherwise streamlit's stream handler
does not work.

(Oct-20-2024)



