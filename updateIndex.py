#!/usr/bin/env python3
import os
import sys
import re

# return code
#   0 : Everything's ok
#   1 : Header problem

featuresDir="shaders/features/"
utilsDir="shaders/utils/"
indexFileLocation="generator/"
indexName="shader_index.py"

def fulfill(path):
    availableFiles = os.listdir(libRootPath+path) # Get file name in path dir
    for file in availableFiles:                          # Open each one then for each line, check if there is @TAG (which define a tag for a feature/utils).
        currentFilePath = path+file
        currentFile = open(libRootPath+path+file, "r")
        currentFileContent = currentFile.readlines()
        for line in range(len(currentFileContent)):
            if "@TAG" in currentFileContent[line]:
                p = re.compile("@TAG (.*)")
                resultTag = p.search(currentFileContent[line]).group(1)
                dictTagToPath[resultTag]=currentFilePath
                if not "@FUNCTION_NAME" in currentFileContent[line+1]:
                    print("Header badly written in "+currentFilePath)
                    print("@FUNCTION_NAME should follow @TAG line")
                    sys.exit(1)
                else:
                    if path == featuresDir:
                        p = re.compile("@FUNCTION_NAME (.*)")
                        resultFunctionName = p.search(currentFileContent[line+1]).group(1)
                        dictFeatureFunctionToTag[resultFunctionName]=resultTag
        currentFile.close()

# print dictTagToPath content (in a readable way) to debug
def print_dictTagToPath():
    for i in dictTagToPath:
        print(i+" : "+dictTagToPath[i])

# write the dictTagToPath in a file
def writeIndex():
    indexPath = libRootPath+indexFileLocation+indexName
    if os.path.exists(indexPath):
        os.remove(indexPath)
    indexFile = open(indexPath, "w")
    indexFile.write("#!/usr/bin/env python3\n")
    indexFile.write("dictTagToPath = "+repr(dictTagToPath).replace(", ",",\n"))
    indexFile.write("\n\n")
    indexFile.write("dictFeatureFunctionToTag = "+ repr(dictFeatureFunctionToTag).replace(", ",",\n"))
    indexFile.close()

def main():
    global libRootPath
    libRootPath=os.path.dirname(os.path.realpath(__file__))+"/"
    global dictTagToPath
    dictTagToPath = {}
    global dictFeatureFunctionToTag
    dictFeatureFunctionToTag = {}
    fulfill(featuresDir)
    fulfill(utilsDir)
    #print_dictTagToPath()
    writeIndex()
    sys.exit(0)

main()
