#version 330 core

layout(location = 0) in vec3 position;

out vec2 fragCoord;

void main() {
  gl_Position = vec4(position, 1);
  fragCoord = position.xy;
}
