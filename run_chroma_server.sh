#!/bin/bash
# muquit@muquit.com Sep-19-2024 
DIRNAME=$(dirname $0)
DB=${DIRNAME}/assistant/db
PORT=8002

chroma run --path ${DB} --port ${PORT}
