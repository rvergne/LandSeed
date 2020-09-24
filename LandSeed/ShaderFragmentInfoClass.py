#!/usr/bin/env python3
import os
import re
import sys
import pkg_resources
from LandSeed.LibPaths import libRootPath

# class used to get all inforamtions about a feaeture or a util
class ShaderFragmentInfo:
    # initialize the object by reading the file path
    def __init__(self, featOrUtil, path):
        self.cat = featOrUtil # 2 values : "feature" or "util"
        if pkg_resources.resource_exists("LandSeed", path):
            self.path = pkg_resources.resource_filename("LandSeed",path)
        else:
            self.path = path
        self.tag = ""
        self.funcName = ""
        self.signature = ""
        self.name = ""
        self.short = ""
        self.spec = ""
        self.tagPresence = False
        self.dependencies = []
        self.functionCode = ""
        self.beginLine = 0
        self.extractInfo()
    # extract all info from the file define by path
    def extractInfo(self):
        if os.path.isfile(self.getPath()):
            fragmentFile = open(self.getPath(), "r")
            fragmentContent = fragmentFile.readlines()
            fragmentFile.close()
            for line in range(len(fragmentContent)):
                if "@TAG" in fragmentContent[line] and fragmentContent[line][fragmentContent[line].find("@TAG")+4] != "\n":
                    p = re.compile("@TAG (.*)")
                    tag = p.search(fragmentContent[line]).group(1)
                    if " " in tag:
                        print("File badly formated : tag should be in one single word in "+self.getPath().replace(libRootPath, ""))
                        sys.exit(1)
                    self.setTag(tag)
                elif "@FUNCTION_NAME" in fragmentContent[line] and fragmentContent[line][fragmentContent[line].find("@FUNCTION_NAME")+14] != "\n":
                    p = re.compile("@FUNCTION_NAME (.*)")
                    functionName = p.search(fragmentContent[line]).group(1)
                    self.setFunctionName(functionName)
                elif "@SIGNATURE" in fragmentContent[line] and fragmentContent[line][fragmentContent[line].find("@SIGNATURE")+10] != "\n":
                    p = re.compile("@SIGNATURE (.*)")
                    signature = p.search(fragmentContent[line]).group(1)
                    self.setSignature(signature)
                elif "@NAME" in fragmentContent[line] and fragmentContent[line][fragmentContent[line].find("@NAME")+5] != "\n":
                    p = re.compile("@NAME (.*)")
                    fullName = p.search(fragmentContent[line]).group(1)
                    self.setName(fullName)
                elif "@SPEC" in fragmentContent[line]:
                    line += 1
                    spec = fragmentContent[line].replace("// ", "")+"\n"
                    line += 1
                    while not "//}" in fragmentContent[line].replace(" ", ""):
                        spec += "- "+fragmentContent[line].replace("// ", "")+"\n"
                        line += 1
                    self.setSpec(spec)
                elif "@SHORT" in fragmentContent[line] and fragmentContent[line][fragmentContent[line].find("@SHORT")+6] != "\n":
                    p = re.compile("@SHORT (.*)")
                    self.setShortDesc(p.search(fragmentContent[line]).group(1))
                if "//END" in fragmentContent[line].replace(" ","").replace("-", ""):
                    if self.isHeaderComplete():
                        break
                    else:
                        print("Header badly formated in "+self.getPath().replace(libRootPath, ""))
                        del self
                        sys.exit(1)
            while (line < len(fragmentContent)) and (not self.tagPresence):
                if "@"+self.getTag() in fragmentContent[line]:
                    self.tagPresence = True
                line += 1
            if not self.tagPresence:
                print("Missing starting tag : @"+self.tag+" before function implementation start in "+self.getPath().replace(libRootPath, ""))
                del self
                sys.exit(1)

            while "@INCLUDE" in fragmentContent[line]:
                p = re.compile("@INCLUDE (.*)") # TODO check case where #INCLUDE
                result = p.search(fragmentContent[line]).group(1)
                self.dependencies.append(result)
                line += 1
            self.beginLine = line
            while line < len(fragmentContent) and not "@END" in fragmentContent[line]:
                self.functionCode += fragmentContent[line]
                line += 1

            if line >= len(fragmentContent):
                print("Missing @END tag in "+self.getPath().replace(libRootPath, ""))
                del self
                sys.exit(1)
            line +=1
        else:
            print("Wrong path to file given : "+self.getPath().replace(libRootPath, ""))
            del self
            sys.exit(2)
    def getPath(self):
        return self.path
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
    def getCat(self):
        return self.cat
    def getRelativePath(self):
        return self.path.replace(libRootPath, "")
    def getAbsolutePath(self):
        return self.path
    def getDependencies(self):
        return self.dependencies
    def getBeginLine(self):
        return self.beginLine
    def getFunctionCode(self):
        return self.functionCode
    def getShortDesc(self):
        return self.short
    def setShortDesc(self, str):
        self.short = str
    # check if the object contains all the informations it should
    def isHeaderComplete(self):
        if not (self.tag == "" or self.funcName == "" or self.signature == "" or self.name == "" or self.spec == "" or self.short == ""):
            return True
        return False
    # display informations about the fragment. Used to debug
    def displayInfo(self):
        print("-----------------------------------------")
        print("Category: "+self.cat)
        print("Tag: "+self.tag)
        print("Function Name: "+self.funcName)
        print("Signature: "+self.signature)
        print("Name: "+self.name)
        print("Spec: "+self.spec)
        print("Tag presence: "+str(self.tagPresence))
        print("-----------------------------------------")

    # convert the object to markdown format for the documentation page
    def toMD(self):
        str = ""
        str += "# "+self.name+"\n\n"
        str += "**Tag**: "+self.tag+"\n\n"
        str += "**Category**: "+self.cat+"\n\n"
        str += "**Function Name**: "+self.funcName+"\n\n"
        str += "**Signature**: "+self.signature+"\n\n"
        str += "**Spec**: "+self.spec+"\n\n"
        str += "**Path**: "+self.path.replace(libRootPath, "")+"\n\n"
        return str
