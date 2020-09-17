// --------------DEV-----------------
// @TAG RAND3
// @FUNCTION_NAME rand3
// @SIGNATURE (vec3 st) -> vec3
// -------------USER-----------------
// @NAME Hash 3D
// @SHORT A 3D hash function
// @SPEC {
// compute a "random" vec3. Values will be in [0,1]
// st : vec3 used as seed. Usually correspond to the terrain position
// }
// -------------END------------------
// @RAND3
// Random function (vec3) -> [0,1]
vec3 rand3(vec3 st){
  return vec3(fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43758.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43897.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*45758.5453123));
}
// @END
