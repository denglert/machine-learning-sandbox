#!/usr/bin/env bash

source setup.sh

PORT=$1

if  [ -z "${PORT}" ]; then
    PORT=8888
fi

echo "PORT=$PORT"

jupyter notebook --no-browser --port=${PORT}
