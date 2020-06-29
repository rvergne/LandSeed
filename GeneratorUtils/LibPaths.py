#!/usr/bin/env python3
import os
import pathlib

# libRootPath=str(pathlib.Path().absolute())+"/" # get lib absolute path
libRootPath = os.path.dirname(os.path.realpath(__file__))+"/../"
inputDir = libRootPath + "input/"
outputDir = libRootPath + "output/"
featuresDir = libRootPath + "shaders/features/"
utilsDir = libRootPath + "shaders/utils/"
emptyShader = libRootPath + "GeneratorUtils/terrain_empty.fs"
generatorIndex = libRootPath + "GeneratorUtils/shader_index.py"
indexFileLocation=libRootPath+"GeneratorUtils/"
indexName="shader_index.py"
docDir = libRootPath + "Doc/"
