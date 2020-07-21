// --------------DEV-----------------
// @TAG GRADIENT
// @FUNCTION_NAME gradient
// @SIGNATURE (vec2 st) -> float
// -------------USER-----------------
// @NAME Gradient noise
// @SHORT Compute gradient noise
// @SPEC {
// Compute the gradient noise with a given vec2 seed.
// st : vec2 used as seed for the noise. Usually correspond to the terrain position
// }
// -------------END------------------

// @GRADIENT
// @INCLUDE RAND2
float gradient(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    vec2 u = f*f*(3.0-2.0*f);

    return mix( mix( dot( -1.0+2.0*rand2(i + vec2(0.0,0.0) ), f - vec2(0.0,0.0) ),
                     dot( -1.0+2.0*rand2(i + vec2(1.0,0.0) ), f - vec2(1.0,0.0) ), u.x),
                mix( dot( -1.0+2.0*rand2(i + vec2(0.0,1.0) ), f - vec2(0.0,1.0) ),
                     dot( -1.0+2.0*rand2(i + vec2(1.0,1.0) ), f - vec2(1.0,1.0) ), u.x), u.y);
}
// @END
