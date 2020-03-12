#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

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

// Useless mais distance a camera
const float DP = 5.0;

Sphere spheres[1] = Sphere[](
    Sphere(vec3(0.0,1.0,0.0),10.0)
);

// field of view
const float fov = 45.0;
// camera position
float an = mousePos.x;
// vec3 cameraPos = vec3(0.0,0.0,DP);
vec3 cameraPos = vec3(30.*cos(an), 0.0, 30.*sin(an));
// vec3 cameraPos = vec3(0.0,0.0,1.0/tan(fov/2.0)+3.0);

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

// intersection test for all objects in the scene
ISObj intersectObjects(in Ray r)
{
    return intersectSphere(spheres[0], r, 0);
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
    // return Ray(cameraPos,normalize(vec3(p.x,aspectRatio*p.y,-cameraPos.z)));
    return Ray(cameraPos,rd);

}

vec3 computeNormal(in ISObj is,in Ray r)
{
	vec3 normal = vec3(0.0);
    vec3 intersectPoint = r.ro + is.d*r.rd;
    normal = vec3((intersectPoint.x - spheres[is.i].c.x)/spheres[is.i].r,(intersectPoint.y - spheres[is.i].c.y)/spheres[is.i].r,(intersectPoint.z - spheres[is.i].c.z)/spheres[is.i].r);
    return normal;
    // return (normal+(vec3(1.0))/vec3(2.0));
}

vec3 getHitPoint(ISObj hit, Ray r){
    return r.ro +hit.d*r.rd;
}

// -------------------------------------------------
// -----------End Sphere Render Part----------------
// -------------------------------------------------


const bool MOTION = true; // Do you want the noise to be in motion or fixed?
float DIVISION = .8;  // How many cells in the grid spliting the screen do you want
const int F = 0; // Distance to what point should we compute (0: closest, 1: 2nd closest...), value should be in [0,8]
const int NUM_OCTAVES = 3; // Num of octaves you want to compute (0 or 1 correspond to 1 and so, no fbm computation)

// Motion used can be modified here
vec3 motion(vec3 st){
    if(MOTION)
        return 0.5+0.5*sin(time + 7.387*st.xyz);
    else
        return st;
}

// Distance function can be modified here
// To see different distance function, check Utis/2DDistanceFunctions.fs
float my_distance(vec3 p1, vec3 p2){
    return distance(p1,p2);
}

// If you want to apply a change on the min_dist at the end of cellular computation
float dist_alteration(float original){
    return original;
    // return 1-original;
}

// Random function is taken with arbitrary values who can be modified here
vec3 rand3(vec3 st){
    return motion(vec3(fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43758.5453123),fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43897.5453123),fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*45758.5453123)));
}

// --------------------------
// ------|---UTILS---|-------
// ------v-----------v-------
// order an array from smallest to biggest
void ordering(inout float[27] tab){
    for(int i = 0; i < tab.length(); i++)
    {
        float curr = tab[i];
        int j = i;
        while (j>0 && tab[j-1]>curr)
        {
            tab[j] = tab[j-1];
            j--;
        }
        tab[j] = curr;
    }
}
// ------^-----------^-------
// ------|---UTILS---|-------
// --------------------------

// Cellular noise general function
// Compute some grey shades
// The idea is to split the screen in cells (number of cells defined by DIVISION),
// then we generate a point for each cells
// finally, for each fragment, we compute the minimum distance for the f closest point
// This minimum distance will define our grey shade value
// SPEC --------------------------------------
// position the screen point you want to compute (the current fragment for this example)
// numOfDiv is the number of subdivision of the screen you want
// f define the point we want (first nearest, second nearest...) so this value should be in the range [0,8]
// -------------------------------------------
float cellular(vec3 position, float numOfDiv, int f){
    float distances[27];
    int indice = 0;

    vec3 cellPosition = floor(position*numOfDiv);
    vec3 positionInCell = fract(position*numOfDiv);

    for(int i =-1; i<=1;i++){
        for(int j=-1;j<=1;j++){
            for(int k = -1; k <= 1; k++){
                vec3 curr_cellPos = cellPosition + vec3(i,j,k);
                vec3 curr_pointPosition = rand3(curr_cellPos)+vec3(i,j,k);
                distances[indice] = my_distance(positionInCell, curr_pointPosition);
                indice++;
            }
        }
    }
    ordering(distances);
    return dist_alteration(distances[f]);
}

// Below, a version to compute for the first nearest point (array-free version)
float cellular(vec3 position, float numOfDiv){

    vec3 cellPosition = floor(position*numOfDiv);
    vec3 positionInCell = fract(position*numOfDiv);
    vec3 pointPosition = rand3(cellPosition);

    float min_dist = my_distance(positionInCell, pointPosition);

    for(int i = -1; i <= 1; i++)
    {
        for(int j = -1; j <= 1; j++)
        {
            for(int k = -1; k <= 1; k++){
                if(vec3(i,j,k) != vec3(0.0)){
                    vec3 curr_cellPos = cellPosition + vec3(i,j,k);
                    vec3 curr_pointPosition = rand3(curr_cellPos)+vec3(i,j,k);
                    float curr_dist = my_distance(positionInCell, curr_pointPosition);
                    if(curr_dist < min_dist)
                        min_dist = curr_dist;
                }
            }
        }
    }
    return dist_alteration(min_dist);
}

// Computation of FBM, with NUM_OCTAVES octaves
float fbm(vec3 x, int num_octave) {
	float v = 0.0;
	float a = 0.5;
	vec3 shift = vec3(100);
	for (int i = 0; i < num_octave; ++i) {
		v += a * cellular(x, DIVISION, F);
		x = x * 2.0 + shift;
		a *= 0.5;
	}
	return v;
}

// This is optionnal
// you can also compute things like cellular(coord, DIVISION, 1)-cellular(coord, DIVISION, 0)
vec3 compute_color(vec3 coord){
    if(NUM_OCTAVES > 1){    // check to see if we need to use fbm function
        return vec3(fbm(coord, NUM_OCTAVES));
    }else{
        if(F == 0)  // If F = 0, we need to compute the closest point only, so we don't need to use the more expensive cellular function
            return vec3(cellular(coord, DIVISION));
        else
            return vec3(cellular(coord, DIVISION, F));
    }
}

void main()
{
    Ray ray = generatePerspectiveRay(fragCoord);
    ISObj intersect = intersectObjects(ray);
    if(intersect.t == -1){
        outColor = vec4(vec3(0.0), 1);
    }else{
        outColor = vec4(compute_color(getHitPoint(intersect, ray)),1);
    }
}
