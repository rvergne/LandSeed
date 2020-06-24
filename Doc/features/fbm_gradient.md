# fractal gradient

**Category**: feature

**Tag**: FBM_GRADIENT

**Function Name**: fbm_gradient

**Signature**: (vec2, float, float, float, int) -> float

**Name**: fractal gradient

**Spec**: Compute the gradient fractal brownian motion that will compute different level of a gradient noise and add them to create a final noise.

- pos : position of the terrain where you want to compute the height

- amplitude : the amplitude of the bigger noise we'll Compute

- frequency : the frequency of the noise computed

- persistence : amplitude will be multiplied by this value before each new noise computations

- nb_octave : how much level of noise you want to compute



