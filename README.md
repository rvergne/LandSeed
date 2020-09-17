# LandSeed

LandSeed is a python library used to generate fragments shaders computing procedural terrains.

The idea is to use, combine or create features to generate various terrains with a single height function. The height mapping function will be used inside a templates to give the final result.

## Table of content

 - [Installation](#install)
 - [Generation](#generation)
 - [Fragments (features and Utils)](#feature)
 - [Common Header](#commonheader)
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
pip3 install -r requirements.txt
```
BE SURE THAT YOU USE PYTHON3 AND PIP3  
pipreqs have been used to generate those dependencies. See [here](https://pypi.org/project/pipreqs/) for more informations.

## <a name="generation"></a>Generate terrain

Fulfill input file in the input folder. Its purpose is to compute terrain height on a specific position. Some demo input files are implemented. You can call them by entering their path or do the following from the LandSeed root location :  
```
cp input/demo2.frag input/input.frag
```
Use the features functions inside the terrain map function (see [documentation](Doc/main.md) for the list of existing features). You can also add functions in input file.  
It has a template parameter at the beginning to choose a template, in order to get different kind of output. Templates can have some custom parameters that you can find in the [documentation](Doc/main.md). If there is no parameters, some defaults values will be taken.

To generate the shader, use the LandSeed.py python script.

There is two ways to use the generation script :
```
./LandSeed.py
or
./LandSeed.py [input path] [output path]
```
Please give paths relative to lib root.

By default, your generated files and shader is in the output folder so you can call
```
./output/viewer.py
```
(The previous command will work if you used one of the templates with the viewer such as classic_shader or fancy_shader)

The first one will choose default input and output files. The second will take input and output according to the parameter you give.

## <a name="feature"></a>Features and Utils

__Features__ are the functions used by the user in the terrainMap function to compute terrain height for a specific position on the terrain.  
__Utils__ are the functions you want to use inside your features without writting it everytime you need them.

### Use a feature

To use a feature, you just have to call the function in the input without doing anything else.

### Declare a new feature<a name="newfeature"></a>

Create a new file in src/shader_code/features/ folder. PLEASE USE THE MAIN FUNCTION NAME OF YOUR FEATURE AS TAG AND FILE NAME !! (your_function.frag as file name)  
Inside, please use the common header as specified [below](#commonheader) so your feature can be automatically included in the librairy. After the common header, start the code with your tag in commentary, and end your code with @END tag.  

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
To know the tags and specifications of the different features, please refer to the [documentation](Doc/main.md).

### Declare a new utils function

Same operating mode as feature but are stored in the src/shader_code/utils/ folder.

## <a name="commonheader"></a>Common Header
See examples in any files using this header.
```
// --------------DEV-----------------
// @TAG TAG_USED_TO_INCLUDE
// @FUNCTION_NAME name_of_the_function
// @SIGNATURE (param1_type param1_name,...) -> function_result_type
// -------------USER-----------------
// @NAME name used for user doc
// @SHORT short description
// @SPEC {
// definition of the function functionnement, effect...everything needed to use it
// param1_name : description of parameter 1
// param2_name : description of parameter 2
// ...
// }
// -------------END------------------
```

## <a name="template"></a>Templates

Templates allows you to get different kind of input. A template is directory containing as much files and subfolder as you want. Its structure always have a GLSL file that will be fulfilled with the terrainMap function and all its dependencies.  
See in the [documentation](Doc/main.md) to have some informations about the purpose of each templates.

A template directory should always contains the following configuration file (at root of the template dir) named template.config :
```
@NAME Name of the template
@TAG tag of the template (used in input file to define which on should be used)
@GEN_FILE The path of the file containing the @TERRAIN_MAP. (path should be relative to the root of the template, so if the file is at the root of the template, just put the file name)
@LINE_DIRECTIVE_ON (TRUE or FALSE) to choose if you want to enable the #line directive in the generation
@DESC { Description for the documentation }
@PARAM TAG_OF_THE_PARAM TYPE FILE_WHERE_TO_REPLACE DEFAULT=VALUE
@PARAM_DESC TAG_OF_THE_PARAM { Description for the doc }
....

```  
You can add some param lines as much as you want. They have to be by two, so every parameters is documented. The param will need to be put in the input file in the order you've put them in the configuration file.

The LINE_DIRECTIVE_ON enable the #line directive usage in the output shader.

Once you finished writting your template, please call the UpdateDoc.py script to update the documentation.

When your template is ready to be added to the librairy and be available for everyone, create a pull request (Tutorial [here](https://yangsu.github.io/pull-request-tutorial/#:~:text=Pull%20requests%20let%20you%20tell,follow%2Dup%20commits%20if%20necessary.)).

## <a name="doc"></a>Documentation

To know more about implemented features, utils and templates, check the [documentation](Doc/main.md).

To update the documentation with your modifications or new files, just call the UpdateDoc.py script.

## Work in progress

First packaged release 
