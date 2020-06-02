// Below, a version to compute for the first nearest point (array-free version)
float cellular(vec2 position, float numOfDiv){

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
    return dist_alteration(min_dist);
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
float cellular(vec2 position, float numOfDiv, int f){
    if(f == 0)
      return cellular(position, numOfDiv);
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
    return dist_alteration(distances[f]);
}
