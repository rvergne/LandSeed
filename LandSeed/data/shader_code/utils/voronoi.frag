// --------------DEV-----------------
// @TAG VORONOI
// @FUNCTION_NAME voronoi
// @SIGNATURE (vec2 st) -> float
// -------------USER-----------------
// @NAME Voronoi noise
// @SHORT Compute voronoi noise
// @SPEC {
// Compute the voronoi noise with a given vec2 seed.
// st : vec2 used as seed for the noise. Usually correspond to the terrain position
// }
// -------------END------------------

// @VORONOI
// @INCLUDE RAND2
float voronoi(in vec2 x) {

  vec2 p = floor(x);
  vec2 f = fract(x);
  vec2 res = vec2( 100.0 );

  for( int j=-1; j<=1; j++ )
    for( int i=-1; i<=1; i++ ) {

      vec2 b = vec2( float(i), float(j) );
      vec2 r = vec2( b ) - f + rand2( p + b );
      float d = dot( r, r );

      if( d < res.x ) {
        res = vec2( d, res.x );
      } else if( d < res.y ) {
        res.y = d;
      }
    }

  return sqrt(res.x);

}
// @END
