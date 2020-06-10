#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

int NUM_OCTAVES = 6;

// Random function is taken with arbitrary values who can be modified here
// source : https://thebookofshaders.com/edit.php#11/2d-gnoise.frag
vec2 rand2(vec2 st){
    st = vec2( dot(st,vec2(127.1,311.7)),
              dot(st,vec2(269.5,183.3)) );
    return fract(sin(st)*43758.5453123);
}

float wnoise(in vec2 x) {

  vec2 p = floor(x);
  vec2 f = fract(x);
  float id = 0.0;
  vec2 res = vec2( 100.0 );

  for( int j=-1; j<=1; j++ )
    for( int i=-1; i<=1; i++ ) {

      vec2 b = vec2( float(i), float(j) );
      vec2 r = vec2( b ) - f + rand2( p + b );
      float d = dot( r, r );

      if( d < res.x ) {
        id = dot( p+b, vec2(1.0,57.0 ) );
        res = vec2( d, res.x );
      } else if( d < res.y ) {
        res.y = d;
      }
    }

  return sqrt(res.x);

}

float fbm(in vec2 p,in float amplitude,in float frequency,in float persistence, in int nboctaves) {
        float a = amplitude;
        vec2 x = p*vec2(frequency,frequency);
        float h = 0.;
        mat2 m = mat2(1.,0.,0.,1.);
        const mat2 m2 = mat2(  0.80,  0.60, -0.60,  0.80 );

        for(int i=0;i<nboctaves;++i) {
								// @FBM_NOISE
                float n = wnoise(x); // get noise + derivative at x

                h = h+a*n; // accum noise with a given amplitude

                a = a*persistence; // update amplitude for next octave
                x = 2.5*m2*x; // scale point to the next octave and apply a rotation (avoid grid patterns?)
        }

        return h;
}

vec3 compute_color(vec2 coord){
    return vec3(fbm(coord, 1.0, 0.3,0.5, 4));
}

void main()
{
    vec2 coord = vec2(fragCoord.x,fragCoord.y*aspectRatio);
    coord *= 10.0;
    outColor = vec4(compute_color(coord),1.0);
}
