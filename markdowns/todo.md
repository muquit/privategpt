# Roadmap/TODO
* Currently all the documents in the chromadb are searched which can return wrong
information if documents contain similar texts. Allow to select
one or more documents to search and use chromadb's filtering mechanism to perform the
similarity search before sending the chunks to LLM.

* Suport [vLLM](https://github.com/vllm-project/vllm?tab=readme-ov-file)

* Add an option to use custom system prompt template.

* Support other OpenSource vector database like [qdrant](https://github.com/qdrant/qdrant)

* Add readline like history to CLI

* Create a docker image

* Run the web ui as a service for Linux, MacOS and Windows. systemd unit file
and script are in systemd directory, needs some modifying for your needs, like
change user and group.
* 
* etc...

You're welcome to contribute to any of these.
