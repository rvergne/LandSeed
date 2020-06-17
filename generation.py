#!/usr/bin/env python3
import os
import re
import sys
import queue

# Error code meaning :
#   1 : keyword missing in a file
#   2 : @END tag missing
#   3 : dependency not recognize

# Lib Paths
inputDir = "input/"
outputDir = "output/"
noisesDir = "shaders/utils/noises/"
featuresDir = "shaders/features/"
utilsDir = "shaders/utils/"
emptyShader = "generator/terrain_empty.fs"

availableFeatureList = []
libRootPath = ""

includedFeatures = [] # to register which feature we already added
includedDependencies = [] # to register which dependencies we already added

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

# TODO : better if prebuild index as include_name -> path_to_file
def includeDependency(dependencyName):
    global includedDependencies
    if not dependencyName in includedDependencies:
        includedDependencies.append(dependencyName)

        print("Including dependency "+dependencyName.lower()+"..")

        if "NOISE" in dependencyName: # noise case
            noiseName = (dependencyName.replace("NOISE_", "").split("_")[0].lower())
            noiseDimension = (dependencyName.replace("NOISE_", "").split("_")[1])
            dependencyFilePath = libRootPath+noisesDir+noiseName+"/"+noiseName+noiseDimension+".fs"
        elif "RANDOM" in dependencyName: # toolbox case
            dependencyFilePath = libRootPath+utilsDir+"random.fs" # TODO change this for more general architecture
        else:
            error("Dependency not recognized : "+dependencyName, 3)

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

def includeFeature(featureName):

    global includedFeatures
    if not featureName in includedFeatures:
        includedFeatures.append(featureName)
        featurePath = libRootPath+featuresDir+featureName+".fs"
        featureFile = open(featurePath, "r")
        featureFileContent = featureFile.readlines()
        featureFile.close()
        line = 0
        line = skipUntil(featureFileContent, "@"+featureName.upper(), featurePath.replace(libRootPath, ""))
        line += 1

        while "@INCLUDE" in featureFileContent[line]: # get dependency name by parsing the line (getting what is after the "@INCLUDE ")
            p = re.compile("@INCLUDE (.*)")
            result = p.search(featureFileContent[line]).group(1)
            includeDependency(result)
            line += 1

        print("Including feature "+featureName+"...")
        copyUntilEnd(featureFileContent, line, featurePath.replace(libRootPath,""))


def includeTerrainMap(input, outputFile):
    # include what is necessary
    line = 0
    line = skipUntil(input, "@FEATURES", "input/input.fs")

    while (line < len(input)) and not "@END" in input[line] : # add each features detected and her dependencies
        for feature in availableFeatureList :
            if feature in input[line]:
                includeFeature(feature)
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

def getAvailableFeatures():
    availableFeatureFile = os.listdir(libRootPath+featuresDir)
    for i in range(len(availableFeatureFile)):
        availableFeatureFile[i] = os.path.splitext(availableFeatureFile[i])[0]
    return availableFeatureFile

def main():
    global libRootPath
    libRootPath=os.path.dirname(os.path.realpath(__file__))+"/"
    global availableFeatureList
    availableFeatureList = getAvailableFeatures()

    # user can enter a personnal input file or use the default one TODO : bug si fichier inexistant
    if len(sys.argv)==1:
        inputPath = libRootPath+inputDir+"input.fs"
        print("Default input file is taken : "+inputPath)
    else:
        inputPath = libRootPath+sys.argv[1]
        print("Input file : "+inputPath)


    inputFile = open(inputPath, "r")
    inputFileContent = inputFile.readlines()
    inputFile.close()
    emptyShaderFile = open(libRootPath+emptyShader, "r")
    emptyShaderContent = emptyShaderFile.readlines()
    emptyShaderFile.close()
    outputPath = libRootPath+outputDir+"fragment_shader01.fs"
    print("Output path : "+outputPath)
    if os.path.exists(outputPath):
        os.remove(outputPath)
    global outputFile
    outputFile = open(outputPath, "w")

    copyAndComplete(emptyShaderContent, inputFileContent)

    outputFile.close()

main()
