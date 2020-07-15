#!/usr/bin/env python3
import sys
if sys.version_info.major < 3: # python version should be 3+
    print("Python version to old, please upgrade your python to 3 or more.")
    sys.exit(6)
import os
import re
import time
try:# Pas beau mais gère le fait qu'on puisse aussi appelé le script depuis de dossier src/LibUtils/
    from src.LibUtils.LibPaths import libRootPath, featuresDir, utilsDir, indexFileLocation, indexName, generatorIndex
except Exception as e:
    from LibPaths import libRootPath, featuresDir, utilsDir, indexFileLocation, indexName, generatorIndex
try:# Pas beau mais gère le fait qu'on puisse aussi appelé le script depuis de dossier src/LibUtils/
    from src.LibUtils.ShaderFragmentInfoClass import ShaderFragmentInfo
except Exception as e:
    from ShaderFragmentInfoClass import ShaderFragmentInfo

# return code
#   0 : Everything's ok
#   1 : keyword missing in a file
#   5 : index file error

# check if files changed, if there is new files, and if some files has been removed
# return true if we should update index
# (can be changed to handle better the case where we have to reload the module)
def shouldUpdateIndex():
    print("Checking if index is up to date..")

    # checking if there is an index
    if not os.path.exists(generatorIndex):
        return True

    # import index to check if a feature or util has been removed
    try:
        try:
            from src.LibUtils.shader_index import dictTagToPath
        except Exception as e:
            from shader_index import dictTagToPath
    except:
        print("Error importing index. Please remove it and try again.("+indexFileLocation.replace(libRootPath, "")+")")
        sys.exit(5)

    for line in dictTagToPath:
        if not os.path.exists(libRootPath+dictTagToPath[line]):
            return True

    # check if a file has a modification dans more recent than the index
    updateDate = os.path.getmtime(generatorIndex)   # Creation time of index
    mostRecentFeature=max([f for f in os.scandir(featuresDir)], key=lambda x: x.stat().st_mtime) # last modified feature
    mostRecentUtils=max([f for f in os.scandir(utilsDir)], key=lambda x: x.stat().st_mtime) # last modified util
    mostRecentlyChangedFile=max([mostRecentFeature,mostRecentUtils], key=lambda x: x.stat().st_mtime).path # last overall modification
    if os.path.getmtime(mostRecentlyChangedFile) > updateDate:
        return True
    return False

# fulfill dictionnaries with file informations
def fulfill(path):
    print("Getting "+path.replace(libRootPath, "")+" files informations..")
    # get category
    cat=""
    if "features" in path:
        cat = "feature"
    else:
        cat = "util"
    availableFiles = os.listdir(path) # Get file name in path dir
    # for every files, get fragments info and add needed informations in dictionnaries
    for file in availableFiles:
        currentFilePath = path+file
        lastLine=0
        # to handle the case where we have multiple fragment in a single file
        for nb in range(ShaderFragmentInfo.getFragmentCounter(currentFilePath)):
            currentFragment = ShaderFragmentInfo(cat, currentFilePath, lastLine) # getting fragment info
            dictTagToPath[currentFragment.getTag()]=currentFragment.getRelativePath()
            if currentFragment.getCat() == "feature":
                dictFeatureFunctionToTag[currentFragment.getFunctionName()]=currentFragment.getTag()
            lastLine=currentFragment.getLastLine()

# print dictTagToPath content (in a readable way) to debug
def print_dictTagToPath():
    for i in dictTagToPath:
        print(i+" : "+dictTagToPath[i])

# write the dictionnaries in the index file
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
    print("Complete")

# create the index by reading all features and utils
def createIndex():
    global dictTagToPath # dict with TAG for key and relative path for value
    dictTagToPath = {}
    global dictFeatureFunctionToTag # features dict with FUNCTION_NAME for key and tag for value
    dictFeatureFunctionToTag = {}
    fulfill(featuresDir)
    fulfill(utilsDir)
    writeIndex()

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   createIndex()
   sys.exit(0)
