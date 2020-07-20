# LandSeed

LandSeed is a python library used to generate fragments shaders computing procedural terrains.

The idea is to use, combine or create features to generate various terrains with a single height function. The height mapping function will be used inside a templates to give the final result.

## Table of content

 - [Installation](#install)
 - [Generation](#generation)
 - [Fragments (features and Utils)](#feature)
 - [Templates](#template)
 - [Documentation](#doc)

## <a name="install"></a>Lib installation and requirements

To install everything you need, please do the following steps :

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

## <a name="generation"></a>Generate terrain

Fulfill input file in the input folder. Its purpose is to compute terrain height on a specific position.  
It has two parameters at the begining of the file, the first is the quality indice, a percentage defining if the output should give priority to speed or render quality (Work in progress).  The second one is used to choose a template, in order to get different kind of output.
Use the features functions inside it. You can also add functions in input file.

To generate the shader, use the Generate.py python script.

There is two ways to use the generation script :
```
./Generation.py
or
./Generation.py [input path] [output path]
```
Please give relative paths.

By default, your generated shader is in the output folder.

The first one will choose default input and output files. The second will take input and output according to the parameter you give.

## <a name="feature"></a>Features and Utils

__Features__ are the functions used by the user in the terrainMap function to compute terrain height for a specific position on the terrain.  
__Utils__ are the functions you want to use inside your features without writting it everytime you need them.

### Use a feature

To use a feature, you just have to call the function in the input without doing anything else.

### Declare a new feature<a name="newfeature"></a>

Create a new file in src/shader_code/features/ folder. Inside, please use the common header as specified below so your feature can be automatically included in the librairy. After the common header, start the code with your tag in commentary, and end your code with @END tag.  
PLEASE USE THE MAIN FUNCTION NAME OF YOUR FEATURE AS TAG AND FILE NAME !! (your_function.frag as file name)

Put your feature code between your tag and @END tag. You can use any existing util or feature adding it with the tag @INCLUDE TAG. The include should be between you function tag and it's beginning. Here is an example :
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

Once you finished writting your feature, please call the UpdateDoc.py script to update the documentation.

When your feature is ready to be added to the librairy and be available for everyone, create a pull request (Tutorial [here](https://yangsu.github.io/pull-request-tutorial/#:~:text=Pull%20requests%20let%20you%20tell,follow%2Dup%20commits%20if%20necessary.)).

### Use a utils

As explained in the [Declare a new feature](#newfeature) section, to use a util in a feature (or Util) file, please use the @INCLUDE tag with the tag of the util.  
To know the tag of the feature you want to use, please refer to the [documentation](Doc/main.md).

### Declare a new utils function

Same operating mode as feature but are stored in the src/shader_code/utils/ folder.

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

## <a name="template"></a>Templates

Templates allows you to get different kind of input. See in the [documentation](Doc/main.md) to have some informations about the purpose of every templates.

A template should always start with the following header :
```
// --------------DEV-----------------
// @LINE_DIRECTIVE_ON BOOLEAN
// @TAG [your template tag used in the input file]
// --------------USER----------------
// @NAME [name of the template]
// @DESC {
// Description of the template for the documentation
// }
// --------------END-----------------
```

The LINE_DIRECTIVE_ON enable the #line directive usage in the output shader.

Once you finished writting your template, please call the UpdateDoc.py script to update the documentation.

When your template is ready to be added to the librairy and be available for everyone, create a pull request (Tutorial here).

## <a name="doc"></a>Documentation

To know more about implemented features, utils and templates, check the [documentation](Doc/main.md).

To update the documentation with your modifications or new files, just call the UpdateDoc.py script.

## Future improvement

- Define in the input file if the output should give priority to quality or computation speed.
    - put tag before quality param : with a RANGE definition
- Packaging
