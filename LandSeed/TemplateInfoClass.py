#!/usr/bin/env python3
import os
import re
import pkg_resources
from pydoc import locate
import sys
# try: # Pas beau mais gère le fait qu'on puisse aussi appeler le script depuis de dossier src/LibUtils/
#     from src.LibUtils.LibPaths import libRootPath
# except Exception as e:
#     from LibPaths import libRootPath
from LandSeed.LibPaths import libRootPath
# param spec in the params array for each indices:
# 0 : TAG
# 1 : type
# 2 : file where it needs to be replaced
# 3 : Default value
# 4 : Description for the documentation

class TemplateInfo:
    # initialize the object by reading the file path, from the line beginLine (for the case where there is more than one fragment in the same file)
    def __init__(self, path):
        if not path[-1:]=="/":
            path += "/"
        self.name = ""
        self.tag = ""
        self.fileToFill = ""
        self.pathToFileToFill = ""
        self.lineDirective = None
        self.desc = ""
        self.params = []
        if pkg_resources.resource_exists("LandSeed", path):
            self.path = pkg_resources.resource_filename("LandSeed",path)
        else:
            self.path = path
        self.content = []
        if not os.path.isdir(self.getPath()): # Check if the template dir exist
            print("The template path given should be a directory containing all template files.\nWrong file path given : "+path)
            sys.exit(2)
        self.extractInfo()
        self.extractContent()
        if not self.isComplete():
            print("Please, fulfill the template.config file following the template described in README")
            sys.exit(1)
        self.checkParamType()

    def extractContent(self):
        if not os.path.exists(self.getPathToFileToFill()):
            print("Wrong path given to the file to fulfill in the template.\nTemplate : "+self.path)
            sys.exit(2)
        shaderFile = open(self.getPathToFileToFill(), "r")
        self.content = shaderFile.readlines()
        shaderFile.close()

    def extractInfo(self):
        if not os.path.exists(os.path.join(self.path,"template.config")):
            print("template.config missing in the template at : "+self.path)
            sys.exit(2)
        configFile = open(os.path.join(self.path,"template.config"), "r")
        configFileContent = configFile.readlines()
        configFile.close()
        for line in configFileContent:
            if "@NAME" in line and len(line.split(" ")) > 1:
                p = re.compile("@NAME (.*)")
                res = p.search(line).group(1)
                self.setName(res)
            elif "@TAG" in line and len(line.split(" ")) == 2:
                self.setTag((line.replace("\n", "")).split(" ")[1])
            elif "@GEN_FILE" in line and len(line.split(" ")) == 2:
                self.setFileToFillName((line.replace("\n","")).split(" ")[1])
                self.setPathToFileToFill(os.path.join(self.path, self.getFileTofillName()))
            elif "@LINE_DIRECTIVE_ON" in line and len(line.split(" ")) == 2:
                res = line.split(" ")[1]
                if "true" in res.lower():
                    self.setLineDirective(True)
                elif "false" in res.lower():
                    self.setLineDirective(False)
                else:
                    print("@LINE_DIRECTIVE_ON should be a boolean in config file at "+ self.path)
                    sys.exit(1)
            elif "@DESC" in line and len(line.split(" ")) > 2:
                p = re.compile("@DESC { (.*) }")
                if p.search(line) != None:
                    res = p.search(line).group(1)
                    self.setDesc(res)
                else:
                    print("@DESC tag badly formatted : Description should be between brackets like that { ... }\nIn template : "+self.path)
                    sys.exit(1)
            elif "@PARAM" in line and not "@PARAM_DESC" in line:
                if not len((line.replace("\n", "")).split(" ")) == 5:
                    print("Param line in template.config file badly written.\nPlease follow the way to write it in the README.\nIn template : "+self.path)
                    sys.exit(2)
                line_split = (line.replace("\n", "")).split(" ")
                del line_split[0]
                if line_split[0] == "" or line_split[1] == "" or line_split[2] == "" or line_split[3] == "":
                    print("Param line in template.config file badly written.\nPlease follow the way to write it in the README.\nIn template : "+self.path)
                    sys.exit(2)
                line_split[1] = line_split[1].lower()
                if line_split[2] == "GEN_FILE":
                    line_split[2] = self.getPathToFileToFill()
                else:
                    line_split[2] = os.path.join(self.getPath(), line_split[2])
                p = re.compile("DEFAULT=(.*)")
                line_split[3] = p.search(line_split[3]).group(1)
                self.params.append(line_split)
            elif "@PARAM_DESC" in line:
                try:
                    p = re.compile("@PARAM_DESC (.*) {")
                    param_name = p.search(line).group(1)
                    p = re.compile("@PARAM_DESC "+param_name+" { (.*) }")
                    param_desc = p.search(line).group(1)
                except Exception as e:
                    print("PARAM_DESC badly written in template.config in "+self.path)
                    sys.exit(1)
                for param in self.params:
                    if param[0] == param_name:
                        param.append(param_desc)

    def checkParamType(self):
        for p in self.getParams():
            try: # try a convertion to detecte some type error (not efficient for all possibilities : 123 to bool will be convert as True and no error will be raised)
                locate(self.getParamType(p).lower())(self.getParamDefaultValue(p))
            except Exception as e:
                print("Wrong type of paramter given in template.config for "+self.getParamTag(p)+".\nThe type should be "+self.getParamType(p))
                sys.exit(1)

    def isComplete(self): # TODO fulfill
        return self.lineDirective != None and self.name != "" and self.desc != "" and self.tag != "" and self.fileToFill != ""

    # use the display function to debug
    def displayInfo(self):
        print("-------------------------------------------")
        print("Name : "+self.getName())
        print("Tag : "+self.getTag())
        print("Line directive on : "+str(self.getLineDirective()))
        print("Desc : "+self.getDesc())
        print("FileToFill : "+self.getFileTofillName())
        print("Path : "+self.getPath())
        print("pathToFileToFill : "+self.getPathToFileToFill())
        print("PARAMS")
        for p in self.params:
            print(repr(p))
        print("-------------------------------------------")
        print("Content : ")
        print(repr(self.getContent()))

    def toMD(self):
        res = ""
        res += "# "+self.getName()+"\n\n"
        res += "**Tag**: "+self.getTag()+"\n\n"
        res += "**Description**: "+self.getDesc()+"\n\n"
        res += "**Path**: "+self.getPath().replace(libRootPath, "")+"\n\n"
        res += "**Parameters**:\n\n"
        res += "| Tag | Type | Default Value | File | Description |\n"
        res += "|-|-|-|-|-|\n"
        for p in self.getParams():
            res += "| "+self.getParamTag(p)+" | "+self.getParamType(p)+" | "+str(self.getParamDefaultValue(p))+" | "+self.getParamFile(p)+" | "+self.getParamDescription(p)+" |\n"
        return res

    def getParams(self):
        return self.params
    def getNbOfParam(self):
        return len(self.params)
    def paramToString(self, param):
        print(param[0]+" : "+param[1]+", default value : "+str(param[3])+"; "+param[4])
    def getParamTag(self, param):
        return param[0]
    def getParamType(self, param):
        return param[1]
    def getParamFileFullPath(self, param):
        return param[2]
    def getParamFile(self, param):
        return param[2].replace(self.path, "")
    def getParamDefaultValue(self, param):
        return param[3]
    def getParamDescription(self, param):
        return param[4]

    def setLineDirective(self, on):
        self.lineDirective = on
    def getLineDirective(self):
        return self.lineDirective
    def setName(self, n):
        self.name = n
    def getName(self):
        return self.name
    def setTag(self, n):
        self.tag = n
    def getTag(self):
        return self.tag
    def setDesc(self, d):
        self.desc = d
    def getDesc(self):
        return self.desc
    def getContent(self):
        return self.content
    def setFileToFillName(self, str):
        self.fileToFill = str
    def getFileTofillName(self):
        return self.fileToFill
    def setPath(self, str):
        self.path = str
    def getPath(self):
        return self.path
    def setPathToFileToFill(self, str):
        self.pathToFileToFill = str
    def getPathToFileToFill(self):
        return self.pathToFileToFill
