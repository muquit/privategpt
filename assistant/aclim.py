#!/usr/bin/env python3

#====================================================================
# It's an OpenSource RAG application that uses ollama
# https://github.com/muquit/privategpt for source
# https://muquit.com/ 
# This code is called from assistant_cli.py otherwise -h or --help
# takes forever due to time takes for importing the python modules.
# Oct-14-2024 
#====================================================================

"""
The document retrieval code is based on:
https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt
But his code have config file, progress bar etc and uses newer versions of python
modules.
"""

from braille_spinner import BrailleSpinner

import sys
import os
import textwrap
import threading
import atexit

sys.stderr.write('\rImporting packages ... ')
# suppress warning
import warnings
from transformers import logging
warnings.filterwarnings("ignore", category=FutureWarning, message=".*`clean_up_tokenization_spaces`.*")
logging.set_verbosity_error()

from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# by default chromadb sends telemetry info
# turn it off.
# muquit@muquit.com Aug-28-2024
os.environ["ANONYMIZED_TELEMETRY"] = "false"

from langchain_chroma import Chroma
import ollama
from ollama import Client
from langchain_community.llms import Ollama
import chromadb
import argparse
import time
#sys.stderr.write(f"Done")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils.load_config import load_config
from utils.logging import setup_logging


class Colors:
    COLOR_HEADER = '\033[95m'
    COLOR_GREEN = '\033[92m'
    COLOR_BLUE = '\033[94m'
    COLOR_CYAN = '\033[96m'
    COLOR_WARNING = '\033[93m'
    COLOR_FAIL = '\033[91m'
    COLOR_NORM = '\033[0m'
    COLOR_BOLD = '\033[1m'
    COLOR_UNDERLINE = '\033[4m'

class NonInterferingStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        super().__init__()
        self.started = False

    def on_llm_start(self, *args, **kwargs):
        pass

    def on_llm_new_token(self, token: str, *args, **kwargs):
        if self.started == False:
            busy_indicator.stop()
            self.started = True
        sys.stdout.write(token)
        sys.stdout.flush()

class NonInterferingStreamHandlerBusyIndicator(StreamingStdOutCallbackHandler):
    def __init__(self, busy_indicator):
        super().__init__()
        self.busy_indicator = busy_indicator
        self.started = False

    def on_llm_start(self, *args, **kwargs):
        pass

    def on_llm_new_token(self, token: str, *args, **kwargs):
        time.sleep(0.1)
        busy_indicator.stop()
        time.sleep(0.1)
        sys.stdout.write(token)
        sys.stdout.flush()

def cleanup():
    global busy_indicator
    if busy_indicator:
        busy_indicator.stop()

def format_answer(text, width=80):
    """
    Format text to fit within a specified width, preserving word boundaries and paragraph structure.
    Handles multiple paragraphs and list items separately.
    
    Args:
    text (str): The input text to be formatted.
    width (int): The maximum width of each line. Defaults to 80.
    
    Returns:
    str: The formatted text with preserved paragraph structure.
    """
    # Split the text into paragraphs
    paragraphs = text.split('\n\n')
    
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Remove leading/trailing whitespace from the paragraph
        paragraph = paragraph.strip()
        
        # Check if the paragraph is a list item
        if paragraph.startswith(('- ', '* ', '• ', '1. ', '2. ')):
            # If it's a list item, wrap it with a hanging indent
            subsequent_indent = ' ' * (len(paragraph) - len(paragraph.lstrip()))
            wrapped = textwrap.fill(paragraph, width=width, subsequent_indent=subsequent_indent)
        else:
            # For regular paragraphs, wrap without any indent
            wrapped = textwrap.fill(paragraph, width=width)
        
        formatted_paragraphs.append(wrapped)
    
    # join the formatted paragraphs with double newlines
    return '\n\n'.join(formatted_paragraphs)

def format_answer_x(text, width=80):
    """
    Format text to fit within a specified width, preserving word boundaries.
    
    Args:
    text (str): The input text to be formatted.
    width (int): The maximum width of each line. Defaults to 80.
    
    Returns:
    str: The formatted text.
    """
    text = text.lstrip()
    wrapped_lines = textwrap.wrap(text, width=width)
    formatted_text = '\n'.join(wrapped_lines)
    
    return formatted_text

