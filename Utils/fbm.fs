#define NUM_OCTAVES 5

// 1D fbm
float fbm(float x, int num_octave) {
	float v = 0.0;
	float a = 0.5;
	float shift = float(100);
	for (int i = 0; i < num_octave; ++i) {
		v += a * noise(x);
		x = x * 2.0 + shift;
		a *= 0.5;
	}
	return v;
}

// 2D fbm
float fbm(vec2 x, int num_octave) {
	float v = 0.0;
	float a = 0.5;
	vec2 shift = vec2(100);
	// Rotate to reduce axial bias
    mat2 rot = mat2(cos(0.5), sin(0.5), -sin(0.5), cos(0.50));
	for (int i = 0; i < num_octave; ++i) {
		v += a * noise(x);
		x = rot * x * 2.0 + shift;
		a *= 0.5;
	}
	return v;
}

// 3D fbm
float fbm(vec3 x, int num_octave) {
	float v = 0.0;
	float a = 0.5;
	vec3 shift = vec3(100);
	for (int i = 0; i < num_octave; ++i) {
		v += a * noise(x);
		x = x * 2.0 + shift;
		a *= 0.5;
	}
	return v;
}

// better version with parameters :
float fbm(in vec2 p,in float amplitude,in float frequency,in float persistence, in int nboctaves) {
        float a = amplitude;
        vec2 x = p*vec2(frequency,frequency);
        float h = 0.;
        mat2 m = mat2(1.,0.,0.,1.);
        const mat2 m2 = mat2(  0.80,  0.60, -0.60,  0.80 );

        for(int i=0;i<nboctaves;++i) {

                float n = gradient(x); // get noise + derivative at x

                h = h+a*n; // accum noise with a given amplitude

                a = a*persistence; // update amplitude for next octave
                x = 2.5*m2*x; // scale point to the next octave and apply a rotation (avoid grid patterns?)
        }

        return h;
}
