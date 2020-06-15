#!/usr/bin/env python3
import os
import re
import sys
import queue

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

# TODO : better if prebuild index as include_name -> path_to_file
def includeDependency(dependencyName, output):
    global includedDependencies
    if not dependencyName in includedDependencies:
        includedDependencies.append(dependencyName)

        print("Including dependency "+dependencyName.lower()+"..")

        if "NOISE" in dependencyName: # noise case
            noiseName = (dependencyName.replace("NOISE_", "").split("_")[0].lower())
            noiseDimension = (dependencyName.replace("NOISE_", "").split("_")[1])
            dependencyFilePath = libRootPath+noisesDir+noiseName+"/"+noiseName+noiseDimension+".fs"
        else: # toolbox case
            dependencyFilePath = libRootPath+utilsDir+"random.fs" # TODO change this for more general architecture

        dependencyFile = open(dependencyFilePath, "r")
        dependencyFileContent = dependencyFile.readlines()
        line = 0

        while not dependencyName in dependencyFileContent[line]: # skip lines until the dependency name is found
            line += 1
        line += 1
        while "@INCLUDE" in dependencyFileContent[line]: # include other dependencies recursively
            p = re.compile("@INCLUDE (.*)")
            result = p.search(dependencyFileContent[line]).group(1)
            includeDependency(result, output)
            line += 1
        while not "@END" in dependencyFileContent[line]:
            output.write(dependencyFileContent[line])
            line += 1
        dependencyFile.close()
        output.write("\n")

def includeFeature(featureName, output):

    global includedFeatures
    if not featureName in includedFeatures:
        includedFeatures.append(featureName)
        featurePath = libRootPath+featuresDir+featureName+".fs"
        featureFile = open(featurePath, "r")
        featureFileContent = featureFile.readlines()
        line = 0

        while not "@"+featureName.upper() in featureFileContent[line]: # skip spec part
            line +=1
        line += 1

        while "@INCLUDE" in featureFileContent[line]: # get dependency name by parsing the line (getting what is after the "@INCLUDE ")
            p = re.compile("@INCLUDE (.*)")
            result = p.search(featureFileContent[line]).group(1)
            includeDependency(result, output)
            line += 1

        print("Including feature "+featureName+"...")
        while not "@END" in featureFileContent[line]: # copy the feature function in output
            output.write(featureFileContent[line])
            line +=1
        output.write("\n")


def includeTerrainMap(input, outputFile):
    # include what is necessary
    line = 0

    while not "FEATURES" in input[line] : # go forward in the terrainMap function until FEATURES part
        line += 1
    while not "END" in input[line] : # add each features detected and her dependencies
        for feature in availableFeatureList :
            if feature in input[line]:
                includeFeature(feature, outputFile)
        line +=1

    for line in input : # finally copy the terrainMap function after adding all dependencies
        if not "TODO" in line:
            outputFile.write(line)
    outputFile.write("\n")


# copy the empty shader into the output shader and detect where includes have to be done
def copyAndComplete(emptyShader, input, outputFile):
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
    emptyShaderFile = open(libRootPath+emptyShader, "r")
    emptyShaderContent = emptyShaderFile.readlines()
    outputPath = libRootPath+outputDir+"fragment_shader01.fs"
    print("Output path : "+outputPath)
    if os.path.exists(outputPath):
        os.remove(outputPath)
    outputFile = open(outputPath, "w")

    copyAndComplete(emptyShaderContent, inputFileContent, outputFile)

    outputFile.close()
    emptyShaderFile.close()
    inputFile.close()

main()
