#!/usr/bin/env python3
import sys
import os
import re
import shutil
from GeneratorUtils.LibPaths import libRootPath, featuresDir, utilsDir, docDir
from GeneratorUtils.ShaderFragmentInfoClass import ShaderFragmentInfo

# Return values
#   0 : Everything's ok
#   1 : keyword missing in a file

features = []
utils = []

# exiting properly on error
def abort(returnCode):
    print("Aborting..")
    for i in features:
        del i
    for i in utils:
        del i
    sys.exit(returnCode)

# write every single doc pages except main
def createDocPages():
    print("Writing specific documentations pages..")
    os.makedirs(docDir+"features/") # TODO check python version
    os.makedirs(docDir+"utils/") # TODO check python version
    for feature in features:
        featureFile = open(docDir+"features/"+feature.getFunctionName()+".md","w")
        featureFile.write(feature.toMD())
        featureFile.close()
    for util in utils:
        utilFile = open(docDir+"utils/"+util.getFunctionName()+".md","w")
        utilFile.write(util.toMD())
        utilFile.close()

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
    mainFile.write("| Function Name | Full Name | Tag |\n")
    mainFile.write("|-|-|-|\n")

    for feature in features:
        completeDocPath="(features/"+feature.getFunctionName()+".md)"
        mainFile.write("| ["+feature.getFunctionName()+"]"+completeDocPath+" | "+feature.getName()+" | "+feature.getTag()+" |\n")

    mainFile.write("\n\n")
    mainFile.write("## Utils")
    mainFile.write("\n\n")
    mainFile.write("Utils are the functions used to develop features. Soon utils will be possible to include in input file.")
    mainFile.write("\n\n")
    mainFile.write("| Function Name | Full Name | Tag |\n")
    mainFile.write("|-|-|-|\n")

    for util in utils:
        completeDocPath="(utils/"+util.getFunctionName()+".md)"
        mainFile.write("| ["+util.getFunctionName()+"]"+completeDocPath+" | "+util.getName()+" | "+util.getTag()+" |\n")

    mainFile.close()

# read shaders fragments files to get informations
def getInfo():
    print("Getting features and utils informations..")

    featuresDirContent = os.listdir(featuresDir)
    for feature in featuresDirContent:
        currentFilePath = featuresDir+feature
        lastLine=0
        for nb in range(ShaderFragmentInfo.getFragmentCounter(currentFilePath)):
            currentFragment = ShaderFragmentInfo("feature", currentFilePath, lastLine)
            features.append(currentFragment)
            lastLine=currentFragment.getLastLine()

    utilsDirContent = os.listdir(utilsDir)
    for util in utilsDirContent:
        currentFilePath = utilsDir+util
        lastLine=0
        for nb in range(ShaderFragmentInfo.getFragmentCounter(currentFilePath)):
            currentFragment = ShaderFragmentInfo("util", currentFilePath, lastLine)
            utils.append(currentFragment)
            lastLine=currentFragment.getLastLine()

    features.sort(key=lambda feature: feature.getFunctionName())
    utils.sort(key=lambda util: util.getFunctionName())

# print all fragment info to debug
def displayDebug():
    for i in features:
        i.displayInfo()
    for i in utils:
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
