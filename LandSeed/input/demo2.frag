// Define the template (use the template tag) and it's parameters (if there is no parameters, default value will be taken)
// @TEMPLATE fancy_shader RAYMARCH_STEP_SIZE=2.0 RENDER_DISTANCE=5000.0
// terrainMap compute the height value for the terrain on pos
float terrainMap(vec2 pos){
  float terrain = 0.0;
  // @FEATURES only feature used after this tag and before end tag will be detected
  terrain += fbm_gradient(pos, 600.0, .001, 0.25, 1);
  // terrain += fbm_gradient(pos, 100.0, .002, .4, 8);
  terrain += fbm_voronoi(pos, 200.0, .004, .25, 10);
  // terrain = plateau(terrain, 200.0, 25.0);
  // terrain = valley(terrain, -100.0, 50.0);
  // terrain += fbm_gradient(pos, 100.0, .002, .4, 10);
  // terrain += phasor(pos, 200.0, 0.0, 0.001, 0.002, false);
  // @END
  return terrain;
}
