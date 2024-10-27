## Install python modules

## Python Version

- Required: python 3.12.x (Currently tested with python 3.12.x)

- ⚠️ Not yet compatible with Python 3.13

- ❌ It may work but not tested with Python versions below 3.12

If you use [homebrew](https://brew.sh/) and if it installed python 3.13, do
the following (this is the procedure on a Mac M2). Please note, this is my
suggestion, you decide if you want to do it or not. If you need Python 3.13,
you might not want to do that.

- Check if python3.13 is installed
```
 brew list|grep python
```
- If python 3.12 is also there, do the following:

```
 brew unlink python@3.13
 brew link python@3.12
 brew pin python@3.12
```

- When doing `brew updgrade`, you can be more selective:

```
 brew upgrade --ignore-pinned    
```

- Set PATH in your `~/.zshrc` or `~/.bash_profile`

```
 export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"
 source ~/.zshrc 
or
 source ~/.bash_profile
 which python3
 python3 -V
 or
 python3.12 -V
 pip3 -V
 which pip3
```

- If the version env is created with python 3.13, remove the directory.

### Create Python Virtual Environment

- Create python virtual environment first. **Do not install the modules globally in your system, it can break things.**

### Linux/MacOS
```
python3 -m venv pvenv
```

If virtual environemnt module is not installed, follow the help message to install it and then create the envionment. In Ubuntu, you might see the message to install `apt install python3.12-venv`. So, do that first and then go back to the previous step to create the python3 virtual environment.

- Activate virtual environment

```
source pvenv/bin/activate
```

- If you need to deactive virtual env

```
deactivate
```

### Windows
```
python3 -m venv pvenv
```

- Activate virtual environment

```
pvenv\Scripts\activate
```

- If you need to deactive virtual env

```
pvenv\Scripts\deactivate
```

### Install the Python Modules

- Install python modules. The following modulles and their dependencies will be installed in the virtual environment.

```
$ more requirements.txt
tqdm
ollama
langchain_community
langchain_huggingface
langchain-chroma
chromadb
sentence_transformers
pymupdf
streamlit
```

To install the modules:

```
pip3 install -r requirements.txt
```

If you are using pythin 3.13, it will fail and you will see the following
error:

```
  Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error

  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [6 lines of output]

      Cargo, the Rust package manager, is not installed or is not on PATH.
      This package requires Rust and Cargo to compile extensions. Install it through
      the system's package manager or via https://rustup.rs/

      Checking for Rust toolchain....
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
```

Install python 3.12 as described above.

The versions I used are shown below:

It's a Mac M2.

```
➤ python3 -V
Python 3.12.5

➤ ./scripts/check_versions.py
tqdm==4.66.5
ollama==0.3.3
langchain_community==0.3.3
langchain_huggingface==0.1.0
langchain-chroma==0.1.4
chromadb==0.5.15
sentence_transformers==3.2.1
pymupdf==1.24.12
streamlit==1.39.0
```

On an Intel Mac running Sonoma 14.6.1

```
➤ python3 -V
Python 3.12.7
➤ ./scripts/check_versions.py
tqdm==4.66.5
ollama==0.3.3
langchain_community==0.3.3
langchain_huggingface==0.1.0
langchain-chroma==0.1.4
chromadb==0.5.15
sentence_transformers==3.2.1
pymupdf==1.24.12
streamlit==1.39.0
```

On a Lenovo T490 with 16GB memory, Ubuntu 24.04.1 LTS

```
➤ python3 -V
Python 3.12.3
➤ ./scripts/check_versions.py
tqdm==4.66.5
ollama==0.3.3
langchain_community==0.3.3
langchain_huggingface==0.1.0
langchain-chroma==0.1.4
chromadb==0.5.15
sentence_transformers==3.2.1
pymupdf==1.24.12
streamlit==1.39.0
```

## Common Issues

1. Wrong python version

Check your Python version

```
python3 --version
```
Make sure it shows Python 3.12.x

2. Module Installation Issues:

- Use a fresh virtual environment
- Make sure you're using the correct Python version
- Update pip before installing requirements

3. Homebrew Python Updates:

- Pin Python 3.12 to prevent unwanted updates:

```
brew pin python@3.12
```

## Troubleshotting

If you encounter installation issues:

1. Check Python version:

```
python3 --version
which python3
```

2. Verify package versions:

Run the included version checker

```
python3 scripts/check_versions.py
```

3. Common Solutions:

- Delete and recreate virtual environment
