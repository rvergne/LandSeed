// randcount allows you to change rand seed (for instance when generating gradient twice at same place, it is useful to change output value)
// (just increment it)
// terrainMap compute the height value for the terrain on pos
float terrainMap(vec2 pos){
  float terrain = 0;
  randcount = 0;
  // --------------------------------------
  terrain += base_relief(pos, AMP/3, FREQ*1.5, PERS, NUM_OCTAVES);
  terrain += mountains(pos, AMP*1.3, FREQ/2.5);
  // --------------------------------------
  return (WATER && terrain<=WATER_HEIGHT)?WATER_HEIGHT:terrain;
}
