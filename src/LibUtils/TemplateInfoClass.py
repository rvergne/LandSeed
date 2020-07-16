#!/usr/bin/env python3
import os
import re
import sys
try: # Pas beau mais gère le fait qu'on puisse aussi appeler le script depuis de dossier src/LibUtils/
    from src.LibUtils.LibPaths import libRootPath
except Exception as e:
    from LibPaths import libRootPath

class TemplateInfo:
    # initialize the object by reading the file path, from the line beginLine (for the case where there is more than one fragment in the same file)
    def __init__(self, path):
        if not path[-1:]=="/":
            path += "/"
        self.path = path
        self.lineDirective = None
        self.fileToFill = ""
        self.tag = ""
        self.name = ""
        self.desc = ""
        self.content = []
        if not os.path.isdir(path):
            print("The template path given should be a directory containing all template files.\nWrong file path given : "+path)
            sys.exit(2)
        self.extractInfo()
        # self.displayInfo()
    def findFileToFill(self):
        for fname in os.listdir(self.getPath()):
            if os.path.isfile(self.getPath()+"/"+fname):
                with open(self.getPath()+"/"+fname, "r") as f:
                    for line in f:
                        if '@TAG' in line:
                            self.setFileToFillName(fname)
                            return
    def extractInfo(self):
        self.findFileToFill()
        if self.getFileTofillName() == "":
            print("Template at "+self.getPath().replace(libRootPath, "")+" don't contains any file with correct header.")
            sys.exit(2)
        fileToFillPath=self.getPath()+self.getFileTofillName()
        if os.path.isfile(fileToFillPath):
            templateFile = open(fileToFillPath, "r")
            templateContent = templateFile.readlines()
            templateFile.close()
            line = 0
            while line < len(templateContent) and not "END" in templateContent[line] :
                if "@LINE_DIRECTIVE_ON" in templateContent[line] and templateContent[line][templateContent[line].find("@LINE_DIRECTIVE_ON")+18] != "\n":
                    p = re.compile("@LINE_DIRECTIVE_ON (.*)")
                    line_directive = p.search(templateContent[line]).group(1)
                    if "true" in line_directive.lower():
                        line_directive = True
                    elif "false" in line_directive.lower():
                        line_directive = False
                    else:
                        print("@LINE_DIRECTIVE_ON should be a boolean in "+fileToFillPath.replace(libRootPath, ""))
                        sys.exit(1)
                    self.setLineDirective(line_directive)
                elif "@TAG" in templateContent[line] and templateContent[line][templateContent[line].find("@TAG")+4] != "\n":
                    p = re.compile("@TAG (.*)")
                    res_tag = p.search(templateContent[line]).group(1)
                    self.setTag(res_tag)
                elif "@NAME" in templateContent[line] and templateContent[line][templateContent[line].find("@NAME")+5] != "\n":
                    p = re.compile("@NAME (.*)")
                    res_name = p.search(templateContent[line]).group(1)
                    self.setName(res_name)
                elif "@DESC" in templateContent[line] and templateContent[line][templateContent[line].find("@DESC")+5] != "\n":
                    p = re.compile("@DESC (.*)")
                    res_desc = p.search(templateContent[line]).group(1)
                    if res_desc != "{":
                        print("Template badly written, please check description format")
                        sys.exit(1)
                    line += 1
                    while line < len(templateContent) and not "//}" in templateContent[line].replace(" ", ""):
                        res_desc = templateContent[line].replace("//", "")
                        line += 1
                    if line >= len(templateContent):
                        print("Template badly written, missing description end \"}\"")
                    if res_desc[len(res_desc)-1] == "\n":
                        res_desc = res_desc[:-1]
                    self.setDesc(res_desc)
                line += 1
            if line >= len(templateContent):
                print("Template header badly written, missing END keyword")
                sys.exit(1)
            if not self.isComplete():
                print("Template badly written, header element missing")
            line += 1
            while line < len(templateContent):
                self.content.append(templateContent[line])
                line += 1
        else:
            print("Wrong path to file given : "+fileToFillPath.replace(libRootPath, ""))
            del self
            sys.exit(2)
    def isComplete(self):
        return self.lineDirective != None and self.name != "" and self.desc != "" and self.tag != ""
    # use the display function to debug
    def displayInfo(self):
        print("-------------------------------------------")
        print("Name : "+self.getName())
        print("Tag : "+self.getTag())
        print("Line directive on : "+str(self.getLineDirective()))
        print("Desc : "+self.getDesc())
        print("Path : "+self.getPath()+self.getFileTofillName())
        print("-------------------------------------------")
        print("Content : ")
        print(repr(self.getContent()))
    def toMD(self):
        str = ""
        str += "# "+self.getName()+"\n\n"
        str += "**Description : \n\n"+self.getDesc()
        return str
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
