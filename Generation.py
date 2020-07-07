#!/usr/bin/env python3
import sys
if sys.version_info.major < 3: # python version should be 3+
    print("Python version to old, please upgrade your python to 3 or more.")
    sys.exit(6)
import os
import re
import queue
if sys.version_info.minor >= 4:
    import importlib
else:
    import imp
from UpdateIndex import shouldUpdateIndex, createIndex
from GeneratorUtils.LibPaths import libRootPath, inputDir, outputDir, featuresDir, utilsDir, emptyShader, generatorIndex

# Return code meaning :
#   0 : everything's ok
#   1 : keyword missing in a file
#   2 : path error
#   3 : dependency not recognize
#   4 : script parameter error
#   5 : index file error
#   6 : Python version too old

sys.path.append(libRootPath)

includedFeatures = [] # to register which feature we already added
includedDependencies = [] # to register which dependencies we already added

# check if we need to update index (function from UpdateIndex.py)
if shouldUpdateIndex():
    # in the shouldUpdateIndex function, if the index exist we have to import it to check that all features and utils are still there
    # so after re create it, we need to reload the module cause it has change
    print("Index outdated (some features or utils has changed).\nUpdating index..")
    if os.path.exists(generatorIndex):
        createIndex()
        # the generatorUtils.shader_index package is imported in shouldUpdateIndex functions so we need to reload it to get last version
        if sys.version_info.minor >= 4:
            importlib.reload(sys.modules["GeneratorUtils.shader_index"])
        else:
            imp.reload(sys.modules["GeneratorUtils.shader_index"])
    else:
        createIndex()

try:
    from GeneratorUtils.shader_index import dictTagToPath, dictFeatureFunctionToTag # importing pre-built dict containing key-value as TAG-PATH
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
    outputFile.write("#line "+str(start+1)+" \""+fileName+"\"\n")
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

# include a dependency a the dependencies of this dependency recursively
def includeDependency(dependencyName):
    global includedDependencies
    # if this dependency hasn't been added yet
    if not dependencyName in includedDependencies and not dependencyName in includedFeatures:
        includedDependencies.append(dependencyName)

        # check if the dependency name refer to an existing dependency
        if not dependencyName in dictTagToPath:
            error("Dependency not recognized : "+dependencyName, 3)
        # get dependency content
        dependencyFilePath = libRootPath+dictTagToPath[dependencyName]
        dependencyFile = open(dependencyFilePath, "r")
        dependencyFileContent = dependencyFile.readlines()
        dependencyFile.close()
        line = 0
        line = skipUntil(dependencyFileContent, "@"+dependencyName, dependencyFilePath.replace(libRootPath, ""))
        line += 1

        # include dependencies
        while "@INCLUDE" in dependencyFileContent[line]: # include other dependencies recursively
            p = re.compile("@INCLUDE (.*)")
            result = p.search(dependencyFileContent[line]).group(1)
            includeDependency(result)
            line += 1

        # finally copy the dependency after every dependencies have been added
        print("Including dependency "+dependencyName+"..")
        copyUntilEnd(dependencyFileContent, line, dependencyFilePath.replace(libRootPath, ""))

# include a feature, starting by including all the dependencies
def includeFeature(featureTag):
    global includedFeatures
    # if we didn't already add this feature
    if not featureTag in includedFeatures:
        includedFeatures.append(featureTag) # keep this feature in added features
        # get feature content
        featurePath = libRootPath+dictTagToPath[featureTag]
        featureFile = open(featurePath, "r")
        featureFileContent = featureFile.readlines()
        featureFile.close()
        line = 0
        line = skipUntil(featureFileContent, "@"+featureTag, featurePath.replace(libRootPath, ""))
        line += 1

        # include feature dependency by parsing the line (getting what is after the "@INCLUDE ")
        while "@INCLUDE" in featureFileContent[line]:
            p = re.compile("@INCLUDE (.*)")
            result = p.search(featureFileContent[line]).group(1)
            includeDependency(result)
            line += 1

        # finally copy the feature after every dependencies have been added
        print("Including feature "+featureTag+"...")
        copyUntilEnd(featureFileContent, line, featurePath.replace(libRootPath,""))

