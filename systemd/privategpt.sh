#!/bin/bash
########################################################################
# Script to start privategpt.
# A quick hasck for. 
# https://github.com/muquit/privategpt
########################################################################
# change
WORKING_DIR=/home/muquit/gitdev/privategpt
VENV_PATH=${WORKING_DIR}/pvenv
APP_PATH=${WORKING_DIR}/assistant/assistant_ui.py
PORT=8501

source "${VENV_PATH}/bin/activate"

streamlit run "${APP_PATH}" --server.headless true --browser.gatherUsageStats false --server.port ${PORT} 

deactivate
