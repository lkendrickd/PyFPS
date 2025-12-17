import moderngl as mgl
import numpy as np


class Crosshair:
    """Simple green reticle rendered in NDC space."""

    def __init__(self, eng):
        self.ctx = eng.ctx
        self.color = (0.0, 1.0, 0.0, 0.9)

        length = 0.025
        thickness = 0.002

        verts = np.array([
            # vertical bar
            -thickness, -length,
             thickness, -length,
             thickness,  length,
            -thickness, -length,
             thickness,  length,
            -thickness,  length,
            # horizontal bar
            -length, -thickness,
             length, -thickness,
             length,  thickness,
            -length, -thickness,
             length,  thickness,
            -length,  thickness,
        ], dtype='f4')

        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_position;
            void main() {
                gl_Position = vec4(in_position, 0.0, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            uniform vec4 u_color;
            out vec4 frag_color;
            void main() {
                frag_color = u_color;
            }
            """,
        )

        vbo = self.ctx.buffer(verts.tobytes())
        self.vao = self.ctx.vertex_array(self.prog, [(vbo, '2f', 'in_position')])

    def render(self):
        self.prog['u_color'].value = self.color  # type: ignore
        self.ctx.disable(mgl.DEPTH_TEST)  # type: ignore
        self.vao.render(mode=mgl.TRIANGLES)
        self.ctx.enable(mgl.DEPTH_TEST)  # type: ignore
