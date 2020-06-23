#!/usr/bin/env python3
import os
import re
import sys
import queue
if sys.version_info.minor >= 4:
    import importlib
else:
    import imp
from updateIndex import shouldUpdateIndex, createIndex

# Return code meaning :
#   0 : everything's ok
#   1 : keyword missing in a file
#   2 : @END tag missing
#   3 : dependency not recognize
#   4 : script parameter error
#   5 : index file error

# Lib Paths
libRootPath=os.path.dirname(os.path.realpath(__file__))+"/" # get lib absolute path
inputDir = libRootPath + "input/"
outputDir = libRootPath + "output/"
featuresDir = libRootPath + "shaders/features/"
utilsDir = libRootPath + "shaders/utils/"
emptyShader = libRootPath + "generatorUtils/terrain_empty.fs"
generatorIndex = libRootPath + "generatorUtils/shader_index.py"

availableFeatureList = []

includedFeatures = [] # to register which feature we already added
includedDependencies = [] # to register which dependencies we already added

if shouldUpdateIndex():
    print("Index outdated (some features or utils has changed).\nUpdating index..")
    if os.path.exists(generatorIndex):
        createIndex()
        # the generatorUtils.shader_index package is imported in shouldUpdateIndex functions so we need to reload it to get last version
        if sys.version_info.minor >= 4:
            importlib.reload(sys.modules["generatorUtils.shader_index"])
        else:
            imp.reload(sys.modules["generatorUtils.shader_index"])
    else:
        createIndex()

try:
    from generatorUtils.shader_index import dictTagToPath, dictFeatureFunctionToTag # importing pre-built dict containing key-value as TAG-PATH
except:
    print("Error while executing updateIndex script. Please fix it manualy")
    sys.exit(5)


# Return index of the line where keyword has been found. Create an error and leave script if the keyword is not found
# fileContent : where to search
# keyword : what to search
# filename : name of the file with his path inside the lib for error printing
def skipUntil(fileContent, keyword, fileName):
    line = 0
    while (line < len(fileContent)) and (not keyword in fileContent[line]): # skipe until keyword is found or EOF is reached
        line += 1
    if line >= len(fileContent):
        error("Keyword " + keyword + " not found in " + fileName, 1)
    else:
        return line

# Copy fileContent in the outputFile starting at start line.
# fileName is the filename where your searching with his path in the lib. For error printing
def copyUntilEnd(fileContent, start, fileName):
    line = start
    while (line < len(fileContent)) and (not "@END" in fileContent[line]):
        outputFile.write(fileContent[line])
        line += 1
    if line >= len(fileContent):
        error("@END tag missing in "+fileName, 2)
    else:
        outputFile.write("\n")

# Exit the script properly with errMessage printed and the code errCode
def error(errorMessage, errCode):
    print(errorMessage)
    outputFile.close()
    sys.exit(errCode)

def includeDependency(dependencyName):
    global includedDependencies
    if not dependencyName in includedDependencies:
        includedDependencies.append(dependencyName)

        print("Including dependency "+dependencyName+"..")

        if not dependencyName in dictTagToPath:
            error("Dependency not recognized : "+dependencyName, 3)
        dependencyFilePath = libRootPath+dictTagToPath[dependencyName]

        dependencyFile = open(dependencyFilePath, "r")
        dependencyFileContent = dependencyFile.readlines()
        dependencyFile.close()
        line = 0
        line = skipUntil(dependencyFileContent, "@"+dependencyName, dependencyFilePath.replace(libRootPath, ""))
        line += 1
        while "@INCLUDE" in dependencyFileContent[line]: # include other dependencies recursively
            p = re.compile("@INCLUDE (.*)")
            result = p.search(dependencyFileContent[line]).group(1)
            includeDependency(result)
            line += 1
        copyUntilEnd(dependencyFileContent, line, dependencyFilePath.replace(libRootPath, ""))

def includeFeature(featureTag):

    global includedFeatures
    if not featureTag in includedFeatures:
        includedFeatures.append(featureTag)
        featurePath = libRootPath+dictTagToPath[featureTag]
        featureFile = open(featurePath, "r")
        featureFileContent = featureFile.readlines()
        featureFile.close()
        line = 0
        line = skipUntil(featureFileContent, "@"+featureTag, featurePath.replace(libRootPath, ""))
        line += 1

        while "@INCLUDE" in featureFileContent[line]: # get dependency name by parsing the line (getting what is after the "@INCLUDE ")
            p = re.compile("@INCLUDE (.*)")
            result = p.search(featureFileContent[line]).group(1)
            includeDependency(result)
            line += 1

        print("Including feature "+featureTag+"...")
        copyUntilEnd(featureFileContent, line, featurePath.replace(libRootPath,""))


def includeTerrainMap(input, outputFile):
    # include what is necessary
    line = 0
    line = skipUntil(input, "@FEATURES", "input/input.fs")

    while (line < len(input)) and not "@END" in input[line] : # add each features detected and her dependencies
        if not "//" in input[line].replace(" ", "")[0:2]:
            for feature in dictFeatureFunctionToTag :
                if feature in input[line]:
                    includeFeature(dictFeatureFunctionToTag[feature])
        line +=1
    if line >= len(input):
        error("@END tag missing in input/input.fs file", 2)

    for line in input : # finally copy the terrainMap function after adding all dependencies
        outputFile.write(line)
    outputFile.write("\n")


# copy the empty shader into the output shader and detect where includes have to be done
def copyAndComplete(emptyShader, input):
    for line in range(len(emptyShader)):
        if not "@TERRAIN_MAP" in emptyShader[line]:
            outputFile.write(emptyShader[line])
        else :
            includeTerrainMap(input, outputFile)


def main():
    # user can enter a personnal input file or use the default one
    if len(sys.argv)==1:
        inputPath = inputDir+"input.fs"
        outputPath = outputDir+"fragment_shader01.fs"
        print("Default input file is taken : "+inputPath)
        print("Default output file is taken : "+outputPath)
    elif len(sys.argv)==3:
        inputPath = libRootPath+sys.argv[1]
        print("Input file : "+inputPath)
        outputPath = libRootPath+sys.argv[2]
        print("Output file : "+outputPath)
    else:
        print("Parameter error.")
        print("Syntax : ")
        print("python generation.py [inputPath] [outputPath]")
        print("or")
        print("python generation.py")
        sys.exit(4)

    if not os.path.exists(inputPath) or not os.path.isfile(inputPath):
        print("Please enter a valid or existing input file.")
        sys.exit(4)
    if os.path.exists(outputPath) and not os.path.isfile(outputPath):
        print("Please enter a valid or non existing output file.")
        sys.exit(4)

    inputFile = open(inputPath, "r")
    inputFileContent = inputFile.readlines()
    inputFile.close()

    if os.path.exists(outputPath):
        os.remove(outputPath)
    global outputFile
    outputFile = open(outputPath, "w")

    emptyShaderFile = open(emptyShader, "r")
    emptyShaderContent = emptyShaderFile.readlines()
    emptyShaderFile.close()

    copyAndComplete(emptyShaderContent, inputFileContent)

    outputFile.close()
    sys.exit(0)

main()
