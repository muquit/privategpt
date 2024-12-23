## Install python modules

## Python Version

- Required: python 3.12.x (Currently tested with python 3.12.x)

- ❌ Not yet compatible with Python 3.13

- ⚠️  It should work but not tested with Python versions below 3.12

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

- If the virtual env is created with python 3.13, `deactivate`, remove the directory and start again.

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
$ more requirements_pinned.txt
@[:markdown](../requirements_pinned.txt)
```

To install the modules:

```
pip3 install -r requirements_pinned.txt
```

If you want to try the latest versions of the modules (may introduce 
compatibility issues)

```
deactivate
rm -rf pvenv
python3 -m venv pvenv
source vnenv/bin/activate # Linux/Unix
pvenv\Scripts\deactivate  # Windows
pip3 install -r requirements.txt --upgrade
```

If you are using python 3.13, it will fail and you will see the following
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