def get_ollama_client(url):
    return Client(host=url)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='privategpt: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source",
                        "-S",
                        action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream",
                        "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        help="Specify the model to use. Defaults to the value set in config.py."
    )

    return parser.parse_args()

def doit(args):
    conf = load_config()

    if args.model is None:
        args.model = conf.DEFAULT_MODEL

    model = args.model

#    logger = setup_logging(conf.LOG_FILE_CHAT)
    global busy_indicator
    busy_indicator = BrailleSpinner("Processing")
    atexit.register(cleanup)

    embeddings_model_name =  conf.EMBEDDINGS_MODEL_NAME
    persist_directory = conf.PERSIST_DIRECTORY
    target_source_chunks = conf.TARGET_SOURCE_CHUNKS

    ollama_client = get_ollama_client(conf.OLLAMA_URL)

    embeddings = HuggingFaceEmbeddings(model_name=conf.EMBEDDINGS_MODEL_NAME)

    print(f"Loading document vector database ...")
    print(f"Persist directory: {conf.PERSIST_DIRECTORY}")
    db = Chroma(
            persist_directory=conf.PERSIST_DIRECTORY,
            embedding_function=embeddings)
#    print(f"Done")
    print(f"Using LLM: {model}")

    target_source_chunks = int(conf.TARGET_SOURCE_CHUNKS)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    stream_handler = NonInterferingStreamHandler()
    callbacks = [] if args.mute_stream else [stream_handler]

#    llm = Ollama(model=model, callbacks=callbacks)
    llm = Ollama(model=model, base_url=conf.OLLAMA_URL, callbacks=callbacks)

    qa = RetrievalQA.from_chain_type(llm=llm,
                                     chain_type="stuff",
                                     retriever=retriever,
                                     return_source_documents= not args.hide_source,
                                     verbose=False)
    # Interactive questions and answers
    while True:
        print(f"\n{Colors.COLOR_GREEN}{Colors.COLOR_BOLD}{conf.ASK_ME_TEXT}{Colors.COLOR_NORM} ")
#        query = input(f"\n{Colors.COLOR_GREEN}{Colors.COLOR_BOLD}{conf.ASK_ME_TEXT}>{Colors.COLOR_NORM} ")
        query = input(f"> ")
        if query == "q" or query == "quit" or query == "quit()" or query == "/bye":
            break
        if query.strip() == "":
            continue

        # Get the answer from the chain
        start = time.time()

        stream_handler.started = False

        busy_indicator.start()
        def run_query():
            nonlocal res
            res = qa.invoke(query)

        res = None
        query_thread = threading.Thread(target=run_query)
        query_thread.start()
        query_thread.join()
        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        end = time.time()
        busy_indicator.stop()

        # print the result
        print(f"\n\n{Colors.COLOR_CYAN}{Colors.COLOR_BOLD}Question:{Colors.COLOR_NORM}")
        print(f"{Colors.COLOR_BOLD}{query}{Colors.COLOR_NORM}")
        formatted_answer = format_answer(answer)
        print(formatted_answer)

        # print the relevant sources used for the answer
        for document in docs:
            meta_data = document.metadata
            source = meta_data.get('source', 'N/A')
            page = meta_data.get('page', 'N/A')
            if isinstance(page, int):
                page += 1
            filename = os.path.basename(source)
            print(f"\n> From: {Colors.COLOR_FAIL}{filename}:{Colors.COLOR_NORM}")
            print(document.page_content)
            print(f"\nPage: {page}")

        print(f"\n\n{Colors.COLOR_CYAN}{Colors.COLOR_BOLD}Question:{Colors.COLOR_NORM}")
        print(f"{Colors.COLOR_BOLD}{query}{Colors.COLOR_NORM}")
        print(f"\nAnswer:")
        formatted_answer = format_answer(answer)
        print(formatted_answer)

        print(f"\nTime took: {end - start:.2f} seconds")
        print(f"LLM used: {args.model}")



if __name__ == "__main__":
    import sys
    from assistant_console_runner import parse_arguments
    args = parse_arguments()
#    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
#        parser.print_help()
#        sys.exit(0)
    doit(args)
