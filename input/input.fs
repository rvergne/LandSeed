// Define quality on a [0.0,100.0] range
// @QUALITY 50.6
// Define the wrapper (use the wrapper file name)
// @WRAPPER classic_shader
// terrainMap compute the height value for the terrain on pos
float terrainMap(vec2 pos){
  float terrain = 0;
  // @FEATURES only feature used after this tag and before end tag will be detected
  terrain += fbm_gradient(pos, 600, .001, 0.25, 1);
  terrain = plateau(terrain, 200, 25);
  // terrain += fbm_gradient(pos, 400, .002, .4, 5);
  // terrain += fbm_voronoi(pos, 200, .004, .25, 2);
  // @END
  return terrain;
}
