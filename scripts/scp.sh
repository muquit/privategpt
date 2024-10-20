#!/bin/bash

#====================================================================
# A helper script for myself to copy files to other hosts in my 
# network excluding certian directories
# muquit@muquit.com Sep-15-2024 
#====================================================================
if (( $# != 2 )); then
    echo "Usage: $0 <hostname> <directory>"
    echo "Eample: $0 host junk"
    echo "junk/privategpt must not exist"
    exit 1
fi
HOST="$1"
DIR="$2/privategpt/"
# make sure directory does not exist
if ssh ${HOST} "[ -d ${DIR} ] && exit 0 || exit 1"; then
    echo "ERROR: The directory ${DIR} exists on ${HOST}, exiting ..."
    echo "       Remove the directory first ..."
    exit 0
else
    echo "OK The directory ${DIR} does not exist on ${HOST}"
    echo "Continute with copying ..."
fi

rsync -arv \
    --exclude=__pycache__ \
    --exclude=pvenv  \
    --exclude=.git \
    . \
    ${HOST}:${DIR}
