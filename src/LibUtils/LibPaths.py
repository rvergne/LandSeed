#!/usr/bin/env python3
import os
import pathlib

libRootPath = os.path.dirname(os.path.realpath(__file__+"/../../"))+"/"
libSrc = libRootPath+"src/"
inputDir = libRootPath + "input/"
outputDir = libRootPath + "output/"
featuresDir = libSrc + "shader_code/features/"
utilsDir = libSrc + "shader_code/utils/"
templatesDir = libSrc + "Templates/"
emptyShader = templatesDir + "classic_shader.frag"
generatorIndex = libSrc + "LibUtils/shader_index.py"
indexFileLocation = libSrc + "LibUtils/"
indexName="shader_index.py"
docDir = libRootPath + "Doc/"
