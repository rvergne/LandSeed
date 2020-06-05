# Procedural terrain generation

## How to generate terrain
To generate a terrain, use the generate_terrain.py python script.

## How to add a new noise :
First of all, create your noise shader following the next standards:

- create a folder with the noise name in the shaders/noises/ directory
- your noise function(s) should be named just as the noise
- for a 2D noise call the shader fragment_shader2D.fs

Annotations :
Annotate the differents part of the noise shader as follow

- @GEN_HEADER : contain header and parameters (such as #define or const). Basically all global parameters
- @GEN_REQ : requirements, all the functions needed for the noise function to work well
- @GEN_NOISE : The noise function

Then call the generate_noise_code_fragments python script to generate every components for the shader generation. Every component will be stored in the noise sub-dir code_gen.

## How to add a new noise :
First of all, create your feature shader following the next standards:

- create a folder with the feature name in the shaders/terrains/features directory
- your shader should be named fragment_shader01.fs
- your feature function(s) should be named just as the noise

Annotations :
Annotate the differents part of the noise shader as follow

- @GEN_FEATURE_HEADER : contain header and parameters (such as #define or const). Basically all global parameters
- @GEN_FEATURE_REQUIREMENT : requirements, all the functions needed for the feature function to work well
- @GEN_FEATURE_CODE : The feature function
- @GEN_FEATURE_FUNCTION : The high-level function that will be called by the user to add your feature. Basically just calling your feature function

The noise call must be in GEN_FEATURE_CODE part (for the moment) as follow :
@NOISE
n=noise_name(x);

Then call the generate_feature_code_fragments python script to generate every components for the shader generation. Every component will be stored in the feature sub-dir code_gen.


## Noise tester
To try a noise, use the test.sh script in the testnoise directory.
