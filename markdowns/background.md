# Background and Motivation

I started this project to learn abut
[RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)
applications using local Large Language Models (LLMs). 
RAG is a fancy acronym for finding similar document fragments (chunks) 
using machine learning algorithm in your local documents and send the chunks to a 
Large Language Model (LLM) to make sense out them by summarizing the chunks.

I wanted to use RAG technology, but did not have time and resource 
to train or fine-tune LLMs. The main goal was to keep documents private by not
sending them to the cloud;

The project was initially based on the 
[privateGPT](https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt)
example from the ollama github repo, which worked greate for querying local
documents. But the original example became outdated and at one point it 
stopped working. I decided to fix it and make it better.

I wanted to run the app  on Linux, Mac, and Windows platforms, with 
improved documentation on RAG functionality.  I added a web interface as 
the original code only had CLI.  I also cleaned up the code, added 
configs, logging etc. and tried to make it more organized so it could be 
used in production.

I plan to keep the project simple and easy to understand. Hope you find
the project useful too.

Please look at [ChangeLog](ChangeLog.md).for details for what is changed.
Please look at the [Roadmap/TODO](#roadmaptodo) section for future plans.
