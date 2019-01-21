#!/usr/bin/env python

export PROJECT_DIR=$(pwd)

PYTHON_MODULES_DIR=${PROJECT_DIR}/python/modules/
export PYTHONPATH=${PYTHON_MODULES_DIR}:${PYTHONPATH}
