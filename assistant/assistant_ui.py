#!/usr/bin/env python3

#==================================================================== 
# It's an OpenSource RAG application that uses ollama
# https://github.com/muquit/privategpt for source
# https://muquit.com/
#==================================================================== 

"""
The document retrieval code is based on:
https://github.com/ollama/ollama/tree/main/examples/langchain-python-rag-privategpt
I wrote the web ui using streamlit
"""


import os
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning:torch.classes'
import sys
import warnings
from typing import Any, Dict

import streamlit as st
import ollama
from ollama import Client
from streamlit.runtime.scriptrunner import get_script_run_ctx

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.callbacks.base import BaseCallbackHandler

# by default chromadb sends telemetry info
# turn it off. 
# muquit@muquit.com Aug-28-2024 
os.environ["ANONYMIZED_TELEMETRY"] = "false"

from langchain_chroma import Chroma

#from langchain_community.llms import Ollama
# updated: Nov-02-2024 
from langchain_ollama import OllamaLLM

# Suppress warnings
from transformers import logging
warnings.filterwarnings("ignore", category=FutureWarning, message=".*`clean_up_tokenization_spaces`.*")
logging.set_verbosity_error()

import socket

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

#from logging.handlers import RotatingFileHandler

from utils.load_config import load_config
from utils.logging import setup_logging

# use Client instead of ollama.list(). If ollama is running on a 
# remote host, ollama.list() uses default URL
# cache the call
@st.cache_resource
def get_ollama_client(url):
    return Client(host=url)


