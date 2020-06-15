// TODO add offset version

// @RANDOM_2D_01
// Random function (vec2) -> [0,1]
vec2 rand2_01(vec2 st){
    st = vec2( dot(st,vec2(127.1,311.7)),
              dot(st,vec2(269.5,183.3)) );
    return fract(sin(st)*43758.5453123);
}
// @END
// @RANDOM_2D_-11
// Random function (vec2) -> [-1,1]
vec2 rand2(vec2 st){
    st = vec2( dot(st,vec2(127.1,311.7)),
              dot(st,vec2(269.5,183.3)) );
    return -1.0+2.0*fract(sin(st)*43758.5453123);
}
// @END
// @RANDOM_3D_01
// Random function (vec3) -> [0,1]
vec3 rand3_01(vec3 st){
  return vec3(fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43758.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43897.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*45758.5453123));
}
// @END
// @RANDOM_3D_-11
// Random function (vec3) -> [-1,1]
vec3 rand3(vec3 st){
  return vec3(-1.0)+2.0*vec3(fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43758.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*43897.5453123),
              fract(sin(dot(st.xyz,vec3(65.48943,12.9898,78.233)))*45758.5453123));
}
// @END
