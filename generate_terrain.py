#!/usr/bin/env python3
import os
import sys

def contains_annotation(line):
    return "@NOISE_HEADER" in line or "@FEATURE_HEADER" in line or "@NOISE_REQUIREMENT" in line or "@FEATURE_REQUIREMENT" in line or "@NOISE_CODE" in line or "@FEATURE_CODE" in line or "@FEATURE_FUNCTIONS" in line or "@FEATURE_USE" in line;

def copy_all_file(input, output):
    lines = input.readlines()
    for line in lines:
        output.write(line)

# TODO do better : appel de bruit pas beau, prev pas beau
def copy_all_file_feature_code(input, output, noise_name):
    lines = input.readlines()
    prev=False
    for i in range(len(lines)):
        if "@NOISE" in lines[i]:
            output.write("\tn="+noise_name+"(x");
            if noise_name=="cellular" :
                output.write(",DIVISION,F);\n");
            else:
                output.write(");\n");
            prev=True
        elif prev:
            prev=False;
        else:
            output.write(lines[i])

def replace_annotation(file, line, noise_list, noise, noise_count, feature_list, feature):
    if "@NOISE_HEADER" in line:
        for i in range(len(noise_count)):
            if noise_count[i] > 0:
                copy_all_file(open("shaders/noises/"+noise_list[noise[i]]+"/code_fragment/header.fs", 'r'),file)
    elif "@FEATURE_HEADER" in line:
        for i in range(len(feature)):
            if feature[i] != 0:
                copy_all_file(open("shaders/terrains/features/"+feature_list[i]+"/code_fragment/header.fs", 'r'),file)
    elif "@NOISE_REQUIREMENT" in line:
        for i in range(len(noise_count)):
            if noise_count[i] > 0:
                copy_all_file(open("shaders/noises/"+noise_list[noise[i]]+"/code_fragment/requirements.fs", 'r'),file)
    elif "@FEATURE_REQUIREMENT" in line:
        for i in range(len(feature)):
            if feature[i] != 0:
                copy_all_file(open("shaders/terrains/features/"+feature_list[i]+"/code_fragment/requirements.fs", 'r'),file)
    elif "@NOISE_CODE" in line:
        for i in range(len(noise_count)):
            if noise_count[i] > 0:
                copy_all_file(open("shaders/noises/"+noise_list[noise[i]]+"/code_fragment/noise.fs", 'r'),file)
    elif "@FEATURE_CODE" in line:
        for i in range(len(feature)):
            if feature[i] != 0:
                copy_all_file_feature_code(open("shaders/terrains/features/"+feature_list[i]+"/code_fragment/code.fs", 'r'),file, noise_list[noise[i]])
    elif "@FEATURE_FUNCTIONS" in line:
        for i in range(len(feature)):
            if feature[i] != 0:
                copy_all_file(open("shaders/terrains/features/"+feature_list[i]+"/code_fragment/function.fs", 'r'),file)
    elif "@FEATURE_USE" in line:
        for i in range(len(feature)):
            if feature[i] != 0:
                for j in range(feature[i]):
                    # TODO DO BETTER
                    if feature_list[i] == "base_relief":
                        file.write("\tterrain += base_relief(pos, AMP/3, FREQ*1.5, PERS, NUM_OCTAVES);\n")
                    else:
                        file.write("\tterrain += mountains(pos, AMP*1.3, FREQ/2.5);\n")
    else:
        print("ERROR")

# show differents features availables TODO check validity
print("Please choose available feature : ")
feature_list = os.listdir("shaders/terrains/features/")
feature = []
noise = []
for i in range(len(feature_list)):
    print(str(i)+":"+feature_list[i])
    feature.append(0)
    noise.append(-1)
# feature array correspond on how mush user want for each features

# ask to the user what do he want and store it in an array
more=True
while more or entry < 0 or entry >= len(feature_list):
    print("Choice : ", end="")
    entry=int(input())
    if entry < 0 or entry >= len(feature_list):
        print("wrong value, please try again")
    else:
        feature[entry]+=1
        print("Do you want to add more feature?(y/n)")
        more=("y"==input())


# show differents noises availables TODO check validity
print("Please choose available noise for each different features : ")
noise_list = os.listdir("shaders/noises/")
noise_count = []
for i in range(len(noise_list)):
    print(str(i)+":"+noise_list[i])
    noise_count.append(0)
# ask to user to choose a noise for each features noise[i] = x correspond to : the ith feature will be done with the xth noise
for i in range(len(feature)):
    if feature[i] != 0:
        print("Pick a noise for "+feature_list[i]+" : ", end="")
        entry = -1
        while entry < 0 or entry >= len(noise_list):
            entry = int(input())
            if entry < 0 or entry >= len(noise_list):
                print("Wrong value, please try again")
        noise[i] = entry

# Debug
for i in range(len(feature)):
    if feature[i] != 0:
        print("Feature "+feature_list[i]+" will be done with the "+noise_list[noise[i]]+" noise")

for i in range(len(noise)):
    if noise[i]!=-1:
        noise_count[noise[i]]+=1

# Create the corresponding shader.
input_shader = open("shaders/terrains/empty/fragment_shader01.fs", "r")
input_shader_content = input_shader.readlines()
output_shader = open("output/fragment_shader01.fs", "w")

for i in range(len(input_shader_content)):
    if contains_annotation(input_shader_content[i]):
        replace_annotation(output_shader, input_shader_content[i], noise_list, noise, noise_count, feature_list, feature);
    else:
        output_shader.write(input_shader_content[i])




# TODO ajouter water
# Late TODO : plusieurs fois la même feature avec différents bruits.
