# Fractal voronoi

**Tag**: FBM_VORONOI

**Category**: feature

**Function Name**: fbm_voronoi

**Signature**: (vec2 pos, float amplitude, float frequency, float persistence, int nb_octave) -> float

**Spec**: Compute the voronoi fractal brownian motion that will compute different level of a voronoi noise and add them to create a final noise.

- pos : position of the terrain where you want to compute the height

- amplitude : the amplitude of the bigger noise we'll Compute

- frequency : the frequency of the noise computed

- persistence : amplitude will be multiplied by this value before each new noise computations

- nb_octave : how much level of noise you want to compute



**Path**: src/shader_code/features/fbm_voronoi.frag

