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
