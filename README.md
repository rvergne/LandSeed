# Procedural terrain generation

## Lib installation and requirements

To install everything you need please do the following steps :

- If you don't have python, pip and glfw installed (python 3+ is needed):
```
apt install python3
apt install python3-pip
apt install libglfw3
```
- To install dependencies :
```
pip install -r requirements.txt
```
pipreqs have been used to generate those dependencies. See [here](https://pypi.org/project/pipreqs/) for more informations.

## Generate terrain

Fulfill input file in the input folder. It's purpose is to compute terrain height on a specific position.

To generate the shader, use the generate.py python script.

Your generated shader is in the output folder with a python script allowing you to try it.

There is two ways to use the generation script :
```
python generation.py
or
python generation.py [input path] [output path]
```
The first one will choose default input and output files. The second will take input and output according to the parameter you give.

## Documentation

To know more about implemented features and utils, check the [documentation](Doc/main.md).
To update the documentation with your modifications or new files, just call the UpdateDoc.py script.

## Features

Features are the functions used by the user in the terrainMap function to compute terrain height for a specific position on the terrain.

### Declare a new feature

Create a new file in shaders/features/ folder. Inside, please use the common header as specified below so your feature can be automatically included in the librairy. After the common header, start the code with your tag in commentary, and end your code with @END tag.

Put your feature code between your tag and @END tag. You can use any noise or function adding it with the tag @INCLUDE TAG. The include should be between you function tag and it's beginning. Here is an example :
```
// COMMON HEADER HERE
//
// @YOUR_FEATURE_TAG
// @INCLUDE TAG
// @INCLUDE TAG
Your_feature_function(){
...
}
// @END
```

## Declare a new noise or utils function

Same operating mode as feature but are stored in the shaders/utils/ folder.


## Common Header
See examples in any files using this header.
```
// --------------DEV-----------------
// @TAG TAG_USED_TO_INCLUDE
// @FUNCTION_NAME name_of_the_function
// @SIGNATURE (param1_type param1_name,...) -> function_result_type
// -------------USER-----------------
// @NAME name used for user doc
// @SPEC {
// definition of the function functionnement, effect...everything needed to use it
// param1_name : description of parameter 1
// param2_name : description of parameter 2
// ...
// }
// -------------END------------------
```
