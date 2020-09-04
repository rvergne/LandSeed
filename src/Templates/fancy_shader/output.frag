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

/*vec3 applyFog ( vec3 color, float far) {
	//just to hide clipping
    return vec3( mix( color ,vec3(.8,.8,.8), smoothstep(0.0,1.0,far/(DIST_MAX+1000)) ) );
}*/


vec3 terrainNormal(in vec3 p, vec3 ro) {
  vec2 e = vec2(1e-2,0.0);
  return normalize( vec3( terrainMap(p.xz-e.xy) - terrainMap(p.xz+e.xy),
                          2.0*e.x,
                          terrainMap(p.xz-e.yx) - terrainMap(p.xz+e.yx) ) );
}
//Maxime tests-----------------------------------------------

const float PI = 3.14159265359f;

vec3 applyFog( in vec3  color,      // original color of the pixel
               in float c_dist, // camera to point distance
               in vec3  V,
               in vec3 L,
               in vec3 ro,
               in float fog_fall)  // camera to point vector
{
    float fog_damp = fog_fall*0.085;
    float fogAmount = exp(-ro.y*0.4*fog_damp)*(1.0-exp( -c_dist*V.y*fog_damp))/V.y;
    vec3  fogColor  = vec3(0.5,0.6,0.7);

    float sun_amount = max(dot(V,-L),0.0f);
    fogColor  = mix(fogColor, vec3(1), pow(sun_amount,8.0));
    return mix( color, fogColor, clamp(fogAmount,0,1) );
}



float DistributionGGX(vec3 N, vec3 H, float roughness)
{
    float a      = roughness*roughness;
    float a2     = a*a;
    float NdotH  = max(dot(N, H), 0.0);
    float NdotH2 = NdotH*NdotH;

    float nom   = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;

    return nom / denom;
}

float GeometrySchlickGGX(float NdotV, float roughness)
{
    float r = (roughness + 1.0);
    float k = (r*r) / 8.0;

    float nom   = NdotV;
    float denom = NdotV * (1.0 - k) + k;

    return nom / denom;
}

float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness)
{
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    float ggx2  = GeometrySchlickGGX(NdotV, roughness);
    float ggx1  = GeometrySchlickGGX(NdotL, roughness);

    return ggx1 * ggx2;
}

vec3 fresnelSchlick(float cosTheta, vec3 F0)
{
    return F0 + (1.0 - F0)*pow((1.0 + 0.000001/*avoid negative approximation when cosTheta = 1*/) - cosTheta, 5.0);
}

vec3 PRim(vec3 N, vec3 Ve, vec3 rim_col, vec3 H, float intensity)
{
    vec3 F0 = vec3(0.04);
    F0 = mix(F0, rim_col, intensity);
    vec3 F = fresnelSchlick(max(dot(H, Ve), 0.0), F0);
    float rim = 1 -  abs(dot(Ve,N));
    return F  * rim / PI;
}

vec3 computeReflectance(vec3 N, vec3 Ve, vec3 F0, vec3 albedo, vec3 L, vec3 H, vec3 light_col, float intensity, float metallic, float roughness)
{
    vec3 radiance =  light_col * intensity; //Incoming Radiance

    // cook-torrance brdf
    float NDF = DistributionGGX(N, H, roughness);
    float G   = GeometrySmith(N, Ve, L,roughness);
    vec3 F    = fresnelSchlick(max(dot(H, Ve), 0.0), F0);

    vec3 kS = F;
    vec3 kD = vec3(1.0) - kS;
    kD *= 1.0 - metallic;

    vec3 nominator    = NDF * G * F;
    float denominator = 4 * max(dot(N, Ve), 0.0) * max(dot(N, L), 0.0) + 0.00001/* avoid divide by zero*/;
    vec3 specular     = nominator / denominator;


    // add to outgoing radiance Lo
    float NdotL = max(dot(N, L), 0.0);
    vec3 diffuse_radiance = kD * (albedo)/ PI;

    return (diffuse_radiance + specular) * radiance * NdotL;
}


float terrainGradientNorm(in vec3 p, vec3 ro)
{
    vec2 e = vec2(1e-4,0.0);
    return length( vec3( terrainMap(p.xz-e.xy) - terrainMap(p.xz+e.xy),
                            2.0*e.x,
                            terrainMap(p.xz-e.yx) - terrainMap(p.xz+e.yx) ) );
}

float AmbientOcclusion(vec3 point, vec3 normal, float step_dist, float step_nbr)
{
    float occlusion = (2*step_nbr+1)*(2*step_nbr+1);

    float eps = 0.001f;
    for(float f = -step_nbr*step_dist; f <= step_nbr*step_dist ; f +=step_dist)
         for(float g = -step_nbr*step_dist; g <= step_nbr*step_dist ; g +=step_dist)
         {
             float dist = terrainMap(point.xz + vec2(f,g)) - point.y;
             if(dist > eps)
                 occlusion--;
             else
                 occlusion++;
         }

    //occlusion /= (2*step_nbr+1)*(2*step_nbr+1);
    float mean = occlusion/(2*step_nbr+1)*(2*step_nbr+1);
    float std = 0.0;
    for(float f = -step_nbr*step_dist; f <= step_nbr*step_dist ; f +=step_dist)
         for(float g = -step_nbr*step_dist; g <= step_nbr*step_dist ; g +=step_dist)
             std += pow( (terrainMap(point.xz + vec2(f,g)) - point.y > eps ? -1 : 1) - mean,2);

    std /=  ((2*step_nbr+1)*(2*step_nbr+1)-1);
    occlusion = exp(-(mean*mean)/(2*std*std));


    return occlusion;
}
//------------------------------------------------------------------------------
// Change the color computation function here
vec3 computeColor(in vec3 p, vec3 ro){
  // return vec3((p.y+AMP)/(2*AMP));
  float gradient = terrainGradientNorm(p,ro);
 /* float ao = 0.0;
  float st_nb = 2;
  float step_dist = 1/(pow(gradient,2));
  for(float f = -st_nb*step_dist; f <= st_nb*step_dist ; f +=step_dist)
       for(float g = -st_nb*step_dist; g <= st_nb*step_dist ; g +=step_dist)
           ao += AmbientOcclusion(p+vec3(f,0,g),terrainNormal(p, ro),step_dist,1);
  ao /= (2*st_nb+1)*(2*st_nb+1);*/
  vec3 normal = terrainNormal(p, ro);
  vec3 light = normalize(vec3(1));
  vec3 view = normalize(ro-p);
  vec3 half = normalize(view+light);
  vec3 m_col = computeReflectance(normal,view,vec3(0.04),mix(mix(vec3(0.7,0.3,0.1),vec3(0.2,0.7,0.3),pow(max(dot(normal,vec3(0,1,0)),0),4)),vec3(0.6,0.5,0.5),abs(dot(normal,vec3(1,0,0)))),light,half,vec3(1),4,0,0.7);
  vec3 col = applyFog(m_col,distance(p, ro),view,light,ro,0.25);
  col += PRim(normal,view,vec3(0.1,0.8,0.8),half,1.0f);
  col = col/(col+vec3(1));
  col = pow(col,vec3(1.0/1));
  return col;
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
