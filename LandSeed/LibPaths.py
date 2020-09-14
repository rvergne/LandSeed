#!/usr/bin/env python3
import os
import pathlib

libRootPath = os.path.dirname(os.path.realpath(__file__+"/../../"))
libSrc = os.path.join(libRootPath,"src/")
inputDir = os.path.join(libRootPath, "input/")
outputDir = os.path.join(libRootPath,"output/")
featuresDir = os.path.join(libSrc,"shader_code/features/")
utilsDir = os.path.join(libSrc,"shader_code/utils/")
templatesDir = os.path.join(libSrc,"Templates/")
docDir = os.path.join(libRootPath,"Doc/")
