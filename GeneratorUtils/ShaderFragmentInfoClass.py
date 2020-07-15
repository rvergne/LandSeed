#!/usr/bin/env python3
import os
import re
import sys
from GeneratorUtils.LibPaths import libRootPath

# class used to get all inforamtions about a feaeture or a util
class ShaderFragmentInfo:
    # initialize the object by reading the file path, from the line beginLine (for the case where there is more than one fragment in the same file)
    def __init__(self, featOrUtil, path, beginLine):
        self.cat = featOrUtil # 2 values : "feature" or "util"
        self.path = path
        self.tag = ""
        self.funcName = ""
        self.signature = ""
        self.name = ""
        self.spec = ""
        self.tagPresence = False
        self.beginLine = beginLine
        self.lastLine = 0
        self.extractInfo(path)
    # extract all info from the file define by path
    def extractInfo(self, path):
        if os.path.isfile(path):
            fragmentFile = open(path, "r")
            fragmentContent = fragmentFile.readlines()
            fragmentFile.close()
            for line in range(self.beginLine, len(fragmentContent)):
                if "@TAG" in fragmentContent[line] and fragmentContent[line][fragmentContent[line].find("@TAG")+4] != "\n":
                    p = re.compile("@TAG (.*)")
                    tag = p.search(fragmentContent[line]).group(1)
                    if " " in tag:
                        print("File badly formated : tag should be in one single word in "+path.replace(libRootPath, ""))
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
                if "//END" in fragmentContent[line].replace(" ","").replace("-", ""):
                    if self.isHeaderComplete():
                        break
                    else:
                        print("Header badly formated in "+path.replace(libRootPath, ""))
                        del self
                        sys.exit(1)
            while (line < len(fragmentContent)) and (not "@END" in fragmentContent[line]) and not "@TAG" in fragmentContent[line]: # TODO add check next feature
                if "@"+self.getTag() in fragmentContent[line]:
                    self.tagPresence = True
                line += 1
            if line >= len(fragmentContent) or "@TAG" in fragmentContent[line]:
                print("Missing @END tag in "+path.replace(libRootPath, ""))
                del self
                sys.exit(1)
            if not self.tagPresence:
                print("Missing starting tag : @"+self.tag+" before function implementation start in "+path.replace(libRootPath, ""))
                del self
                sys.exit(1)
            line +=1
            self.lastLine = line
        else:
            print("Wrong path to file given : "+path.replace(libRootPath, ""))
            del self
            sys.exit(2)
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
    def getLastLine(self):
        return self.lastLine
    # check if the object contains all the informations it should
    def isHeaderComplete(self):
        if not (self.tag == "" or self.funcName == "" or self.signature == "" or self.name == "" or self.spec == ""):
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
    # convert the object to markdown format for the documentation
    def toMD(self):
        str = ""
        str += "# "+self.name+"\n\n"
        str += "**Tag**: "+self.tag+"\n\n"
        str += "**Category**: "+self.cat+"\n\n"
        str += "**Function Name**: "+self.funcName+"\n\n"
        str += "**Signature**: "+self.signature+"\n\n"
        str += "**Spec**: "+self.spec+"\n\n"
        return str
    # return how much feature or utils there is in the file by counting the number of "@TAG" in the file
    @staticmethod
    def getFragmentCounter(path):
        c=0
        file = open(path, "r")
        content = file.readlines()
        file.close()
        for line in content:
            if "@TAG" in line:
                c += 1
        return c
