# Classic shader

**Tag**: classic_shader

**Description**: Default fragment shader. Can be used with the python viewer script (in the output dir) to display it.

**Path**: LandSeed/data/Templates/classic_shader

**Parameters**:

| Tag | Type | Default Value | File | Description |
|-|-|-|-|-|
| RENDER_DISTANCE | float | 5000.0 | /output.frag | Choose the maximum distance to compute the terrain. Something between 2000.0 and 10000.0. |
| RAYMARCH_STEP_SIZE | float | 10.0 | /output.frag | Define the Raymarch step size. Something between 1.0 and 50.0. |
