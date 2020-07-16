#!/usr/bin/env python3
from src.LibUtils.UpdateIndex import getMostRecentTemplateChange
import os
from src.LibUtils.LibPaths import templatesDir, generatorIndex

updateDate = os.path.getmtime(generatorIndex)   # Creation time of index
templateUpdateDate = os.path.getmtime(getMostRecentTemplateChange(templatesDir).path)
print(templateUpdateDate)
if updateDate > os.path.getmtime(templateUpdateDate):
    print("Index more recent")
else:
    print("template more recent")
