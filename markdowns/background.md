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
