#!/usr/bin/env python3
import sys
if sys.version_info.major < 3: # python version should be 3+
    print("Python version to old, please upgrade your python to 3 or more.")
    sys.exit(6)
import os
import re
import queue
import shutil
if sys.version_info.minor >= 4:
    import importlib
else:
    import imp
from src.LibUtils.LibPaths import libRootPath, inputDir, outputDir, featuresDir, utilsDir, templatesDir
from src.LibUtils.TemplateInfoClass import TemplateInfo
from src.LibUtils.ShaderFragmentInfoClass import ShaderFragmentInfo

# Return code meaning :
#   0 : everything's ok
#   1 : keyword missing in a file or badly written
#   2 : path error
#   3 : dependency not recognize
#   4 : script parameter error
#   5 : index file error
#   6 : Python version too old

sys.path.append(libRootPath)

includedFeatures = [] # to register which feature we already added
includedDependencies = [] # to register which dependencies we already added

def writeLineDirective(line, file):
    if template.getLineDirective():
        outputFile.write("#line "+str(line)+" \""+file+"\"\n")

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

# Exit the script properly with errMessage printed and the code errCode
def error(errorMessage, errCode):
    print(errorMessage)
    if outputFile != None:
        outputFile.close()
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    sys.exit(errCode)

# include a dependency a the dependencies of this dependency recursively
def includeDependency(dependencyName):
    global includedFeatures
    global includedDependencies
    dependency = None
    # if this dependency hasn't been added yet
    if not dependencyName.lower() in includedDependencies and not dependencyName.lower() in includedFeatures:

        for feat in os.listdir(featuresDir):
            if feat.replace(".frag", "").upper() == dependencyName.upper():
                dependencyPath = os.path.join(featuresDir, feat)
                dependency = ShaderFragmentInfo("feature", dependencyPath)
                includedFeatures.append(dependencyName.lower())
                break
        if dependency == None:
            for util in os.listdir(utilsDir):
                if util.replace(".frag", "").upper() == dependencyName.upper():
                    dependencyPath = os.path.join(utilsDir, util)
                    dependency = ShaderFragmentInfo("utils", dependencyPath)
                    includedDependencies.append(dependencyName.lower())
                    break
        if dependency == None:
            error("Dependency not recognize : "+dependencyName, 3)

        for dep in dependency.getDependencies():
            includeDependency(dep)

        print("Including "+dependency.getCat()+" "+dependencyName+"...")
        writeLineDirective(dependency.getBeginLine()+1, dependencyPath.replace(libRootPath, ""))
        outputFile.write(dependency.getFunctionCode())


# start including input.
# Run two times through the input file's line
# the first time, detect every features used and include them
# the second time, assuming all dependencies have been included, copy the terrainMap function.
def includeTerrainMap(input, outputFile):
    # include what is necessary
    line = 0
    line = skipUntil(input, "@FEATURES", inputPath) # get the line number where is the keyword FEATURES

    # add each features detected and her dependencies
    # for each not commented lines, if there is a feature in it, call includeFeature
    while (line < len(input)) and not "@END" in input[line] :
         #if the line is not commented
        if not "//" in input[line].replace(" ", "")[0:2]:
            # check every features
            for featureFile in os.listdir(featuresDir) :
                feature = featureFile.replace(".frag","")
                # if the feature is in the line, include it
                if feature in input[line] and (input[line].replace(" ", "")[input[line].replace(" ", "").find(feature)+len(feature)]=="("):
                    includeDependency(feature)
            for utilFile in os.listdir(utilsDir) : # check util after feature
                util = utilFile.replace(".frag","")
                # if the util is in the line, include it
                if util in input[line] and (input[line].replace(" ", "")[input[line].replace(" ", "").find(util)+len(util)]=="("):
                    includeDependency(util)
        line +=1

    # if we have reached the end of the file without finding any @END tag
    if line >= len(input):
        error("@END tag missing in input/input.frag file", 2)
    writeLineDirective(1, inputPath.replace(libRootPath, ""))
    # finally copy the terrainMap function after adding all dependencies
    for line in input :
        outputFile.write(line)
    outputFile.seek(0) # used in order to readlines again to count the number of lines
    writeLineDirective(len(outputFile.readlines())+2, outputFilePath.replace(libRootPath, ""))
    outputFile.write("\n")


