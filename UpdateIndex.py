#!/usr/bin/env python3
import os
import sys
import re
import time

# return code
#   0 : Everything's ok
#   1 : Header problem
#   5 : index file error

libRootPath=os.path.dirname(os.path.realpath(__file__))+"/"
featuresDir=libRootPath+"shaders/features/"
utilsDir=libRootPath+"shaders/utils/"
indexFileLocation=libRootPath+"generatorUtils/"
indexName="shader_index.py"
generatorIndex=libRootPath + "generatorUtils/shader_index.py"

# check if files changes, if there is new files, and if some files has been removed
# return true if we should update index
def shouldUpdateIndex():
    print("Checking if index is up to date..")
    if not os.path.exists(generatorIndex):
        return True

    try:
        from generatorUtils.shader_index import dictTagToPath
    except:
        print("Error importing index. Please remove it and try again.(generatorUtils/shader_index.py)")
        sys.exit(5)

    for line in dictTagToPath:
        if not os.path.exists(libRootPath+dictTagToPath[line]):
            return True

    updateDate = os.path.getmtime(generatorIndex)   # Creation time of index
    mostRecentFeature=max([f for f in os.scandir(featuresDir)], key=lambda x: x.stat().st_mtime) # last modified feature
    mostRecentUtils=max([f for f in os.scandir(utilsDir)], key=lambda x: x.stat().st_mtime) # last modified util
    mostRecentlyChangedFile=max([mostRecentFeature,mostRecentUtils], key=lambda x: x.stat().st_mtime).path # last overall modification
    if os.path.getmtime(mostRecentlyChangedFile) > updateDate:
        return True

    return False

def fulfill(path):
    print("Getting "+path+" files informations..")
    availableFiles = os.listdir(path) # Get file name in path dir
    for file in availableFiles:                          # Open each one then for each line, check if there is @TAG (which define a tag for a feature/utils).
        currentFilePath = path+file
        currentFile = open(currentFilePath, "r")
        currentFileContent = currentFile.readlines()
        currentFile.close()
        for line in range(len(currentFileContent)):
            if "@TAG" in currentFileContent[line]:
                p = re.compile("@TAG (.*)")
                resultTag = p.search(currentFileContent[line]).group(1)
                dictTagToPath[resultTag]=currentFilePath.replace(libRootPath,"")
                if not "@FUNCTION_NAME" in currentFileContent[line+1]:    # get the associated function name
                    print("Header badly written in "+currentFilePath)
                    print("@FUNCTION_NAME should follow @TAG line")
                    sys.exit(1)
                else:
                    if path == featuresDir:
                        p = re.compile("@FUNCTION_NAME (.*)")
                        resultFunctionName = p.search(currentFileContent[line+1]).group(1)
                        dictFeatureFunctionToTag[resultFunctionName]=resultTag

# print dictTagToPath content (in a readable way) to debug
def print_dictTagToPath():
    for i in dictTagToPath:
        print(i+" : "+dictTagToPath[i])

# write the dictTagToPath in a file
def writeIndex():
    print("writting the index..",end="")
    indexPath = indexFileLocation+indexName
    if os.path.exists(indexPath):
        os.remove(indexPath)
    indexFile = open(indexPath, "w")
    indexFile.write("#!/usr/bin/env python3\n")
    indexFile.write("dictTagToPath = "+repr(dictTagToPath).replace(", ",",\n"))
    indexFile.write("\n\n")
    indexFile.write("dictFeatureFunctionToTag = "+ repr(dictFeatureFunctionToTag).replace(", ",",\n"))
    indexFile.close()

def createIndex():
    global dictTagToPath
    dictTagToPath = {}
    global dictFeatureFunctionToTag
    dictFeatureFunctionToTag = {}
    fulfill(featuresDir)
    fulfill(utilsDir)
    #print_dictTagToPath()
    writeIndex()
    print("Complete")

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   createIndex()
   sys.exit(0)