# start including input.
# Run two times through the input file's line
# the first time, detect every features used and include them
# the second time, assuming all dependencies have been included, copy the terrainMap function.
def includeTerrainMap(input, outputFile):
    # include what is necessary
    line = 0
    line = skipUntil(input, "@FEATURES", "input/input.fs") # get the line number where is the keyword FEATURES

    # add each features detected and her dependencies
    # for each not commented lines, if there is a feature in it, call includeFeature
    while (line < len(input)) and not "@END" in input[line] :
         #if the line is not commented
        if not "//" in input[line].replace(" ", "")[0:2]:
            # check every features
            for feature in dictFeatureFunctionToTag :
                # if the feature is in the line, include it
                if feature in input[line] and (input[line].replace(" ", "")[input[line].replace(" ", "").find(feature)+len(feature)]=="("):
                    includeFeature(dictFeatureFunctionToTag[feature])
        line +=1

    # if we have reached the end of the file without finding any @END tag
    if line >= len(input):
        error("@END tag missing in input/input.fs file", 2)

    outputFile.write("#line 1 \""+inputPath.replace(libRootPath, "")+"\"\n")
    # finally copy the terrainMap function after adding all dependencies
    for line in input :
        outputFile.write(line)
    outputFile.seek(0) # used in order to readlines again to count the number of lines
    outputFile.write("#line "+str(len(outputFile.readlines())+2)+" \""+outputPath.replace(libRootPath, "")+"\"\n") # replace GLSL line counter as it should be
    outputFile.write("\n")


# copy the wrapper into the output shader and detect where includes have to be done
def copyAndComplete(emptyShader, input):
    # run through every lines of the wrapper, seeking for the @TERRAIN_MAP tag.
    # if it's not present, copy the current line then go on the next one
    # if it's on the line, include the input and all the dependencies
    for line in range(len(emptyShader)):
        if not "@TERRAIN_MAP" in emptyShader[line]:
            if line == 1:
                outputFile.write("#line 3 \""+outputPath.replace(libRootPath, "")+"\"\n")
            outputFile.write(emptyShader[line])
        else :
            includeTerrainMap(input, outputFile)


def main():
    # user can enter a personnal input file or use the default one
    global outputPath
    global inputPath
    # no parameters -> default input and output
    if len(sys.argv)==1:
        inputPath = inputDir+"input.fs"
        outputPath = outputDir+"fragment_shader01.fs"
        print("Default input file is taken : "+inputPath.replace(libRootPath, ""))
        print("Default output file is taken : "+outputPath.replace(libRootPath, ""))
    # parameters given
    elif len(sys.argv)==3:
        inputPath = libRootPath+sys.argv[1]
        print("Input file : "+inputPath)
        outputPath = libRootPath+sys.argv[2]
        print("Output file : "+outputPath)
    # wrong number of parameters
    else:
        print("Parameter error.")
        print("Syntax : ")
        print("python generation.py [inputPath] [outputPath]")
        print("or")
        print("python generation.py")
        sys.exit(4)

    # checking that input exist and that it's a file
    if not os.path.exists(inputPath) or not os.path.isfile(inputPath):
        print("Please enter a valid or existing input file.")
        sys.exit(4)
    # checking that if output file exist, it's a file
    if os.path.exists(outputPath) and not os.path.isfile(outputPath):
        print("Please enter a valid or non existing output file.")
        sys.exit(4)
    # checking that the path to the output file exist, if not, create it
    if not os.path.exists(os.path.dirname(outputPath)):
        # TODO create dir
        print("WORK IN PROGRESS : create path to the output file")

    # opening and getting input file content
    inputFile = open(inputPath, "r")
    inputFileContent = inputFile.readlines()
    inputFile.close()

    # if output file exists, remove it, then open it
    if os.path.exists(outputPath):
        os.remove(outputPath)
    global outputFile
    outputFile = open(outputPath, "w+")

    # getting wrapper content
    emptyShaderFile = open(emptyShader, "r")
    emptyShaderContent = emptyShaderFile.readlines()
    emptyShaderFile.close()

    # fulfill wrapper with input file and dependencies
    copyAndComplete(emptyShaderContent, inputFileContent)

    # close output file and exit
    outputFile.close()
    sys.exit(0)

main()
