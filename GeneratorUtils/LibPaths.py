#!/usr/bin/env python3
import os
import pathlib

libRootPath = os.path.dirname(os.path.realpath(__file__))+"/../"
inputDir = libRootPath + "input/"
outputDir = libRootPath + "output/"
featuresDir = libRootPath + "shaders/features/"
utilsDir = libRootPath + "shaders/utils/"
wrappersDir = libRootPath + "GeneratorUtils/Wrappers/"
emptyShader = wrappersDir + "classic_shader.fs"
generatorIndex = libRootPath + "GeneratorUtils/shader_index.py"
indexFileLocation=libRootPath+"GeneratorUtils/"
indexName="shader_index.py"
docDir = libRootPath + "Doc/"
