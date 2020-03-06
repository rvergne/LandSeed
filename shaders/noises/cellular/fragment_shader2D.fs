#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

const bool MOTION = true; // Do you want the noise to be in motion or fixed?
const float DIVISION = 10.0;  // How many cells in the grid spliting the screen do you want
const int F = 0; // Distance to what point should we compute (0: closest, 1: 2nd closest...), value should be in [0,8]

// Motion used can be modified here
vec2 motion(vec2 st){
    if(MOTION)
        return 0.5+0.5*sin(time + 7.387*st);
    else
        return st;
}

// Distance function can be modified here
// To see different distance function, check Utis/2DDistanceFunctions.fs
float my_distance(vec2 p1, vec2 p2){
    return distance(p1,p2);
}

// If you want to apply a change on the min_dist at the end of cellular computation
float dist_alteration(float original){
    return original;
    // return 1-original;
}

// Random function is taken with arbitrary values who can be modified here
vec2 rand2(vec2 st){
    return motion(vec2(fract(sin(dot(st.xy,vec2(12.9898,78.233)))*43758.5453123),fract(sin(dot(st.xy,vec2(12.9898,78.233)))*43897.5453123)));
}

// --------------------------
// ------|---UTILS---|-------
// ------v-----------v-------
// order an array from smallest to biggest
void ordering(inout float[9] tab){
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
vec3 cellular(vec2 position, float numOfDiv, int f){
    float distances[9];
    int indice = 0;

    vec2 cellPosition = floor(position*numOfDiv);
    vec2 positionInCell = fract(position*numOfDiv);

    for(int i =-1; i<=1;i++){
        for(int j=-1;j<=1;j++){
            vec2 curr_cellPos = cellPosition + vec2(i,j);
            vec2 curr_pointPosition = rand2(curr_cellPos)+vec2(i,j);
            distances[indice] = my_distance(positionInCell, curr_pointPosition);
            indice++;
        }
    }
    ordering(distances);
    return vec3(dist_alteration(distances[f]));
}

// Below, a version to compute for the first nearest point (array-free version)
vec3 cellular(vec2 position, float numOfDiv){

    vec2 cellPosition = floor(position*numOfDiv);
    vec2 positionInCell = fract(position*numOfDiv);
    vec2 pointPosition = rand2(cellPosition);

    float min_dist = my_distance(positionInCell, pointPosition);

    for(int i = -1; i <= 1; i++)
    {
        for(int j = -1; j <= 1; j++)
        {
            if(vec2(i,j) != vec2(0.0)){
                vec2 curr_cellPos = cellPosition + vec2(i,j);
                vec2 curr_pointPosition = rand2(curr_cellPos)+vec2(i,j);
                float curr_dist = my_distance(positionInCell, curr_pointPosition);
                if(curr_dist < min_dist)
                    min_dist = curr_dist;
            }
        }
    }
    return vec3(dist_alteration(min_dist));
}

void main()
{
    vec2 coord = vec2(fragCoord.x,fragCoord.y*aspectRatio);
    // you can also compute things like cellular(coord, DIVISION, 1)-cellular(coord, DIVISION, 0)
    outColor = vec4(cellular(coord, DIVISION, 0),1.0);
}
