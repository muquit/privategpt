## Contents
<!-- TOC -->

- [v1.0.4](#v104)
- [v1.0.3](#v103)
- [v1.0.2](#v102)

<!-- /TOC -->

# v1.0.4

* Resolve #3. ollama Python package was updated from 0.3.3 to 0.4.2 which 
changed how model information is returned from the API. The old code tried 
to access models using dict syntax model["name"] but the new version 
returns Model objects that need to be accessed using model.model 
attribute. Now a pinned version of `requirements_pinned.txt` is supplied with
the versions of the modules known to work.

(Nov-29-2024)

* For ingestion testing adddd Universal Declaration of Human Rights 
documents in `documents/universal_declaration_of_human_rights.pdf`
Source: https://www.un.org/sites/un2.un.org/files/2021/03/udhr.pdf

(Nov-30-2024)

# v1.0.3

* Due to LangChain's package restructuring, Ollama integration is updated. 
`langchain-ollama` is added in `requirements.txt`.
Please follow these steps to update:

```
    pip3 install -r requirements.txt
```

Or specifically install langchain-ollama:

```
    pip3 install langchain-ollama
```
If you're extending or modifying the code, note that imports from:

```
from langchain_community.llms import Ollama
```
is changed to:

```
from langchain_ollama import OllamaLLM
```

Also Ollama() call is changed to OllamaLLM()

(Nov-02-2024)

* Custom prompt template can be spcified in [Configuration file](README.md#configuration-file). Please look 
at [Custom Prompts](README.md#custom-prompts) for various examples.

(Nov-02-2024)

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



