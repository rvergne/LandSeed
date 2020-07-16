# Plateau

**Tag**: PLATEAU

**Category**: feature

**Function Name**: plateau

**Signature**: (float terrainHeight, float plateauHeight, float delta) -> float

**Spec**: Compute the new terrain height according to parameters, to smoothly make it flat at plateauHeight if terrainHeight is above plateauHeight.

- terrainHeight : terrain height to filter.

- plateauHeight : wanted height of the plateau

- delta : the modification of terrainHeight will happen form plateauHeight - delta and do a smooth transition between [plateauHeight - delta, plateauHeight]



**Path**: src/shader_code/features/plateau.frag

