#!/bin/bash
# Muhammad.Muquit@cygnalabs.com Aug-12-2024 
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -print
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
