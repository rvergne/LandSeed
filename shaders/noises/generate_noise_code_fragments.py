#!/usr/bin/env python3
import os


# copy the code fragment in the file
def copy_fragment(file):
    print("WORK IN PROGRESS")

# return boolean value. True if the line contain one of the annotation we're looking for
def contains_annotation(line):
    print("WORK IN PROGRESS")

# Get all directories (noises)
noises = os.listdir()
noises.remove(__file__) #remove this script from the list

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
# do every noises
for noise in noises:
    print(dir_path+"/"+noise)
    print(os.path.exists(dir_path+"/"+noise))
    # se déplacer dans le repertoire ou stocker son chemin
    # vérifier l'existence du dossier code_gen
        # si non le créer
    # parcourir le shader
    # si une annotation, créer fichier correspondant then call copy_fragment



# Do a final check? would check if every noise has every fragments created.
