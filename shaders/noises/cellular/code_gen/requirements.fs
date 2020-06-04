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
