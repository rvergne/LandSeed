# LandSeed - Documentation

## Features

Features are the main functions you can use in your terrainMap fonction (inside your input file) without any import.

| Function Name | Full Name | Tag |
|-|-|-|
| [fbm_gradient](features/fbm_gradient.md) | Fractal gradient | FBM_GRADIENT |
| [fbm_voronoi](features/fbm_voronoi.md) | Fractal voronoi | FBM_VORONOI |
| [phasor](features/phasor.md) | Phasor noise height map | PHASOR |
| [plateau](features/plateau.md) | Plateau | PLATEAU |


## Utils

Utils are the functions used to develop features.

| Function Name | Full Name | Tag |
|-|-|-|
| [gradient](utils/gradient.md) | Gradient noise | GRADIENT_2D |
| [rand2](utils/rand2.md) | 2D hash function | RANDOM_2D |
| [rand3](utils/rand3.md) | 3D hash function | RANDOM_3D |
| [voronoi](utils/voronoi.md) | Voronoi noise | VORONOI_2D |


## Templates

Templates are a way to gett different kind of output.  
The name is what you have to write in the input to choose which template to use for the output

| Name | Tag | Description |
|-|-|-|
| Classic shader | classic_shader |  Default fragment shader. Can be used with the python viewer script (in the output dir) to display it. |
| Heightmap | heightmap |  Heightmap fragment shader. Can be used with the python viewer script (in the output dir) to display it. |
| Shadertoy | shadertoy |  Fragment shader you can copy and paste in Shadertoy |
