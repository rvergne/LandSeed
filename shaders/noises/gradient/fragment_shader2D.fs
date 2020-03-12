#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

int NUM_OCTAVES = 6;

// Random function is taken with arbitrary values who can be modified here
// source : https://thebookofshaders.com/edit.php#11/2d-gnoise.frag
vec2 rand2(vec2 st){
    st = vec2( dot(st,vec2(127.1,311.7)),
              dot(st,vec2(269.5,183.3)) );
    return -1.0 + 2.0*fract(sin(st)*43758.5453123);
}

// source : https://www.shadertoy.com/view/XdXGW8
float gradient(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    vec2 u = f*f*(3.0-2.0*f);

    return mix( mix( dot( rand2(i + vec2(0.0,0.0) ), f - vec2(0.0,0.0) ),
                     dot( rand2(i + vec2(1.0,0.0) ), f - vec2(1.0,0.0) ), u.x),
                mix( dot( rand2(i + vec2(0.0,1.0) ), f - vec2(0.0,1.0) ),
                     dot( rand2(i + vec2(1.0,1.0) ), f - vec2(1.0,1.0) ), u.x), u.y);
}

float fbm(vec2 x, int num_octave) {
	float v = 0.0;
	float a = 0.5;
	vec2 shift = vec2(100);
	// Rotate to reduce axial bias
    mat2 rot = mat2(cos(0.5), sin(0.5), -sin(0.5), cos(0.50));
	for (int i = 0; i < num_octave; ++i) {
		v += a * gradient(x);
		x = rot * x * 2.0 + shift;
		a *= 0.5;
	}
	return v;
}

vec3 compute_color(vec2 coord){
    if(NUM_OCTAVES > 1)
        return vec3(fbm(coord, NUM_OCTAVES))*.5+.5;
    else
        return vec3(gradient(coord))*.5+.5;
}

void main()
{
    vec2 coord = vec2(fragCoord.x,fragCoord.y*aspectRatio);
    coord *= 10.0;
    outColor = vec4(compute_color(coord),1.0);
}
