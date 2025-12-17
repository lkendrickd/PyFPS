#version 330 core

out vec4 frag_color;

in vec2 uv;

uniform sampler2D u_menu_texture;

void main() {
    frag_color = texture(u_menu_texture, uv);
}
