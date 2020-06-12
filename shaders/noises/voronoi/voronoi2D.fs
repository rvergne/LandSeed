
// @NOISE_VORONOI_2D
// @INCLUDE RANDOM_2D_01
float voronoi(in vec2 x) {

  vec2 p = floor(x);
  vec2 f = fract(x);
  float id = 0.0;
  vec2 res = vec2( 100.0 );

  for( int j=-1; j<=1; j++ )
    for( int i=-1; i<=1; i++ ) {

      vec2 b = vec2( float(i), float(j) );
      vec2 r = vec2( b ) - f + rand2_01( p + b );
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
// @END
