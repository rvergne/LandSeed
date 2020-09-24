#!/usr/bin/env python3
import sys
if sys.version_info.major < 3: # python version should be 3+
    print("Python version to old, please upgrade your python to 3 or more.")
    raise PythonVersionException("Python version too old")
if sys.version_info.minor >= 4:
    import importlib
else:
    import imp
import os
from pydoc import locate
import re
import queue
import shutil
import pkg_resources
from LandSeed.LibPaths import libRootPath, inputDir, outputDir, featuresDir, utilsDir, templatesDir
from LandSeed.TemplateInfoClass import TemplateInfo
from LandSeed.ShaderFragmentInfoClass import ShaderFragmentInfo

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

        for feat in pkg_resources.resource_listdir("LandSeed", featuresDir):
            if feat.replace(".frag", "").upper() == dependencyName.upper():
                dependencyPath = os.path.join(featuresDir, feat)
                dependency = ShaderFragmentInfo("feature", dependencyPath)
                includedFeatures.append(dependencyName.lower())
                break
        if dependency == None:
            for util in pkg_resources.resource_listdir("LandSeed", utilsDir):
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
            for featureFile in pkg_resources.resource_listdir("LandSeed", featuresDir) :
                feature = featureFile.replace(".frag","")
                # if the feature is in the line, include it
                if feature in input[line] and (input[line].replace(" ", "")[input[line].replace(" ", "").find(feature)+len(feature)]=="("):
                    includeDependency(feature)
            for utilFile in pkg_resources.resource_listdir("LandSeed", utilsDir) : # check util after feature
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
def copyAndComplete(input):
    global template
    global outputFilePath
    templateName = None
    firstLines = 0
    while firstLines < len(input) and (templateName == None):
        if "@TEMPLATE" in input[firstLines] and input[firstLines][input[firstLines].find("@TEMPLATE")+9] == " ":
            inputFileTemplateLine = input[firstLines].replace("// ", "").replace("//", "").replace("\n", "").split(" ")
            templateName = inputFileTemplateLine[1]
            # if not templateName in os.listdir(templatesDir):
            if not pkg_resources.resource_exists("LandSeed", os.path.join(templatesDir, templateName)):
                error("Unknown template name : "+templateName, 3)
        firstLines += 1
    if firstLines >= len(input):
        if templateName == None:
            error("Missing template declaration in input file.", 1)
    print("Template : "+templateName)

    templateDirPath=os.path.join(templatesDir, templateName)

    template = TemplateInfo(templateDirPath)
    # getting template content
    emptyShaderContent = template.getContent()
    shutil.copytree(template.getPath(), outputPath,ignore=shutil.ignore_patterns('template.config'))

    outputFilePath=os.path.join(outputPath, template.getFileTofillName())

    # if output file exists, remove it, then open it
    if os.path.exists(outputFilePath):
        os.remove(outputFilePath)
    global outputFile

    if len(inputFileTemplateLine) < 2 or len(inputFileTemplateLine) > 2 + template.getNbOfParam(): # check if the input file got enough param (this means no param or all params)
        print("Please declare correctly template in input file.\nYou can declare it alone or with some of the parameters.")
        for param in template.getParams():
            template.paramToString(param)
        sys.exit(1)

    # init tag list in order to mark those who are defined by the user then use the non-marked defaults values
    paramUsed = {}
    for p in template.getParams():
        paramUsed[template.getParamTag(p)]= False

    for paramDeclared in range(2,len(inputFileTemplateLine)): # run through each parameters declared by the user in the input file
        if inputFileTemplateLine[paramDeclared]: # if there is a parameter
            try: # try to parse it getting to two parts of the "TAG=VALUE" declaration
                currentParamTagRE = re.compile("(.*)=")
                currentParamTag = currentParamTagRE.search(inputFileTemplateLine[paramDeclared]).group(1)
                currentParamGivenValueRE = re.compile("=(.*)")
                currentParamGivenValue = currentParamGivenValueRE.search(inputFileTemplateLine[paramDeclared]).group(1)
            except Exception as e:
                print("Error while parsing input file.")
                sys.exit(1)
            if currentParamTag == "" or currentParamGivenValue == "":
                print("One of the parameter you entered has no value or no tag")
                sys.exit(1)
            if currentParamTag in paramUsed.keys():
                paramUsed[currentParamTag] = True
            else:
                print("Template param "+currentParamTag+" used in the input is not recognize.\nPlease use the following parameters correctly.")
                for param in template.getParams():
                    template.paramToString(param)
                sys.exit(1)
            for templateParam in template.getParams(): # search for the parameter in all the parameters defined in the template
                if template.getParamTag(templateParam) == currentParamTag :
                    try: # try a convertion to detecte some type error (not efficient for all possibilities : 123 to bool will be convert as True and no error will be raised)
                        locate(template.getParamType(templateParam).lower())(currentParamGivenValue)
                    except Exception as e:
                        print("Wrong type of paramter given for "+currentParamTag+".\nThe type should be "+template.getParamType(templateParam))
                        sys.exit(1)
                    if template.getParamFile(templateParam) == template.getFileTofillName(): # if the param should be put in GEN_FILE
                        for line in range(len(emptyShaderContent)):
                            if "@"+template.getParamTag(templateParam) in emptyShaderContent[line]:
                                emptyShaderContent[line] = emptyShaderContent[line].replace("@"+currentParamTag, currentParamGivenValue)
                    else: # if it's a custom file
                        print("---------------DEBUG-------------")
                        print("outputPath : "+outputPath)
                        print("ParamFile : "+template.getParamFile(p))
                        print(os.path.join(outputPath, template.getParamFile(p)))
                        print("---------------DEBUG-------------")
                        fileToFulfillPath = os.path.join(outputPath, template.getParamFile(p))
                        fin = open(fileToFulfillPath, "rt")
                        data = fin.read()
                        data = data.replace("@"+currentParamTag, currentParamGivenValue)
                        fin.close()
                        fin = open(fileToFulfillPath, "wt")
                        fin.write(data)
                        fin.close()

    # fill missing params with with defaults values
    for templateParam in template.getParams():
        if paramUsed[template.getParamTag(templateParam)] == False:
            print(template.getParamTag(templateParam)+" default value is taken")
            if template.getParamFile(templateParam) == template.getFileTofillName(): # if the param should be put in GEN_FILE
                for line in range(len(emptyShaderContent)):
                    if "@"+template.getParamTag(templateParam) in emptyShaderContent[line]:
                        emptyShaderContent[line] = emptyShaderContent[line].replace("@"+template.getParamTag(templateParam), template.getParamDefaultValue(templateParam))
            else: # if it's a custom file
                fileToFulfillPath = os.path.join(outputPath, template.getParamFile(p))
                fin = open(fileToFulfillPath, "rt")
                data = fin.read()
                data = data.replace("@"+template.getParamTag(templateParam), template.getParamDefaultValue(templateParam))
                fin.close()
                fin = open(fileToFulfillPath, "wt")
                fin.write(data)
                fin.close()

    outputFile = open(outputFilePath, "w+")
    outputFile.write("// @FROM "+inputPath.replace(libRootPath,"")+"\n")
    outputFile.write("// @TO "+os.path.dirname(outputFilePath.replace(libRootPath, ""))+"\n")
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
def generate(inputP=os.path.join(inputDir,"demo.frag"), output=os.path.join(os.getcwd(),outputDir), forceOverwrite=False):

    global outputPath # path to the output dir
    global outputFile # output file (the one where @TERRAIN_MAP is)
    global inputPath # path to the input file
    global includedFeatures
    global includedDependencies

    includedFeatures = [] # to register which feature we already added
    includedDependencies = [] # to register which dependencies we already added

    if len(sys.argv) == 3:
        inputPath, outputPath = os.path.join(sys.argv[1]),os.path.join(sys.argv[2])
    elif len(sys.argv) == 1:
        print("Default parameters are taken.")
        inputPath = inputP
        outputPath = output
    else:
        print("Parameter error.")
        print("Syntax : ")
        print("LandSeed.py [inputPath] [outputPath]")
        print("or")
        print("LandSeed.py")
        sys.exit(4)
    # inputPath = os.path.join(libRootPath,input)
    print("Input file : "+inputPath)
    # outputPath = os.path.join(libRootPath,output)
    print("Output file : "+outputPath)
    # checking that input exist and that it's a file
    if (not os.path.exists(inputPath) or not os.path.isfile(inputPath)) and not pkg_resources.resource_exists("LandSeed", inputPath) :
        print("Please enter a valid or existing input file.")
        sys.exit(4)

    # opening and getting input file content
    if pkg_resources.resource_exists("LandSeed", inputPath):
        inputFile = open(pkg_resources.resource_filename("LandSeed", inputPath), "r")
    else:
        inputFile = open(inputPath, "r")
    inputFileContent = inputFile.readlines()
    inputFile.close()

    outputFile = None

    if os.path.exists(outputPath) and forceOverwrite == False:
        choice = input(outputPath + " already exists, are you sure you want to overwrite it (y/n)? ")
        if choice.upper() == "Y":
            shutil.rmtree(outputPath)
        else:
            print("Aborting..")
            sys.exit(-1)
    elif os.path.exists(outputPath) and forceOverwrite == True:
        shutil.rmtree(outputPath)
    # fulfill template with input file and dependencies
    copyAndComplete(inputFileContent)

    return 0

def newInputFile():
    print("Generating new input file")
    shutil.copyfile(pkg_resources.resource_filename("LandSeed", os.path.join(inputDir,"demo.frag")), "input.frag")
    return 0

# Todo : make this usable
if __name__=="__main__":
        # user can enter a personnal input file or use the default one
        # no parameters -> default input and output
        if len(sys.argv)==1:
            print("Default input file is taken : "+os.path.join(inputDir, "input.frag"))
            print("Default output directory is taken : "+outputDir)
            generate(os.path.join(inputDir,"input.frag"), outputDir)
        # parameters given
        elif len(sys.argv)==3:
            print("Input file : "+sys.argv[1])
            print("Output file : "+sys.argv[2])
            generate(sys.argv[1], sys.argv[2])
        # wrong number of parameters
        else:
            print("Parameter error.")
            print("Syntax : ")
            print("LandSeed.py [inputPath] [outputPath]")
            print("or")
            print("LandSeed.py")
            sys.exit(4)

        # exit
        sys.exit(0)
