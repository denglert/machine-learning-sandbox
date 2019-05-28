#!/usr/bin/env python

BASEDIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export MACHINELEARNING_SANDBOX_DIR=${BASEDIR}

PYTHON_MODULES_DIR=${MACHINELEARNING_SANDBOX_DIR}/python/modules/
export PYTHONPATH=${PYTHON_MODULES_DIR}:${PYTHONPATH}

# - Source toolbox
source ${MACHINELEARNING_SANDBOX_DIR}/toolbox/setup.sh
