#!/usr/bin/env bash

source setup.sh

PORT=$1
BROWSER=$2

if  [ -z "${PORT}" ]; then
	PORT=8888
	echo "PORT=${PORT}"
fi


if  [ -z "${BROWSER}" ]; then
	echo "No browser selected."
	jupyter notebook --no-browser --port=${PORT}

else
	echo "BROWSER=${BROWSER}"
	jupyter notebook --browser=${BROWSER} --port=${PORT}
fi


