# Classic shader

**Tag**: classic_shader

**Description**: Default fragment shader. Can be used with the python viewer script (in the output dir) to display it.

**Path**: /src/Templates/classic_shader/

**Parameters (use them in that order in the input file)**:

- RENDER_DISTANCE: float, default value : 5000.0 Is used in output.frag. Description : Choose the maximum distance to compute the terrain. Something between 2000.0 and 10000.0.
- RAYMARCH_STEP_SIZE: float, default value : 10.0 Is used in output.frag. Description : Define the Raymarch step size. Something between 1.0 and 50.0.
