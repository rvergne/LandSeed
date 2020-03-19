// 3D distance function
float my_distance(vec3 p1, vec3 p2){
  // return distance(p1,p2); // classic distance function
  // return (p2.x-p1.x)*(p2.x-p1.x) + (p2.y-p1.y)*(p2.y-p1.y) + (p2.z-p1.z)*(p2.z-p1.z); // length2 without squared root
  // return abs(p1.x-p2.x)+abs(p1.y-p2.y)+abs(p1.z-p2.z); // Manhattan distance
  // return max(max(abs(p1.x-p2.x),abs(p1.y-p2.y)),abs(p1.z-p2.z)); // chebyshev distance
  // return (p2.x-p1.x)*(p2.x-p1.x) + (p2.y-p1.y)*(p2.y-p1.y) + (p2.z-p1.z)*(p2.z-p1.z) + (p2.x-p1.x)*(p2.y-p1.y) + (p2.x-p1.x)*(p2.z-p1.z) + (p2.y-p1.y)*(p2.z-p1.z); Quadratic distance
  // return minkowskiDistance(p1, p2, 4);
}

float minkowskiDistance(vec3 p1, vec3 p2, int dim){
    return pow( pow( abs(p2.x-p1.x), dim) + pow( abs(p2.y-p1.y), dim) + pow( abs(p2.z-p1.z), dim), 1.0/dim);
}
