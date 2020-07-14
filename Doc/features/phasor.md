# Phasor noise height map

**Tag**: PHASOR

**Category**: feature

**Function Name**: phasor

**Signature**: (vec2 pos, float amplitude, float angle, float frequency, float bandwidth, bool normalized) -> float

**Spec**: Compute a height map using procedural phasor noise with a sine profile.

- pos : current terrain position

- amplitude : amplitude of the resulting noise

- angle : angle of the main oscillation pattern

- frequency : frequency of the oscillations

- bandwidth : bandwidth of the noise kernels (inverse of the noise radius)

- normalized : true if all oscillations should use the full range [0, amplitude]. false to allow contrast variations



