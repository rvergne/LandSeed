#!/usr/bin/env python3
import os
import sys

# copy the code fragment in the file
# return last line checked
def copy_fragment(start, file_content, path):
    if "@GEN_HEADER" in file_content[start]:
        file=open(path+"/header.fs", "w")
    elif "@GEN_REQ" in file_content[start]:
        file=open(path+"/requirements.fs", "w")
    elif "@GEN_NOISE" in file_content[start]:
        file=open(path+"/noise.fs", "w")
    else:
        print("FILE_ERROR")
        return start
    i=start+1
    #TODO : Ajouter check fin de fichier (pareil dans feature)
    while not "@END" in file_content[i]:
        file.write(file_content[i])
        i+=1
    file.close()
    return i

# return boolean value. True if the line contain one of the annotation we're looking for
def contains_annotation(line):
    return ("@GEN_HEADER" in line) or ("@GEN_REQ" in line) or ("@GEN_NOISE" in line)

# remove all files in the specified dir
def clear_dir(dir):
    files_in_dir=os.listdir(dir)
    for file in files_in_dir:
        os.remove(dir+"/"+file)

def generate():
    oldDir= os.getcwd()

    # Get current path
    noises_path = os.path.dirname(os.path.realpath(__file__))+"/shaders/noises"
    os.chdir(noises_path)

    # Get all directories (noises)
    noises = os.listdir()

    # do every noises
    for noise in noises:
        print("Generating code fragments for "+noise+" noise")

        current_noise_dir=noises_path+"/"+noise
        code_gen_dir=current_noise_dir+"/code_fragment"

        #preparing the structure
        if not os.path.exists(code_gen_dir): # Check code_gen dir existence. If it doesn't exist, create it
            os.makedirs(code_gen_dir)
        clear_dir(code_gen_dir) # removing all old code fragments

        shader_file = open(current_noise_dir+"/"+"fragment_shader2D.fs","r") # open the shader noise file
        shader_content=shader_file.readlines()
        for i in range(len(shader_content)): # browse the shader
            if contains_annotation(shader_content[i]):
                skip=copy_fragment(i, shader_content, code_gen_dir) # if we detect a Annotation, copy the content in the corresponding code fragment
                i=skip
        shader_file.close()

    # check that every file have been created
    print("Checking that everything worked", end="...")
    for noise in noises:
        error=False
        current_noise_dir=noises_path+"/"+noise
        code_gen_dir=current_noise_dir+"/code_fragment"
        if not (os.path.exists(code_gen_dir+"/header.fs") and os.path.exists(code_gen_dir+"/requirements.fs") and os.path.exists(code_gen_dir+"/noise.fs")):
            error=True

    os.chdir(oldDir) # Go back where the script has been called

    if not error:
        print("OK")
        sys.exit(404)
    else:
        print("ERROR IN FILE TREE")
        sys.exit(-1)

def main():
    generate()

main()