# copy the template into the output shader and detect where includes have to be done
# first analyze input file to get template and quality
def copyAndComplete(input):
    global template
    global outputFilePath
    templateName = None
    qualityValue = None
    firstLines = 0
    while firstLines < len(input) and (qualityValue == None or templateName == None):
        if "@QUALITY" in input[firstLines] and input[firstLines][input[firstLines].find("@QUALITY")+8] == " ":
            p = re.compile("@QUALITY (.*)")
            qualityValue = p.search(input[firstLines]).group(1)
            try:
                qualityValue = float(qualityValue)
            except Exception as e:
                error("@QUALITY param should be float in "+inputPath.replace(libRootPath, ""), 2)
        if "@TEMPLATE" in input[firstLines] and input[firstLines][input[firstLines].find("@TEMPLATE")+9] == " ":
            p = re.compile("@TEMPLATE (.*)")
            templateName = p.search(input[firstLines]).group(1)
            if not templateName in os.listdir(templatesDir):
                error("Unknown template name : "+templateName, 3)
        firstLines += 1
    if firstLines >= len(input):
        if templateName == None:
            error("Missing template declaration in input file.", 1)
        if qualityValue == None:
            error("Missing quality declaration in input file.", 1)
    print("Quality : "+str(qualityValue)+"/ 100 (Work in progress)")
    print("Template : "+templateName)

    templateDirPath=os.path.join(templatesDir, templateName)

    template = TemplateInfo(templateDirPath)
    # getting template content
    emptyShaderContent = template.getContent()
    shutil.copytree(templateDirPath, outputPath)

    outputFilePath=os.path.join(outputPath,(template.getPathToFileToFill().replace(template.getPath(), "")),template.getFileTofillName())

    # if output file exists, remove it, then open it
    if os.path.exists(outputFilePath):
        os.remove(outputFilePath)
    global outputFile
    outputFile = open(outputFilePath, "w+")

    outputFile.write("// @FROM "+inputPath.replace(libRootPath,"")+"\n")
    # run through every lines of the template, seeking for the @TERRAIN_MAP tag.
    # if it's not present, copy the current line then go on the next one
    # if it's on the line, include the input and all the dependencies
    # for line in range(line, len(emptyShaderContent)):
    for line in range(len(emptyShaderContent)):
        if not "@TERRAIN_MAP" in emptyShaderContent[line]:
            if line == 1:
                writeLineDirective(3, outputFilePath.replace(libRootPath, ""))
            outputFile.write(emptyShaderContent[line])
        else :
            includeTerrainMap(input, outputFile)
    outputFile.close()

# in order to make the genreation from another file
def generate(input, output):
    global outputPath # path to the output dir
    global outputFile # output file (the one where @TERRAIN_MAP is)
    global inputPath # path to the input file
    global includedFeatures
    global includedDependencies

    includedFeatures = [] # to register which feature we already added
    includedDependencies = [] # to register which dependencies we already added

    inputPath = os.path.join(libRootPath,input)
    print("Input file : "+inputPath)
    outputPath = os.path.join(libRootPath,output)
    print("Output file : "+outputPath)

    # checking that input exist and that it's a file
    if not os.path.exists(inputPath) or not os.path.isfile(inputPath):
        print("Please enter a valid or existing input file.")
        sys.exit(4)

    # opening and getting input file content
    inputFile = open(inputPath, "r")
    inputFileContent = inputFile.readlines()
    inputFile.close()

    outputFile = None

    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)

    # fulfill template with input file and dependencies
    copyAndComplete(inputFileContent)

    return 0

def main():
    global outputPath # path to the output dir
    global outputFile # output file (the one where @TERRAIN_MAP is)
    global inputPath # path to the input file
    # user can enter a personnal input file or use the default one
    # no parameters -> default input and output
    if len(sys.argv)==1:
        inputPath = os.path.join(inputDir,"input.frag")
        outputPath = outputDir
        print("Default input file is taken : "+inputPath.replace(libRootPath, ""))
        print("Default output directory is taken : "+outputPath.replace(libRootPath, ""))
    # parameters given
    elif len(sys.argv)==3:
        inputPath = os.path.join(libRootPath,sys.argv[1])
        print("Input file : "+inputPath)
        outputPath = os.path.join(libRootPath,sys.argv[2])
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

    # opening and getting input file content
    inputFile = open(inputPath, "r")
    inputFileContent = inputFile.readlines()
    inputFile.close()

    outputFile = None

    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)

    # fulfill template with input file and dependencies
    copyAndComplete(inputFileContent)

    # exit
    sys.exit(0)

if __name__=="__main__":
    main()
