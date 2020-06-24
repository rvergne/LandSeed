#plateau

**Category**: feature

**Tag**: PLATEAU

**Function Name**: plateau

**Signature**: (float, float, float) -> float

**Name**: plateau

**Spec**: Compute the new terrain height according to parameters, to smoothly make it flat at plateauHeight if terrainHeight is above plateauHeight.

- terrainHeight : terrain height to filter.

- plateauHeight : wanted height of the plateau

- delta : the modification of terrainHeight will happen form plateauHeight - delta and do a smooth transition between [plateauHeight - delta, plateauHeight]



