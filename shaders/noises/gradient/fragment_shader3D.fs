#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

int NUM_OCTAVES = 6;

// -------------------------------------------------
// ---------------Sphere Render Part----------------
// -------------------------------------------------
#define DIST_MIN 1e-5 // minimum distance to objects
#define DIST_MAX 1e+5 // maximum distance to objects

// ray structure
struct Ray
{
  vec3 ro; // origin
  vec3 rd; // direction
};
// sphere structure
struct Sphere
{
  vec3 c; // center
  float r; // radius
};

// struct for remembering intersected object
struct ISObj
{
  float d; // distance to the object
  int t; // type (-1=nothing,0=plane, 1=sphere)
  int i; // object ID
};

Sphere spheres[1] = Sphere[](
    Sphere(vec3(0.0,1.0,0.0),10.0)
);

// camera position
float an = mousePos.x;
vec3 cameraPos = vec3(30.*cos(an), 0.0, 30.*sin(an));

// intersection test with one sphere
ISObj intersectSphere(in Sphere s,in Ray r,in int id)
{
	float a=dot(r.rd,r.rd);
	float b=dot(2.0*r.ro,r.rd)-dot(2.0*r.rd,s.c);
	float c=dot(r.ro,r.ro)-dot(2.0*r.ro, s.c)+dot(s.c,s.c)-pow(s.r,2.0);
    float d=sqrt(pow(b,2.0)-4.0*a*c);
    float t=min((-b-d)/(2.0*a),(-b+d)/(2.0*a));
    if(t > DIST_MIN && t <= DIST_MAX){
        return ISObj(t,1,id);
    }
    return ISObj(DIST_MAX,-1,-1);
}

Ray generatePerspectiveRay(in vec2 p)
{
    // p is the current pixel coord, in [-1,1]
    vec3 ta = vec3( 0.0, 1.0, 0.0 );
    // camera matrix
    vec3 ww = normalize( ta - cameraPos );
    vec3 uu = normalize( cross(ww,vec3(0.0,1.0,0.0) ) );
    vec3 vv = normalize( cross(uu,ww));
    // create view ray
    vec3 rd = normalize( p.x*uu + p.y*vv*aspectRatio + 1.5*ww );
    return Ray(cameraPos,rd);
}

vec3 getHitPoint(ISObj hit, Ray r){
    return r.ro +hit.d*r.rd;
}

// -------------------------------------------------
// -----------End Sphere Render Part----------------
// -------------------------------------------------

// source : https://www.shadertoy.com/view/Xsl3Dl
// Random function is taken with arbitrary values who can be modified here
vec3 hash( vec3 p )
{
	p = vec3( dot(p,vec3(127.1,311.7, 74.7)),
			  dot(p,vec3(269.5,183.3,246.1)),
			  dot(p,vec3(113.5,271.9,124.6)));

	return -1.0 + 2.0*fract(sin(p)*43758.5453123);
}

// source : https://www.shadertoy.com/view/Xsl3Dl
float gradient( in vec3 p )
{
    vec3 i = floor( p );
    vec3 f = fract( p );

	vec3 u = f*f*(3.0-2.0*f);

    return mix( mix( mix( dot( hash( i + vec3(0.0,0.0,0.0) ), f - vec3(0.0,0.0,0.0) ),
                          dot( hash( i + vec3(1.0,0.0,0.0) ), f - vec3(1.0,0.0,0.0) ), u.x),
                     mix( dot( hash( i + vec3(0.0,1.0,0.0) ), f - vec3(0.0,1.0,0.0) ),
                          dot( hash( i + vec3(1.0,1.0,0.0) ), f - vec3(1.0,1.0,0.0) ), u.x), u.y),
                mix( mix( dot( hash( i + vec3(0.0,0.0,1.0) ), f - vec3(0.0,0.0,1.0) ),
                          dot( hash( i + vec3(1.0,0.0,1.0) ), f - vec3(1.0,0.0,1.0) ), u.x),
                     mix( dot( hash( i + vec3(0.0,1.0,1.0) ), f - vec3(0.0,1.0,1.0) ),
                          dot( hash( i + vec3(1.0,1.0,1.0) ), f - vec3(1.0,1.0,1.0) ), u.x), u.y), u.z );
}

float fbm(vec3 x, int num_octave) {
	float v = 0.0;
	float a = 0.5;
	vec3 shift = vec3(100);
	for (int i = 0; i < num_octave; ++i) {
		v += a * gradient(x);
		x = x * 2.0 + shift;
		a *= 0.5;
	}
	return v;
}


vec3 compute_color(vec3 coord){
    if(NUM_OCTAVES > 1)
        return vec3(fbm(coord, NUM_OCTAVES))*.5+.5;
    else
        return vec3(gradient(coord))*.5+.5;
}

void main()
{
    // vec2 coord = vec2(fragCoord.x,fragCoord.y*aspectRatio);
    // coord *= 10.0;
    // outColor = vec4(compute_color(coord),1.0);
	Ray ray = generatePerspectiveRay(fragCoord);
	ISObj intersect = intersectSphere(spheres[0], ray, 0);
	if(intersect.t == -1){
		outColor = vec4(vec3(0.0), 1);
	}else{
		outColor = vec4(compute_color(getHitPoint(intersect, ray)),1);
	}

}
