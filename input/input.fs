// TODO : add quality parametrization HERE
// TODO bring back randcount

// terrainMap compute the height value for the terrain on pos
float terrainMap(vec2 pos){
  float terrain = 0;
  // ------------FEATURES-----------------
  terrain += fbm_gradient(pos, 600, .001, 0.25, 1);
  terrain += fbm_gradient(pos, 400, .002, .4, 5);
  terrain += fbm_voronoi(pos, 200, .004, .25, 2);
  // ------------END FEATURES-------------
  return terrain;
}
