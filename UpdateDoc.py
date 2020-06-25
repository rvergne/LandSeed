#!/usr/bin/env python3
import sys
import os
import re
import shutil

# Return values
#   0 : Everything's ok
#   1 : file badly formated

libRootPath = os.path.dirname(os.path.realpath(__file__))+"/"
featuresDir = libRootPath + "shaders/features/"
utilsDir = libRootPath + "shaders/utils/"
docDir = libRootPath + "Doc/"

features = []
utils = []

class ShaderFragment:
    def __init__(self, featOrUtil):
        self.cat = featOrUtil # 2 values : "feature" or "util"
        self.tag = ""
        self.funcName = ""
        self.signature = ""
        self.name = ""
        self.spec = ""
    def setTag(self, str):
        self.tag = str
    def setFunctionName(self, str):
        self.funcName = str
    def setSignature(self, str):
        self.signature = str
    def setName(self, str):
        self.name = str
    def setSpec(self, str):
        self.spec = str
    def getTag(self):
        return self.tag
    def getFunctionName(self):
        return self.funcName
    def getSignature(self):
        return self.signature
    def getName(self):
        return self.name
    def getSpec(self):
        return self.spec
    def isComplete(self):
        if not (self.tag == "" or self.funcName == "" or self.signature == "" or self.name == "" or self.spec == ""):
            return True
        return False
    def displayInfo(self):
        print("-----------------------------------------")
        print("Category: "+self.cat)
        print("Tag: "+self.tag)
        print("Function Name: "+self.funcName)
        print("Signature: "+self.signature)
        print("Name: "+self.name)
        print("Spec: "+self.spec)
        print("-----------------------------------------")
    def toMD(self):
        str = ""
        str += "# "+self.name+"\n\n"
        str += "**Category**: "+self.cat+"\n\n"
        str += "**Tag**: "+self.tag+"\n\n"
        str += "**Function Name**: "+self.funcName+"\n\n"
        str += "**Signature**: "+self.signature+"\n\n"
        str += "**Name**: "+self.name+"\n\n"
        str += "**Spec**: "+self.spec+"\n\n"
        return str

def abort(returnCode):
    print("Aborting..")
    for i in features:
        del i
    for i in utils:
        del i
    sys.exit(returnCode)

def createDocPages():
    print("Writing specific documentations pages..")
    os.makedirs(docDir+"features/")
    os.makedirs(docDir+"utils/")
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
    # mainFile.write("<style>\n    table{\n        border-collapse: collapse;\n        border-spacing: 0;\n        border:2px solid black;\n    }\n\n    th{\n        border:2px solid #000000;\n        padding: 10px;\n    }\n\n    td{\n        border:1px solid #000000;\n        padding: 5px;\n    }\n    </style>\n    \n\n")
    mainFile.write("# Procedural Terrain Lib - Documentation")
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

def getInfo():
    print("Getting features and utils informations..")
    featuresDirContent = os.listdir(featuresDir)
    currentFragment = ShaderFragment("feature")
    for feature in featuresDirContent:
        featureFile = open(featuresDir+feature, "r")
        featureContent = featureFile.readlines()
        featureFile.close()
        for line in range(len(featureContent)):
            if "@TAG" in featureContent[line]:
                p = re.compile("@TAG (.*)")
                tag = p.search(featureContent[line]).group(1)
                currentFragment.setTag(tag)
            elif "@FUNCTION_NAME" in featureContent[line]:
                p = re.compile("@FUNCTION_NAME (.*)")
                functionName = p.search(featureContent[line]).group(1)
                currentFragment.setFunctionName(functionName)
            elif "@SIGNATURE" in featureContent[line]:
                p = re.compile("@SIGNATURE (.*)")
                signature = p.search(featureContent[line]).group(1)
                currentFragment.setSignature(signature)
            elif "@NAME" in featureContent[line]:
                p = re.compile("@NAME (.*)")
                fullName = p.search(featureContent[line]).group(1)
                currentFragment.setName(fullName)
            elif "@SPEC" in featureContent[line]:
                line += 1
                spec = featureContent[line].replace("// ", "")+"\n"
                line += 1
                while not "//}" in featureContent[line].replace(" ", ""):
                    spec += "- "+featureContent[line].replace("// ", "")+"\n"
                    line += 1
                currentFragment.setSpec(spec)
            if "//END" in featureContent[line].replace(" ","").replace("-", ""):
                if currentFragment.isComplete():
                    features.append(currentFragment)
                    currentFragment = ShaderFragment("feature")
                else:
                    print("File badly formated : "+featuresDir+feature)
                    abort(1)
    utilsDirContent = os.listdir(utilsDir)
    currentFragment = ShaderFragment("util")
    for util in utilsDirContent:
        utilFile = open(utilsDir+util, "r")
        utilContent = utilFile.readlines()
        utilFile.close()
        for line in range(len(utilContent)):
            if "@TAG" in utilContent[line]:
                p = re.compile("@TAG (.*)")
                tag = p.search(utilContent[line]).group(1)
                currentFragment.setTag(tag)
            elif "@FUNCTION_NAME" in utilContent[line]:
                p = re.compile("@FUNCTION_NAME (.*)")
                functionName = p.search(utilContent[line]).group(1)
                currentFragment.setFunctionName(functionName)
            elif "@SIGNATURE" in utilContent[line]:
                p = re.compile("@SIGNATURE (.*)")
                signature = p.search(utilContent[line]).group(1)
                currentFragment.setSignature(signature)
            elif "@NAME" in utilContent[line]:
                p = re.compile("@NAME (.*)")
                fullName = p.search(utilContent[line]).group(1)
                currentFragment.setName(fullName)
            elif "@SPEC" in utilContent[line]:
                line += 1
                spec = utilContent[line].replace("// ", "")+"\n"
                line += 1
                while not "//}" in utilContent[line].replace(" ", ""):
                    spec += "- "+utilContent[line].replace("// ", "")+"\n"
                    line += 1
                currentFragment.setSpec(spec)
            if "//END" in utilContent[line].replace(" ","").replace("-", ""):
                if currentFragment.isComplete():
                    utils.append(currentFragment)
                    currentFragment = ShaderFragment("util")
                else:
                    print("File badly formated : "+utilsDir+util)
                    abort(1)
    features.sort(key=lambda feature: feature.getFunctionName())
    utils.sort(key=lambda util: util.getFunctionName())

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
