# Requirements (ollama and python3)

- [ollama](https://ollama.com) - you have to install, read below.
- python3

Check if python3 is installed by typing `python3 --version`. If not, you have to install it.
Please look at [https://www.python.org/](https://www.python.org/) for information.

## Python Version

- Required: python 3.12.x (Currently tested with python 3.12.x)

- ⚠️  Not yet compatible with Python 3.13 

- ❌ It may work but not tested with Python versions below 3.12


If the system where [ollama](https://ollama.com) will be running has a GPU, queries and 
responses will be fast. Without a GPU, it will still work but will be 
slower. You can run [ollama](https://ollama.com) on another system with a GPU or even in the 
cloud with a GPU by specifying the URL in [config.py](#configuration-file).
