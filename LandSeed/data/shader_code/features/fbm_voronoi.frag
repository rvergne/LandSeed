// --------------DEV-----------------
// @TAG FBM_VORONOI
// @FUNCTION_NAME fbm_voronoi
// @SIGNATURE (vec2 pos, float amplitude, float frequency, float persistence, int nb_octave) -> float
// -------------USER-----------------
// @NAME Fractal voronoi
// @SHORT Compute fractalized voronoi
// @SPEC {
// Compute the voronoi fractal brownian motion that will compute different level of a voronoi noise and add them to create a final noise.
// pos : position of the terrain where you want to compute the height
// amplitude : the amplitude of the bigger noise we'll Compute
// frequency : the frequency of the noise computed
// persistence : amplitude will be multiplied by this value before each new noise computations
// nb_octave : how much level of noise you want to compute
// }
// -------------END------------------

// @FBM_VORONOI
// @INCLUDE VORONOI
float fbm_voronoi(in vec2 p,in float amplitude,in float frequency,in float persistence, in int nboctaves) {
        float a = amplitude;
        vec2 x = p*vec2(frequency,frequency);
        float h = 0.;
        mat2 m = mat2(1.,0.,0.,1.);
        const mat2 m2 = mat2(  0.80,  0.60, -0.60,  0.80 );

        for(int i=0;i<nboctaves;++i) {
                float n = voronoi(x); // get noise + derivative at x

                h = h+a*n; // accum noise with a given amplitude

                a = a*persistence; // update amplitude for next octave
                x = 2.5*m2*x; // scale point to the next octave and apply a rotation (avoid grid patterns?)
        }

        return h;
}
// @END
