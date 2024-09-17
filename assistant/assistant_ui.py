#!/usr/bin/env python3

#==================================================================== 
# It's an OpenSource RAG application that uses ollama
# https://muquit.com/ for source and project info
#==================================================================== 

"""
The document retrieval code is based on:
https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt
I wrote the web ui using streamlit
"""


import os
import sys

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.callbacks.base import BaseCallbackHandler

# by default chromadb sends telemetry info
# turn it off. 
# muquit@muquit.com Aug-28-2024 
os.environ["ANONYMIZED_TELEMETRY"] = "false"

from langchain_chroma import Chroma

from langchain_community.llms import Ollama

# Suppress warnings
import warnings
from transformers import logging
warnings.filterwarnings("ignore", category=FutureWarning, message=".*`clean_up_tokenization_spaces`.*")
logging.set_verbosity_error()

import socket

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

#from logging.handlers import RotatingFileHandler

from utils.load_config import load_config
from utils.logging import setup_logging

def doit():
    conf = load_config()
    logger = setup_logging(conf.LOG_FILE_CHAT)

    logger.info(f"Starting {conf.VERSION}")

    def print_header():
        st.markdown("""
        <style>
        .centered {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

        APP_TITLE = "Private Documents Assistant"
        url_line = f'<br><a href="{conf.PROJECT_URL}" target="_blank" style="font-style: italic; font-weight: normal;">{conf.PROJECT_URL}</a>' if conf.SHOW_PROJECT_URL else ''

        logger.info(f"URL line: {url_line}")

        st.markdown(f"""
        <div class="centered">
            <h2>{APP_TITLE}</h2>
            <p style='font-size: 0.9em; font-weight: bold;'>
            An OpenSource on-premises ML-powered
            Retrieval-Augmented Generation (RAG) application with ollama{url_line}
            </p>
        </div>
        """, unsafe_allow_html=True)



    # Streamlit callback handler for streaming responses
    class StreamHandler(BaseCallbackHandler):
        def __init__(self, container):
            self.container = container
            self.text = ""

        def on_llm_new_token(self, token: str, **kwargs) -> None:
            self.text += token
            self.container.markdown(self.text)

    # load configuration. look at config.py at the base of the project

    # initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'qa' not in st.session_state:
        st.session_state.qa = None

    # sidebar for configuration
    if conf.SHOW_SIDEBAR == False:
        st.set_page_config(initial_sidebar_state="collapsed")
    st.sidebar.title("Configuration")
    model = st.sidebar.selectbox("Select Model", ["mistral", "llama3"], index=0)
    embeddings_model_name = conf.EMBEDDINGS_MODEL_NAME
    hide_source = st.sidebar.checkbox("Hide Source", value=False)

    # print the header first
    print_header()

    # initialize embeddings and database
    @st.cache_resource(show_spinner=False)
    def initialize_qa(model, embeddings_model_name, hide_source):
        logger.info("Initializing QA ...")
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        db = Chroma(persist_directory=conf.PERSIST_DIRECTORY, embedding_function=embeddings)
        doc_count = db._collection.count()
        if doc_count == 0:
            centered_text = f"<div style='text-align: center;'>The document database is empty. Please ingest documents before querying.</div>"
            st.markdown(centered_text, unsafe_allow_html=True)
        else:
            centered_text = f"<div style='text-align: center;'>Document database contains {doc_count} chunks of text.</div>"
            st.markdown(centered_text, unsafe_allow_html=True)

        retriever = db.as_retriever(search_kwargs={"k": conf.TARGET_SOURCE_CHUNKS})
        logger.debug(f"Retriever: {retriever}")
        logger.debug(f"Number of documents in Chroma: {retriever.vectorstore._collection.count()}")
        llm = Ollama(model=model, base_url=conf.OLLAMA_URL)
        qa = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=retriever, 
            return_source_documents=True,
            verbose=True
        )
        logger.debug(f"QA chain return_source_documents: {qa.return_source_documents}")
        return qa

    # initialize or update QA when configuration changes
    if (st.session_state.qa is None or
        model != st.session_state.get('model') or
        embeddings_model_name != st.session_state.get('embeddings_model') or
        hide_source != st.session_state.get('hide_source')):
        
        if (st.session_state.qa is None or
            model != st.session_state.get('model') or
            embeddings_model_name != st.session_state.get('embeddings_model') or
            hide_source != st.session_state.get('hide_source')):    
         with st.spinner("Initializing ..."):
            st.session_state.qa = initialize_qa(model, embeddings_model_name, hide_source)
            st.session_state.model = model
            st.session_state.embeddings_model = embeddings_model_name
            st.session_state.hide_source = hide_source

    # display conversation history
    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # input
    if prompt := st.chat_input("Ask me anything about your documents", key="user_input"):
        st.session_state.conversation.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # generate and display response
        with st.chat_message("assistant"):
            response_container = st.empty()
            stream_handler = StreamHandler(response_container)
            # __call__ method is deprecated, use invoke instead.
            with st.spinner('Processing...'):
                response = st.session_state.qa.invoke(
                    input={"query": prompt},
                    callbacks=[stream_handler]
                )
            
            logger.info(f"Question: {prompt}")
            logger.info(f"Debug - Full response: {response}")
            logger.info(f"Debug - Response type: {type(response)}")
            
            if isinstance(response, dict):
                answer = response['result']
                source_documents = response.get('source_documents', [])
                logger.info(f"Debug - Response is a dict. Answer: {answer[:100]}...")
                logger.info(f"Debug - Source documents found: {len(source_documents)}")
            else:
                answer = str(response)
                logger.info(f"Debug - Response is not a dict. Full response: {answer[:100]}...")
                try:
                    source_documents = st.session_state.qa.retriever.get_relevant_documents(prompt)
                    logger.info(f"Debug - Source documents retrieved from retriever: {len(source_documents)}")
                except Exception as e:
                    logger.error(f"Debug - Error retrieving source documents: {str(e)}")
                    source_documents = []

            logger.info(f"Answer: {answer}")

            # __call__ method is deprecated, use invoke instead. But 
            # we must update the response container with the final 
            # answer 
            # Sep-16-2024 
            response_container.markdown(answer)
            st.session_state.conversation.append({"role": "assistant", "content": answer})

            if not hide_source:
                if source_documents:
                    st.write("Sources:")
                    for idx, doc in enumerate(source_documents):
                        with st.expander(f"Source {idx + 1}"):
                            st.write(f"From: {doc.metadata.get('source', 'Unknown')}")
                            st.write(doc.page_content)
                    logger.info(f"Debug - Displayed {len(source_documents)} source documents")
                else:
                    st.write("No source documents found for this query.")
                    logger.info("Debug - No source documents to display")
            else:
                logger.info("Debug - Source display is hidden")            

    logger.debug(f"hide_source value: {hide_source}")
    logger.debug(f"qa chain type: {type(st.session_state.qa)}")
    #logger.debug(f"qa chain attributes: {dir(st.session_state.qa)}")

    # button to clear conversation history (only shown if there's a 
    # conversation)
    if st.session_state.conversation:
        if st.button("Clear Conversation"):
            st.session_state.conversation = []
            st.rerun()

if __name__ == "__main__":
    doit()
