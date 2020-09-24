# LandSeed

LandSeed is a python library used to generate fragments shaders computing procedural terrains.

The idea is to use, combine or create features to generate various terrains with a single height function. The height mapping function will be used inside a templates to give the final result.

---

## Table of content

**[User part](#user)**

 - [Installation](#install)
 - [Generation](#generation)
 - [Documentation](#doc)

**[Developper part](#dev)**

 - [Test your work locally](#testlocally)
 - [Fragments (features and Utils)](#feature)
 - [Common Header](#commonheader)
 - [Templates](#template)


<br />

---
# <a name="user"></a>User part
---

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
pip3 install LandSeed
```
BE SURE THAT YOU USE PYTHON3 AND PIP3  

## <a name="generation"></a>How to generate a terrain

To generate a terrain, you need to fulfill a input file. Its purpose is to compute terrain height on a specific position. Some demo input files are implemented. You can try the generation with a demo file by calling   
```
LandSeed
```
This call will use the first demo file and generate a output folder at the location where you called the script.  
To see the generated result, please use the viewer in the output directory.
```
python3 output/viewer/py
```
Now, you may want to generate your own terrain. In order to generate a input file, use
```
LandSeed_newinput
```
The newly generated input file is located in the current folder.

The newly created input file contains a terrainMap function. Use the features functions inside it (see [documentation](Doc/main.md) for the list of existing features).
It has a template parameter at the beginning to choose a template, in order to get different kind of output. Templates can have some custom parameters that you can find in the [documentation](Doc/main.md). The line should look like this :
```
// @TEMPLATE template_tag PARAM1=VALUE PARAM2=VALUE
```
If there is no parameters, some defaults values will be taken. You don't have to declare every parameters, if some of them are missing, the default value for this one will be taken too.

## <a name="doc"></a>Documentation

To know more about implemented features, utils and templates, check the [documentation](Doc/main.md).

To update the documentation with your modifications or new files, just call the UpdateDoc.py script.

<br />

---
# <a name="dev"></a>Developper part
---

To extend the librairie of features or create a new template, please clone the project, get the last version by pulling master branch and create your own branch. Once your work is done you'll be able to create a pull request. More informations [here](https://yangsu.github.io/pull-request-tutorial/#:~:text=Pull%20requests%20let%20you%20tell,follow-up%20commits%20if%20necessary.) (If your not familiar with git and pull requests please read the topic before starting your work).  
Once your work is done and before you create the pull request, please call the UpdateDoc.py script to update the documentation.

## <a name="testlocally"></a>How to test your work locally

To test your work must have installed [virtualenv](https://pypi.org/project/virtualenv/).

**TL;DR** :  
A example testing script is in the root directory of the LandSeed repository. Calling it will create the virtualenv (in the parent folder), set it up, copy LandSeed/input/input.frag inside, run LandSeed on it and try to run the viewer in the ouput. Finally, the script will get out and remove properly the virtualenv. To resume : use the LandSeed/input/input.frag and call TestLandSeed.sh.

**Complete version** :  
Use ```virtualenv -p python3 NAME``` to create a virtual environnement using python3 and named NAME (see the virtualenv documentation for more informations).  
To use virtualenv shell, call ```source path/to/your/virtualenv/bin/activate```.  
Finally call ```pip install /path/to/the/cloned/landseed/repo/```. This will simulate a LandSeed installation in the virtualenv you just created.
To get out of virtualenv, just call ```deactivate```.

## <a name="feature"></a>Features and Utils

__Features__ are the functions used by the user in the terrainMap function to compute terrain height for a specific position on the terrain.  
__Utils__ are the functions you want to use inside your features without writting it everytime you need them.

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

The LINE_DIRECTIVE_ON enable the #line directive usage in the output shader (currently all disabled cause it doesn't work on intel GPU).

Once you finished writting your template, please call the UpdateDoc.py script to update the documentation.

When your template is ready to be added to the librairy and be available for everyone, create a pull request (Tutorial [here](https://yangsu.github.io/pull-request-tutorial/#:~:text=Pull%20requests%20let%20you%20tell,follow%2Dup%20commits%20if%20necessary.)).

## Known limitation

When using the viewer in classic_shader and fancy_shader templates, if you want to re generate output from shader, please call the viewer from the location of the input file.  
For instance, if you have :
```
.
├── input.frag
└── output
        ├── output.frag
        ├── vertex_shader.vert
        └── viewer.py
```

please do ```./output/viewer.py``` instead of ```cd output``` and ```./viewer.py```

## Random informations

pipreqs have been used to generate the setup.py dependencies. See [here](https://pypi.org/project/pipreqs/) for more informations.
