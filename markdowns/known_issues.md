# Known Issues

Currently all the documents in the chromadb are searched for simillarity, 
which can return wrong information if documents contain similar texts. 
Please look at the returned **Source** to make sure the response is correct.

[Roadmap/TODO](#roadmaptodo) is to allow to select documents to 
search for similarity and use chromadb's filtering mechanism to perform the 
similarity search before sending the chunks to LLM.

