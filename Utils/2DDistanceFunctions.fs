// 2D distances functions
float my_distance(vec2 p1, vec2 p2){
    // return distance(p1,p2); // classic length
    // return (p2.x-p1.x)*(p2.x-p1.x) + (p2.y-p1.y)*(p2.y-p1.y); // length2 without squared root
    // return abs(p1.x-p2.x)+abs(p1.y-p2.y); // Manhattan distance
    // return max(abs(p1.x-p2.x),abs(p1.y-p2.y)); // chebyshev distance
    // return (p2.x-p1.x)*(p2.x-p1.x) + (p2.x-p1.x)*(p2.y-p1.y) + (p2.y-p1.y)*(p2.y-p1.y); Quadratic distance
    // return minkowskiDistance(p1, p2, 4);
}

float minkowskiDistance(vec2 p1, vec2 p2, int dim){
    return pow( pow( abs(p2.x-p1.x), dim) + pow( abs(p2.y-p1.y), dim), 1.0/dim);
}
