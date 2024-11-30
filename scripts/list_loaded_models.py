#!/usr/bin/env python3

########################################################################
# List loaded model to ollama. ollama Python package was updated from 
# 0.3.3 to 0.4.2 which changed how model information is returned from the 
# API
# muquit@muquit.com Nov-29-2024 
########################################################################

import sys
import os
import json
from typing import Optional
import ollama
from ollama import Client

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from utils.load_config import load_config

def test_ollama_connection(url: str = "http://localhost:11434") -> bool:
    try:
        client = Client(host=url)
        print(f"✓ Successfully connected to Ollama at {url}")
        return True
    except Exception as e:
        print(f"✗ Failed to connect to Ollama at {url}")
        print(f"Error: {str(e)}")
        return False

def get_ollama_models(url: str = "http://localhost:11434") -> Optional[list]:
    # get list of available models from Ollama
    try:
        client = Client(host=url)
        response = client.list()
        print("\nRaw API Response:")
        print(str(response))
        
        print("\nAttempting to parse models...")
        models = []
        
        try:
            if hasattr(response, 'models'):
                print("Found 'models' attribute")
                # Use 'model' attribute instead of 'name'
                models = [model.model for model in response.models]
            elif isinstance(response, (list, tuple)):
                print("Response is a list/tuple")
                models = [model.model for model in response]
            else:
                print(f"Unknown response format. Type: {type(response)}")
                return None
        except Exception as parse_error:
            print(f"Error parsing response: {parse_error}")
            return None
            
        return models
    except Exception as e:
        print(f"Error getting models: {str(e)}")
        print(f"Exception type: {type(e)}")
        return None

def print_model_info(models: list) -> None:
    if not models:
        print("\n✗ No models found")
        return
        
    print("\nFound Models:")
    print("-" * 40)
    for idx, model in enumerate(models, 1):
        print(f"{idx}. {model}")
    print("-" * 40)
    print(f"Total models found: {len(models)}")

def main():
    conf = load_config()
    print("Ollama Diagnostic Tool")
    print("=" * 50)
    
    default_url = conf.OLLAMA_URL
    if test_ollama_connection(default_url):
        models = get_ollama_models(default_url)
        if models is not None:
            print_model_info(models)

if __name__ == "__main__":
    main()
