#!/bin/bash
set -e
VENV_PATH="LandSeed-venv/"
virtualenv -p python3 $VENV_PATH
source ${VENV_PATH}bin/activate
pip install .
cp LandSeed/input/input.frag ${VENV_PATH}input.frag
LandSeed ${VENV_PATH}input.frag ${VENV_PATH}output/ && python3 ${VENV_PATH}output/viewer.py
deactivate
rm -rf $VENV_PATH
