#Procedural terrain generation

##How to generate terrain
// WORK IN PROGRESS

##How to add a new noise :
First of all, create your noise shader following the next standards:

- create a folder with the noise name in the shaders/noises/ directory
- your noise function(s) should be named just as the noise
- for a 2D noise call the shader fragment_shader2D.fs

Annotations :
Annotate the differents part of the noise shader as follow

- @GEN_HEADER : contain header and parameters (such as #define or const). Basically all global parameters
- @GEN_REQ : requirements, all the functions needed for the noise function to work well
- @GEN_NOISE : The noise function
   
Then call the generate_noise_code_fragments script to generate every components for the shader generation. Every component will be stored in the noise sub-dir code_gen. // WORK IN PROGRESS

##Noise tester
To try a noise, use the test.sh script in the testnoise directory.