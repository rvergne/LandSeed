# LandSeed - Documentation

## Features

Features are the main functions you can use in your terrainMap fonction (inside your input file) without any import.

| Function Name | Full Name | Short description |
|-|-|-|
| [fbm_gradient](features/fbm_gradient.md) | Fractal gradient | Compute fractalized gradient |
| [fbm_voronoi](features/fbm_voronoi.md) | Fractal voronoi | Compute fractalized voronoi |
| [phasor](features/phasor.md) | Phasor noise height map | Compute phasor noise hight map |
| [plateau](features/plateau.md) | Plateau | Flatten the terrain with smooth transition |


## Utils

Utils are the functions used to develop features.

| Function Name | Full Name | Short description |
|-|-|-|
| [gradient](utils/gradient.md) | Gradient noise | Compute gradient noise |
| [rand2](utils/rand2.md) | Hash 2D | A 2D hash function |
| [rand3](utils/rand3.md) | Hash 3D | A 3D hash function |
| [voronoi](utils/voronoi.md) | Voronoi noise | Compute voronoi noise |


## Templates

Templates are a way to gett different kind of output.  
The name is what you have to write in the input to choose which template to use for the output

| Name | Tag | Description |
|-|-|-|
| Classic shader | classic_shader |  Default fragment shader. Can be used with the python viewer script (in the output dir) to display it. |
| Heightmap | heightmap |  Heightmap fragment shader. Can be used with the python viewer script (in the output dir) to display it. |
| Shadertoy | shadertoy |  Fragment shader you can copy and paste in Shadertoy |
