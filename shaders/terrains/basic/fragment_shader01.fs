#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

// Ray struct
struct Ray{
    vec3 ro;    // ray origin
    vec3 rd;    // ray direction
};

/////////////////////////////////////////////
///////////////////PARAM/////////////////////
/////////////////////////////////////////////
// RayMarch param
#define MOVEMENT false
#define DIST_MIN 0.1 // minimum distance to objects
#define DIST_MAX 1000.0 // maximum distance to render objects
#define RAY_MARCH_PRECI 2. // Ray march step (bigger = slower but more more accurate)
#define NUM_OCTAVES 5

// FBM param
#define AMP 200.0 // Amplitude
#define AMPVAR 0.170 // Amplitude variation : useless for now
#define FREQ 0.004 // Frequence
#define PERS 0.350 // Persistence

/////////////////////////////////////////////
///////////////////NOISE/////////////////////
/////////////////////////////////////////////
// Random function is taken with arbitrary values who can be modified here
// source : https://thebookofshaders.com/edit.php#11/2d-gnoise.frag
vec2 rand2(vec2 st){
    st = vec2( dot(st,vec2(129.1,311.7)),
              dot(st,vec2(269.5,183.3)) );
    return -1.0 + 2.0*fract(sin(st)*44758.5453123);
}

// noise gradient
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

float terrainMap(vec2 pos){
  return fbm(pos, AMP, FREQ, PERS, NUM_OCTAVES);
}

vec3 terrainNormal(in vec2 p) {
    vec2 e = vec2(1e-2,0.0);
    return normalize( vec3(terrainMap(p-e.xy) - terrainMap(p+e.xy),
                       2.0*e.x,
                       terrainMap(p-e.yx) - terrainMap(p+e.yx) ) );
}

float rayMarchTerrain(Ray r){
  const float deltfac = RAY_MARCH_PRECI;
  const float mint = DIST_MIN;
  const float maxt = DIST_MAX;
  float delt = deltfac;

  float lasth = 0.0;
  float lasty = 0.0;

  for(float t=mint; t<maxt; t+=delt){
    vec3 curr_pos = r.ro + r.rd*t;

    float h = terrainMap(curr_pos.xz);

    if(curr_pos.y<h)
      return t - delt + delt*(lasth-lasty)/(curr_pos.y-lasty-h+lasth);

    delt = deltfac+t/200.0;
    lasth = h;
    lasty = curr_pos.y;

  }

  return -1;

}

Ray generateRay(vec2 p){

  const float DP = AMP;
  const vec3 moveFact = MOVEMENT?vec3(10.0,0.0,0.0):vec3(0.0); // moveFact.y should be 0

  // p is the current pixel coord, in [-1,1]

  // normalized mouse position
  vec2 m = mousePos;

  // camera position
  float d = DP/2.;
  vec3 ro = vec3(d*cos(6.0*m.x),(DP/2.0)*(m.y*4.)+AMP/3,d*sin(6.0*m.x) )+moveFact*time;

  // target point
  vec3 ta = vec3(0.0,DP/20.+AMP/3,0.0)+moveFact*time;

  // camera view vector
  vec3 cw = normalize(ta-ro);

  // camera up vector
  vec3 cp = vec3(0.0,1.0,0.0);

  // camera right vector
  vec3 cu = normalize(cross(cw,cp));

  // camera (normalized) up vector
  vec3 cv = normalize(cross(cu,cw));

  // view vector, including perspective (the more you multiply cw, the less fovy)
  vec3 rd = normalize(p.x*cu + p.y*cv + 1.5*cw);

  return Ray(ro,rd);
}

void main()
{
    vec2 coord = vec2(fragCoord.x, fragCoord.y*aspectRatio);

    Ray r = generateRay(coord);
    float res = rayMarchTerrain(r);

    if( res != -1 ){
      vec3 rendu = terrainNormal((r.ro + res*r.rd).xz);
      outColor = vec4(rendu,1.0);
    }else{
      outColor = vec4(0.0);
    }
}
