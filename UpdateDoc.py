#!/usr/bin/env python3
import sys
if sys.version_info.major < 3: # python version should be 3+
    print("Python version to old, please upgrade your python to 3 or more.")
    sys.exit(6)
import os
import re
import shutil
from src.LibUtils.LibPaths import libRootPath, featuresDir, utilsDir, docDir, templatesDir
from src.LibUtils.ShaderFragmentInfoClass import ShaderFragmentInfo
from src.LibUtils.TemplateInfoClass import TemplateInfo

# Return values
#   0 : Everything's ok
#   1 : keyword missing in a file

features = []
utils = []
templates = []

# exiting properly on error
def abort(returnCode):
    print("Aborting..")
    for i in features:
        del i
    for i in utils:
        del i
    for i in templates:
        del i
    sys.exit(returnCode)

# write every single doc pages except main
def createDocPages():
    print("Writing specific documentations pages..")
    os.makedirs(docDir+"features/") # TODO check python version
    os.makedirs(docDir+"utils/") # TODO check python version
    os.makedirs(docDir+"templates/") # TODO check python version
    for feature in features:
        featureFile = open(docDir+"features/"+feature.getFunctionName()+".md","w")
        featureFile.write(feature.toMD())
        featureFile.close()
    for util in utils:
        utilFile = open(docDir+"utils/"+util.getFunctionName()+".md","w")
        utilFile.write(util.toMD())
        utilFile.close()
    for template in templates:
        templateFile = open(os.path.join(os.path.join(docDir,"templates"), template.getTag().lower()+".md"), "w")
        templateFile.write(template.toMD())
        templateFile.close()

# Create a page that list features and utils linking them to their own page
def createMainDocPage():
    print("Writing main doc page..")
    mainFile = open(docDir+"main.md","w")
    mainFile.write("# LandSeed - Documentation")
    mainFile.write("\n\n")
    mainFile.write("## Features")
    mainFile.write("\n\n")
    mainFile.write("Features are the main functions you can use in your terrainMap fonction (inside your input file) without any import.")
    mainFile.write("\n\n")
    mainFile.write("| Function Name | Full Name | Short description |\n")
    mainFile.write("|-|-|-|\n")

    for feature in features:
        completeDocPath="(features/"+feature.getFunctionName()+".md)"
        mainFile.write("| ["+feature.getFunctionName()+"]"+completeDocPath+" | "+feature.getName()+" | "+feature.getShortDesc()+" |\n")

    mainFile.write("\n\n")
    mainFile.write("## Utils")
    mainFile.write("\n\n")
    mainFile.write("Utils are the functions used to develop features.")
    mainFile.write("\n\n")
    mainFile.write("| Function Name | Full Name | Short description |\n")
    mainFile.write("|-|-|-|\n")

    for util in utils:
        completeDocPath="(utils/"+util.getFunctionName()+".md)"
        mainFile.write("| ["+util.getFunctionName()+"]"+completeDocPath+" | "+util.getName()+" | "+util.getShortDesc()+" |\n")

    mainFile.write("\n\n")
    mainFile.write("## Templates")
    mainFile.write("\n\n")
    mainFile.write("Templates are a way to get different kind of output.  \n")
    mainFile.write("The name is what you have to write in the input to choose which template to use for the output")
    mainFile.write("\n\n")
    mainFile.write("| Name | Tag | Description |\n")
    mainFile.write("|-|-|-|\n")

    for template in templates:
        completeDocPath="(templates/"+template.getTag().lower()+".md)"
        mainFile.write("| ["+template.getName()+"]"+completeDocPath+" | "+template.getTag()+" | "+template.getDesc()+" |\n")

    mainFile.close()

# read shaders fragments files to get informations
def getInfo():
    print("Getting features and utils informations..")

    featuresDirContent = os.listdir(featuresDir)
    for feature in featuresDirContent:
        currentFilePath = os.path.join(featuresDir,feature)
        currentFragment = ShaderFragmentInfo("feature", currentFilePath)
        features.append(currentFragment)

    utilsDirContent = os.listdir(utilsDir)
    for util in utilsDirContent:
        currentFilePath = os.path.join(utilsDir,util)
        currentFragment = ShaderFragmentInfo("util", currentFilePath)
        utils.append(currentFragment)

    templatesDirContent = os.listdir(templatesDir)
    templatesDirContent.remove("shared")
    for template in templatesDirContent:
        currentFilePath = os.path.join(templatesDir,template)
        currentTemplate = TemplateInfo(currentFilePath)
        templates.append(currentTemplate)

    features.sort(key=lambda feature: feature.getFunctionName())
    utils.sort(key=lambda util: util.getFunctionName())
    templates.sort(key=lambda template: template.getName())

# print all fragment info to debug
def displayDebug():
    for i in features:
        i.displayInfo()
    for i in utils:
        i.displayInfo()
    for i in templates:
        i.displayInfo()

def main():
    if os.path.isdir(docDir):
        shutil.rmtree(docDir)
    getInfo()
    # displayDebug()
    os.makedirs(docDir)
    createMainDocPage()
    createDocPages()
    sys.exit(0)

main()
