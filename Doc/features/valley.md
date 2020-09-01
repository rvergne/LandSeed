# Valley

**Tag**: VALLEY

**Category**: feature

**Function Name**: valley

**Signature**: (float terrainHeight, float valleyHeight, float delta) -> float

**Spec**: Compute the new terrain height according to parameters, to smoothly make it flat at valleyHeight if terrainHeight is below valleyHeight.

- terrainHeight : terrain height to filter.

- valleyHeight : wanted height of the valley

- delta : the modification of terrainHeight will happen form valleyHeight + delta and do a smooth transition between [valleyHeight, valleyHeight + delta]



**Path**: /src/shader_code/features/valley.frag

