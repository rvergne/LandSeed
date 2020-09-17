// --------------DEV-----------------
// @TAG VALLEY
// @FUNCTION_NAME valley
// @SIGNATURE (float terrainHeight, float valleyHeight, float delta) -> float
// -------------USER-----------------
// @NAME Valley
// @SHORT Flatten the terrain with smooth transition on the bottom
// @SPEC {
// Compute the new terrain height according to parameters, to smoothly make it flat at valleyHeight if terrainHeight is below valleyHeight.
// terrainHeight : terrain height to filter.
// valleyHeight : wanted height of the valley
// delta : the modification of terrainHeight will happen form valleyHeight + delta and do a smooth transition between [valleyHeight, valleyHeight + delta]
// }
// -------------END------------------

// @VALLEY
float valley(float terrainHeight,float valleyHeight, float delta){
  if(terrainHeight <= valleyHeight + delta){
    float t = smoothstep(valleyHeight + delta, valleyHeight, terrainHeight);
    return mix(terrainHeight, valleyHeight, t);
  }else{
    return terrainHeight;
  }
}
// @END
