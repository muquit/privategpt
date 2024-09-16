#!/bin/bash
#==================================================================== 
# muquit@muquit.com Sep-14-2024 
#==================================================================== 
DIRNAME=$(dirname $0)
source ${DIRNAME}/pvenv/bin/activate
${DIRNAME}/ingest/ingest.py
