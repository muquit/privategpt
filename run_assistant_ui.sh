#!/bin/bash

#====================================================================
# start assistant streamlit web app to start browser or not
# muquit@muquit.com Sep-15-2024 
#====================================================================

set -e  # exit immediately if a command exits with a non-zero status

DIRNAME=$(dirname "$0")
S="streamlit"
APP="${DIRNAME}/assistant/assistant_ui.py"

show_usage() {
    echo "Usage: $0 [yes|no]"
    echo ""
    echo "Options:"
    echo "  yes    Start Streamlit and open browser (default)"
    echo "  no     Start Streamlit without opening a browser"
    echo "  -h, --help  Show this help message"
    echo ""
    echo "If 'no' is used, Streamlit will start without opening a browser."
    echo "This is useful when running the app on a remote system."
    echo "Ensure you've configured Ollama to bind to all network interfaces."
    echo "Refer to Ollama documentation and FAQ for configuration details."
}

# exit if streamlis not installed
if ! command -v "${S}" &> /dev/null; then
    echo "Error: Streamlit is not installed."
    echo "Please install it using: pip3 install streamlit"
    echo "Make sure you're using Python's virtual environment"
    exit 1
fi

echo "OK: ${S} is installed"

start_browser="yes"

if [[ $# -gt 1 ]]; then
    echo "Error: Too many arguments"
    show_usage
    exit 1
fi

if [[ $# -eq 1 ]]; then
    case "$1" in
        -h|--help)
            show_usage
            exit 0
            ;;
        yes|no)
            start_browser="$1"
            ;;
        *)
            echo "Error: Invalid argument '$1'"
            show_usage
            exit 1
            ;;
    esac
fi

if [[ ${start_browser} == "yes" ]]; then
    "${S}" run "${APP}"
else
    echo "Starting ${S} without opening a browser"
    "${S}" run "${APP}" --server.headless true
fi
