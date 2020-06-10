#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

#define EPS 1e-5
#define DIST_MIN 1e-5 // minimum distance to objects
#define DIST_MAX 1e+5 // maximum distance to objects
const int NUM_OCTAVES = 3; // Num of octaves you want to compute (0 or 1 correspond to 1 and so, no fbm computation)

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

vec3 hash33(vec3 p) {
  vec3 q = vec3(  dot(p,vec3(127.1,311.7,74.7)),
                  dot(p,vec3(269.5,183.3,246.1)),
                  dot(p,vec3(113.5,271.9,124.6)));
  return fract(sin(q)*43758.5453123);
}

float wnoise(in vec3 x) {

  vec3 p = floor(x);
  vec3 f = fract(x);
  float id = 0.0;
  vec2 res = vec2( 100.0 );

  for( int k=-1; k<=1; k++ )
    for( int j=-1; j<=1; j++ )
      for( int i=-1; i<=1; i++ ) {

        vec3 b = vec3( float(i), float(j), float(k) );
        vec3 r = vec3( b ) - f + hash33( p + b );
        float d = dot( r, r );

        if( d < res.x ) {
          id = dot( p+b, vec3(1.0,57.0,113.0 ) );
          res = vec2( d, res.x );
        } else if( d < res.y ) {
          res.y = d;
        }
      }

  return sqrt(res.x);

}

float fnoise(in vec3 p,in float amplitude,in float frequency,in float persistence, in int nboctaves) {

  float a = amplitude;
  float f = frequency;
  float n = 0.0;

  for(int i=0;i<nboctaves;++i) {
    n = n+a*wnoise(p*f);
    f = f*2.;
    a = a*persistence;
  }
  return n;
}

// This is optionnal
// you can also compute things like cellular(coord, DIVISION, 1)-cellular(coord, DIVISION, 0)
vec3 compute_color(vec3 coord){
  return vec3(fnoise(coord, 1.0,0.2,0.25,1)); 
}

void main()
{
    Ray ray = generatePerspectiveRay(fragCoord);
    ISObj intersect = intersectSphere(spheres[0], ray, 0);
    if(intersect.t == -1){
        outColor = vec4(vec3(0.0), 1);
    }else{
        outColor = vec4(compute_color(getHitPoint(intersect, ray)),1);
    }
}
