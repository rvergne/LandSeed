#!/bin/bash
virtualenv -p python3 ../LandSeed-venv
source ../LandSeed-venv/bin/activate
pip install .
cp LandSeed/input/input.frag ../LandSeed-venv/input.frag
cd ../LandSeed-venv/
LandSeed input.frag output/ && python3 output/viewer.py
cd ../
deactivate
rm -rf LandSeed-venv/
cd LandSeed
