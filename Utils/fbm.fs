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
