// Define quality on a [0.0,100.0] range, 0.0 being the faster and 100.0 being the more qualitati*ne the wrapper (use the template file name)
// @QUALITY 50.6
// Define the template (use the template file name)
// @TEMPLATE heightmap
// terrainMap compute the height value for the terrain on pos
float terrainMap(vec2 pos){
  float terrain = 0.0;
  // @FEATURES only feature used after this tag and before end tag will be detected
  terrain += fbm_gradient(pos, 600.0, .001, 0.25, 1);
  // terrain = plateau(terrain, 200.0, 25.0);
  terrain += fbm_gradient(pos, 400.0, .002, .4, 5);
  // terrain += fbm_voronoi(pos, 200.0, .004, .25, 2);
  terrain = phasor(pos, 200.0, 0.0, 0.001, 0.002, false);
  // @END
  return terrain;
}
