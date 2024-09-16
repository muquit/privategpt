#!/bin/bash

#====================================================================
# A help script for myself to copy files to other hosts in my 
# network excluding certian directories
# muquit@muquit.com Sep-15-2024 
#====================================================================
if (( $# != 1 )); then
    echo "Usage: $0 <hostname>"
    exit 1
fi
HOST="$1"
rsync -arv \
    --exclude=__pycache__ \
    --exclude=pvenv  \
    --exclude=.git \
    . \
    ${HOST}:gitdev/privategpt/