def doit():
    conf = load_config()
    logger = setup_logging(conf.LOG_FILE_CHAT)
    logger.info(f"Starting {conf.VERSION}")
    logger.info(f"ollama URL {conf.OLLAMA_URL}")

    # change title and icon
    # use the favicon.ico I designed for muquit.com early days of web when 
    # favicon was introduced
    st.set_page_config(
        page_title="privategpt",
        page_icon="assistant/m.ico",
        initial_sidebar_state="collapsed" if conf.SHOW_SIDEBAR == False else "expanded",
        layout="wide"
    )
    st.sidebar.title("Configuration")

    # get the client for listing
    ollama_client = get_ollama_client(conf.OLLAMA_URL)

    @st.cache_resource
    def print_header(conf):
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

        APP_TITLE = conf.APP_TITLE
        url_line = f'<br><a href="{conf.PROJECT_URL}" target="_blank" style="font-style: italic; font-weight: normal;">{conf.PROJECT_URL}</a>' if conf.SHOW_PROJECT_URL else ''

        logger.info(f"URL line: {url_line}")

        st.markdown(f"""
        <div class="centered">
            <h2>{APP_TITLE} v{conf.VERSION}</h2>
            <p style='font-size: 0.9em; font-weight: bold;'>
            {conf.APP_DESCRIPTION}{url_line}
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
            
        def on_chain_start( self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
            logger.info(f"chain started")

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

    # get the list of models
    logger.info(f"Listing models from ollama ...")
    all_models = [model["name"] for model in ollama_client.list()["models"]]
    models = [model for model in all_models if model not in conf.EXCLUDE_MODELS]

    # select the first model in the list as default
    model = st.sidebar.selectbox("Choose your model", models, index=0)
    
    # model to use for vectorizing texts
    embeddings_model_name = conf.EMBEDDINGS_MODEL_NAME

    # hide source checkbox
    hide_source = st.sidebar.checkbox("Hide Source", value=False)

    # print the header first
    print_header(conf)

    @st.cache_resource(show_spinner=False)
    def get_embeddings(model_name):
        return HuggingFaceEmbeddings(model_name=model_name)

    
    # initialize embeddings and database
    @st.cache_resource(show_spinner=False)
    def initialize_qa(model, embeddings_model_name, hide_source):
        logger.info("Initializing QA ...")
        embeddings = get_embeddings(embeddings_model_name)
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
        llm = OllamaLLM(model=model, base_url=conf.OLLAMA_URL)

        # if custom prompt specified use it.
        if hasattr(conf, 'CUSTOM_PROMPT'):
            custom_prompt = PromptTemplate(
                template=conf.CUSTOM_PROMPT,
                input_variables=["context", "question"]
            )
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                verbose=False,
                chain_type_kwargs={"prompt": custom_prompt}
            )
        else:
            qa = RetrievalQA.from_chain_type(
                llm=llm, 
                chain_type="stuff", 
                retriever=retriever, 
                return_source_documents=True,
                verbose=False
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
#            print("XXXXXXXXXXX")
#            print(f">>>>>>>>>>>>>>>> using model {model}")
#            print("XXXXXXXXXXX")
            st.session_state.qa = initialize_qa(model, embeddings_model_name, hide_source)
            st.session_state.model = model
            st.session_state.embeddings_model = embeddings_model_name
            st.session_state.hide_source = hide_source

    # display conversation history
    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # input
    if prompt := st.chat_input(conf.ASK_ME_TEXT, key="user_input"):
        st.session_state.conversation.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # generate and display response
        with st.chat_message("assistant"):
            response_container = st.empty()
            stream_handler = StreamHandler(response_container)
            # __call__ method is deprecated, use invoke instead.
            with st.spinner('Processing...'):
                # use invoke 
                # it is important use config with invoke otherwise
                # streamlit will not stream
                # Oct-20-2024 
                response = st.session_state.qa.invoke(
                        {"query": prompt},
                        config={"callbacks":[stream_handler]}
                 )
                # old __call__ way
#                response = st.session_state.qa(
#                    {"query": prompt},
#                    callbacks=[stream_handler]
#                )
            
#            logger.info(f"Question: {prompt}")
#            logger.info(f"Debug - Full response: {response}")
#            logger.info(f"Debug - Response type: {type(response)}")
            
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

##--            logger.info(f"Answer: {answer}")
            # Only log the answer if it's for a new question
#            if 'last_question' not in st.session_state or st.session_state.last_question != prompt:
#                logger.info(f"Question: {prompt}")
#                logger.info(f"Answer: {answer}")
#                st.session_state.last_question = prompt


            # __call__ method is deprecated, use invoke instead. But 
            # we must update the response container with the final 
            # answer 
            # Sep-16-2024 
            response_container.markdown(answer)
            st.session_state.conversation.append({"role": "assistant", "content": answer})

            if not hide_source:
                if source_documents:
                    st.markdown("**Sources:**")
                    for idx, doc in enumerate(source_documents):
                        with st.expander(f"Source {idx + 1}"):
                            meta_data = doc.metadata
                            # get the source and page if possible
                            source = meta_data.get('source', 'N/A')
                            page = meta_data.get('page', 'N/A')
                            filename = os.path.basename(source)
                            st.write(f"From: **{filename}**", unsafe_allow_html=True)
                            # write the source content
                            st.write(doc.page_content)
                            st.write(f"**Page**: {page}")
                    logger.info(f"Debug - Displayed {len(source_documents)} source documents")
                else:
                    st.write("No source documents found for this query.")
                    logger.info("Debug - No source documents to display")
            else:
                logger.info("Debug - Source display is hidden")            

    if model != st.session_state.get('model'):
        logger.debug(f"hide_source value: {hide_source}")
        logger.debug(f"qa chain type: {type(st.session_state.qa)}")
        logger.debug(f">>>>>>>>>>>>>>>> using model {model}")
        #logger.debug(f"qa chain attributes: {dir(st.session_state.qa)}")

    # button to clear conversation history (only shown if there's a 
    # conversation)
    if st.session_state.conversation:
        if st.button("Clear Conversation"):
            st.session_state.conversation = []
            st.rerun()

if __name__ == "__main__":
    doit()
