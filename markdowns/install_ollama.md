## Install ollama

- First of all you have to install [ollama](https://ollama.com) on your system. Please follow 
the instructions at https://ollama.com
- To check if ollama is running, point your browser to `http://127.0.0.1:11434`. You should see:

```
Ollama is running
```

- Then install say 2 Large Language Models (LLMS), I use mistral and llama3. 
You can install as many as you like provided your system has plenty of memory.
Here is how to install and query models. You can run any model from ollama 
page. It is also possible to convert any GGUF models from huggingface to 
ollama modes and use them. I will add instructions on how to do that ...

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

