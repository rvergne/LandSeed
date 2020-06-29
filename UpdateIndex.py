#!/usr/bin/env python3
import os
import sys
import re
import time
from GeneratorUtils.LibPaths import libRootPath, featuresDir, utilsDir, indexFileLocation, indexName, generatorIndex
from GeneratorUtils.ShaderFragmentInfoClass import ShaderFragmentInfo

# return code
#   0 : Everything's ok
#   1 : keyword missing in a file
#   5 : index file error

# check if files changes, if there is new files, and if some files has been removed
# return true if we should update index
def shouldUpdateIndex():
    print("Checking if index is up to date..")
    if not os.path.exists(generatorIndex):
        return True

    try:
        from GeneratorUtils.shader_index import dictTagToPath
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
    print("Getting "+path.replace(libRootPath, "")+" files informations..")
    cat=""
    if "features" in path:
        cat = "feature"
    else:
        cat = "util"
    availableFiles = os.listdir(path) # Get file name in path dir
    for file in availableFiles:
        currentFilePath = path+file
        lastLine=0
        for nb in range(ShaderFragmentInfo.getFragmentCounter(currentFilePath)):
            currentFragment = ShaderFragmentInfo(cat, currentFilePath, lastLine)
            dictTagToPath[currentFragment.getTag()]=currentFragment.getRelativePath()
            if currentFragment.getCat() == "feature":
                dictFeatureFunctionToTag[currentFragment.getFunctionName()]=currentFragment.getTag()
            lastLine=currentFragment.getLastLine()

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
    global dictTagToPath # dict with TAG for key and relative path for value
    dictTagToPath = {}
    global dictFeatureFunctionToTag # features dict with FUNCTION_NAME for key and tag for value
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
