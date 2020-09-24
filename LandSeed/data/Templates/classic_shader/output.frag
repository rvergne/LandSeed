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

// Ray march parameters
#define MOVEMENT false
#define DIST_MIN 0.1 // minimum distance to objects
#define DIST_MAX @RENDER_DISTANCE // maximum distance to render objects
#define RAY_MARCH_PRECI @RAYMARCH_STEP_SIZE // Ray march step (smaller = slower but more more accurate)

#define AMP 400.0

int randcount =0;

// @TERRAIN_MAP

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

    delt = deltfac+t/AMP;
    lasth = h;
    lasty = curr_pos.y;

  }

  return -1.;

}

Ray generateRay(vec2 p){

  const float DP = AMP;
  const vec3 moveFact = MOVEMENT?vec3(-100.0,0.0,0.0):vec3(0.0); // moveFact.y should be 0

  // p is the current pixel coord, in [-1,1]

  // normalized mouse position
  vec2 m = mousePos;

  // camera position
  float d = DP/2.;
  vec3 ro = vec3(d*cos(6.0*m.x),(DP/2.0)*(m.y*4.)+300,d*sin(6.0*m.x) )+moveFact*time;

  // target point
  vec3 ta = vec3(0.0,(DP/20.)+(AMP/3)+100,0.0)+moveFact*time;
  // vec3 ta = vec3(0.0,200,0.0)+moveFact*time;

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

vec3 applyFog ( vec3 color, float far) {
	//just to hide clipping
    return vec3( mix( color ,vec3(.8,.8,.8), smoothstep(0.0,1.0,far/(DIST_MAX+1000)) ) );
}


vec3 terrainNormal(in vec3 p, vec3 ro) {
  vec2 e = vec2(1e-2,0.0);
  return normalize( vec3( terrainMap(p.xz-e.xy) - terrainMap(p.xz+e.xy),
                          2.0*e.x,
                          terrainMap(p.xz-e.yx) - terrainMap(p.xz+e.yx) ) );
}

// Change the color computation function here
vec3 computeColor(in vec3 p, vec3 ro){
  // return vec3((p.y+AMP)/(2*AMP));
  return applyFog(terrainNormal(p, ro), distance(p, ro));
  // return p;
}

void main()
{
    vec2 coord = vec2(fragCoord.x, fragCoord.y*aspectRatio);
    Ray r = generateRay(coord);
    float res = rayMarchTerrain(r);
    vec3 rendu = vec3(0.0);

    if( res != -1){
      vec3 intersectionPoint = (r.ro + res*r.rd);
      rendu = computeColor(intersectionPoint, r.ro);
      outColor = vec4(rendu,1.0);
    }else{
      outColor = vec4(0.80);
    }
}
