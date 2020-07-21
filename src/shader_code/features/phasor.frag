// --------------DEV-----------------
// @TAG PHASOR
// @FUNCTION_NAME phasor
// @SIGNATURE (vec2 pos, float amplitude, float angle, float frequency, float bandwidth, bool normalized) -> float
// -------------USER-----------------
// @NAME Phasor noise height map
// @SHORT Compute phasor noise hight map
// @SPEC {
// Compute a height map using procedural phasor noise with a sine profile.
// pos : current terrain position
// amplitude : amplitude of the resulting noise
// angle : angle of the main oscillation pattern
// frequency : frequency of the oscillations
// bandwidth : bandwidth of the noise kernels (inverse of the noise radius)
// normalized : true if all oscillations should use the full range [0, amplitude]. false to allow contrast variations
// }
// -------------END------------------

// @PHASOR
#define M_PI 3.14159265358979323846
const uint PHASOR_LCG_N = 15487469u;
uint hash(uint x) {
    x = ((x >> 16) ^ x) * 0x45d9f3bu;
    x = ((x >> 16) ^ x) * 0x45d9f3bu;
    x = ((x >> 16) ^ x);
    return x;
}
void seed(inout uint x_, uint s) { x_ = hash(s) % PHASOR_LCG_N; }
uint next(inout uint x_) {
    x_ *= 3039177861u;
    x_ = x_ % PHASOR_LCG_N;
    return x_;
}
float uni_0_1(inout uint x_) { return float(next(x_)) / float(PHASOR_LCG_N); }
float uni(inout uint x_, float min, float max) {
    return min + (uni_0_1(x_) * (max - min));
}

uint phasor_morton(uint x, uint y) {
    uint z = 0u;
    for (uint i = 0u; i < 32u * 4u; i++) {
        z |= ((x & (1u << i)) << i) | ((y & (1u << i)) << (i + 1u));
    }
    return z;
}

float bessel_3(float x) {
    float y = 0.5 * x;
    float y2 = (y * y);
    return (y2 * y *
            (1.0 / 6.0 +
             y2 * (1.0 / 24.0 +
                   y2 * (1.0 / 240.0 + y2 * (1.0 / 4320.0 + y2 / 120960.0)))));
}

float phasor_window(vec2 x, float radius) {
    // Kaiser-Bessel window function for continuity
    float r = length(x) / radius;

    float t = sqrt(1.0 - pow(r, 2.0));
    return float(bessel_3(3.0 * M_PI * t) / bessel_3(M_PI * 3.0));
}

float phasor(vec2 pos, float amplitude, float angle, float frequency,
             float bandwidth, bool normalized) {
    // The cell size is the kernel radius
    // The kernel radius is sqrt(-log(0.05) / M_PI) / bandwidth
    const float THRESHOLD = 0.05;
    float RADIUS = sqrt(-log(THRESHOLD) / M_PI) / bandwidth;

    // Find current index in grid
    ivec2 cgridCell = ivec2(floor(pos / RADIUS));
    ivec2 cg;

    // Static configuration
    const int LOOKAHEAD = 1;
    const int NKERNELS = 4;

    // Complex accumulator
    vec2 res = vec2(0.);
    vec2 w = vec2(cos(angle), sin(angle));

    // Look at neighbor cells for contributions
    for (cg.x = cgridCell.x - LOOKAHEAD; cg.x <= cgridCell.x + LOOKAHEAD;
         ++cg.x) {
        for (cg.y = cgridCell.y - LOOKAHEAD; cg.y <= cgridCell.y + LOOKAHEAD;
             ++cg.y) {
            // Seed the rng using a hash of the current cell number
            uint rngState;
            seed(rngState, hash(333u + phasor_morton(uint(cg.x), uint(cg.y))));

            // Now generate impulses
            for (int k = 0; k < NKERNELS; ++k) {
                // Impulse center in world coordinates
                vec2 impulseCenter =
                    RADIUS *
                    (vec2(cg) + vec2(uni_0_1(rngState), uni_0_1(rngState)));
                // Vector from current pos to impulse center
                vec2 d = pos - impulseCenter;
                // Gaussian parameter
                float g = phasor_window(d, RADIUS);

                if (g >= 0.0) {
                    // Contribute oscillating part
                    float ph = 2. * M_PI * frequency * dot(d, w);
                    res += g * vec2(cos(ph), sin(ph));
                }
            }
        }
    }

    res /= sqrt(float(NKERNELS));

    // Compute phasor noise at the right amplitude
    return amplitude * (normalized ? 1.0 : length(res)) *
           (.5 + .5 * sin(atan(res.y, res.x)));
}
// @END
