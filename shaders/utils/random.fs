// TODO add offset version

// --------------DEV-----------------
// @TAG RANDOM_2D
// @FUNCTION_NAME rand2
// @SIGNATURE (vec2 st) -> vec2
// -------------USER-----------------
// @NAME 2D hash function
// @SPEC {
// compute a "random" vec2. Values will be in [0,1]
// st : vec2 used as seed. Usually correspond to the terrain position
// }
// -------------END------------------

// @RANDOM_2D
// Random function (vec2) -> [0,1]
vec2 rand2(vec2 st){
    st = vec2( dot(st,vec2(127.1,311.7)),
              dot(st,vec2(269.5,183.3)) );
    return fract(sin(st)*43758.5453123);
}
// @END

// --------------DEV-----------------
// @TAG RANDOM_3D
// @FUNCTION_NAME rand3
// @SIGNATURE (vec3 st) -> vec3
// -------------USER-----------------
// @NAME 3D hash function
// @SPEC {
// compute a "random" vec3. Values will be in [0,1]
// st : vec3 used as seed. Usually correspond to the terrain position
// }
// -------------END------------------
// @RANDOM_3D
// Random function (vec3) -> [0,1]
vec3 rand3(vec3 st){
  return vec3(fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43758.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43897.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*45758.5453123));
}
// @END
