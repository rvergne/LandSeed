#!/usr/bin/env python3
from src.LibUtils.TemplateInfoClass import TemplateInfo
from src.LibUtils.LibPaths import templatesDir

print("Test for : "+templatesDir+"classic_shader")
x = TemplateInfo(templatesDir+"classic_shader")
print("Test for : "+templatesDir+"heightmap")
y = TemplateInfo(templatesDir+"heightmap/")
print("Test for : "+templatesDir+"shadertoy")
z = TemplateInfo(templatesDir+"shadertoy/")
