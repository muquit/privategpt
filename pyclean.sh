#!/bin/bash
# muquit@muquit.com 
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -print
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
