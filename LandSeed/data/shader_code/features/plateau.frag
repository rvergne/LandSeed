// --------------DEV-----------------
// @TAG PLATEAU
// @FUNCTION_NAME plateau
// @SIGNATURE (float terrainHeight, float plateauHeight, float delta) -> float
// -------------USER-----------------
// @NAME Plateau
// @SHORT Flatten the terrain with smooth transition
// @SPEC {
// Compute the new terrain height according to parameters, to smoothly make it flat at plateauHeight if terrainHeight is above plateauHeight.
// terrainHeight : terrain height to filter.
// plateauHeight : wanted height of the plateau
// delta : the modification of terrainHeight will happen form plateauHeight - delta and do a smooth transition between [plateauHeight - delta, plateauHeight]
// }
// -------------END------------------

// @PLATEAU
float plateau(float terrainHeight,float plateauHeight, float delta){
  if(terrainHeight >= plateauHeight - delta){
    float t = smoothstep(plateauHeight - delta, plateauHeight, terrainHeight);
    return mix(terrainHeight, plateauHeight, t);
  }else{
    return terrainHeight;
  }
}
// @END
