#!/bin/bash
#==================================================================== 
# muquit@muquit.com Sep-14-2024 
#==================================================================== 
DIRNAME=$(dirname $0)
source ${DIRNAME}/ingest/pvenv/bin/activate
ingest/ingest.py
