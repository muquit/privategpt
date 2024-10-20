# Background and Motivation

This project emerged from a personal exploration into 
[RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)
applications using local Large Language Models (LLMs). 
RAG is a fancy acronym for findng similar document fracments (chunks) 
using machine learing algorithm in your local documents and send the chunks to a 
Large Language Model (LLM) to make sense out them by summarizing the chunks.

Inspired by the potential of RAG technology, but lacking time and resource 
for training or fine-tuning an LLM, the project began as an experiment with local 
LLMs. The most important goal was not to send propietary documents to
cloud for searching.

The project was initially based on the 
[privateGPT](https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt)
example from the ollama gitHub repo, which demonstrated impressive results 
with local document querying. But the original example became outdated 
and at one point it stopped working, this project aimed to revive and 
improve upon the concept.

Efforts were made to ensure the application works across Linux, Mac, and 
Windows platforms, with improved documentation on RAG functionality.
The codebase was modularized, configurations were added, and the overall 
structure was refined to make it potentially production-ready. 

I plan to keep the project simple and easy to understand. Hope you will find
the project useful as well.

Please look at [ChangeLog](ChangeLog.md).for details for what is changed.
Please look at the [Roadmap/TODO](#roadmaptodo) section for future plans.
