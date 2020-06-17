# Procedural terrain generation

## Generate terrain

Fulfill input file in the input folder. It's purpose is to compute terrain height on a specific position.

To generate the shader, use the generate.py python script.

Your generated shader is in the output folder with a python script allowing you to try it.

Soon it will be possible to create the output file somewhere else.

## Features

Features are the functions used by the user in the terrainMap function to compute terrain height for a specific position on the terrain.

### Current features

fbm_voronoi, fbm_gradient, plateau, you can see explanation in each file in the shaders/features/ folder.

(Documentation will come)

### Declare a new feature

Create a new file with the name of your feature and .fs extention. Inside, please use the common header as specified below so your feature can be automatically included in the librairy. After the common header, start the code with your tag in commentary, and end your code with @END tag.

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

## Declare a new noise

Same operating mode as feature but noises are stored in the shaders/utils/noises/ folder.

Your noise tag should start with @NOISE_

## Add a Utils function

Same operating mode as feature but functions are stored in the shaders/utils/ folder.

For the moment, new feature need a modification in the python script to be operationnal. Will change.

## Common Header
See examples in any files using this header.
```
// --------------DEV-----------------
// @TAG TAG_USED_TO_INCLUDE
// @SPEC {
//	(function_param_type) -> function_result_type
// }
// -------------USER-----------------
// @NAME name used for user doc
// @SPEC {
// definition of the function functionnement, effect...everything needed to use it
// param1 : description of parameter 1
// param2 : description of parameter 2
// ...
// }
// -------------END------------------
```