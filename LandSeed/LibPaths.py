#!/usr/bin/env python3
import os
import pathlib

libRootPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..")
docDir = os.path.join(libRootPath,"Doc")
inputDir = os.path.join("input")
outputDir = os.path.join("output")
featuresDir = os.path.join("data","shader_code","features")
utilsDir = os.path.join("data","shader_code","utils")
templatesDir = os.path.join("data","Templates")
