########################################################################
# Add CLI config separate than main app, otherwise -h or --help takes
# forever to load due to time takes for importing the python modules
# muquit@muquit.com Oct-14-2024 
########################################################################
CLI_DESCRIPTION = "privategpt: Ask questions to your documents without an internet connection, using the power of LLMs."

CLI_ARGUMENTS = [
    {
        "flags": ["--hide-source", "-S"],
        "action": "store_true",
        "help": "Use this flag to disable printing of source documents used for answers."
    },
    {
        "flags": ["--mute-stream", "-M"],
        "action": "store_true",
        "help": "Use this flag to disable the streaming StdOut callback for LLMs."
    },
    {
        "flags": ["--model", "-m"],
        "type": str,
        "help": "Specify the model to use. Defaults to the value set in config.py."
    }
]
