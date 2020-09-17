#version 330 core

uniform vec2 mousePos;
uniform float time;
uniform float aspectRatio;

in vec2 fragCoord;

out vec4 outColor;

// TODO: Adjust to match the classic_shader range
#define XSCALE 5000.0
#define YSCALE 600.0
#define ZSCALE (XSCALE * aspectRatio)

// @TERRAIN_MAP

void main()
{
    float h = terrainMap(vec2(XSCALE, ZSCALE) * fragCoord);
    h /= YSCALE;
    outColor = vec4(vec3(h), 1.0);
}
