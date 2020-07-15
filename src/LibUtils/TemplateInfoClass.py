#!/usr/bin/env python3
import os
import re
import sys
try: # Pas beau mais gère le fait qu'on puisse aussi appelé le script depuis de dossier src/LibUtils/
    from src.LibUtils.LibPaths import libRootPath
except Exception as e:
    from LibPaths import libRootPath

class TemplateInfo:
    # initialize the object by reading the file path, from the line beginLine (for the case where there is more than one fragment in the same file)
    def __init__(self, path):
        self.lineDirective = None
        self.name = ""
        self.desc = ""
        self.content = []
        self.extractInfo(path)
    def extractInfo(self, path):
        if os.path.isfile(path):
            templateFile = open(path, "r")
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
                        print("@LINE_DIRECTIVE_ON should be a boolean in "+path.replace(libRootPath, ""))
                        sys.exit(1)
                    self.setLineDirective(line_directive)
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
            print("Wrong path to file given : "+path.replace(libRootPath, ""))
            del self
            sys.exit(2)
    def isComplete(self):
        return self.lineDirective != None and self.name != "" and self.desc != ""
    # use the display function to debug
    def displayInfo(self):
        print("-------------------------------------------")
        print("Name : "+self.getName())
        print("Line direction on : "+str(self.getLineDirective()))
        print("Desc : "+self.getDesc())
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
    def setDesc(self, d):
        self.desc = d
    def getDesc(self):
        return self.desc
    def getContent(self):
        return self.content
