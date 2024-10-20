# Roadmap/TODO
* Currently all the documents in the chromadb is searched which can return wrong
information if documents contain similar texts. Specify users to select
documents to search and user chromadb filtering mechanism to perform the
similarity search before sending the chunks to LLM

* Support other OpenSource vector database like [qdrant](https://github.com/qdrant/qdrant)

* Add readline like history to CLI

* Create a docker image

* Run the web ui as a service for Linux, MacOS and Windows. systemd unit file
and script are in systemd directory, needs some modifying for your needs, like
change user and group.
* 
* etc...
