import pygame as pg
import moderngl as mgl
import numpy as np
from typing import Tuple


class MenuRenderer:
    """Handles rendering of menu UI elements."""
    
    def __init__(self, ctx: mgl.Context, screen_size: Tuple[int, int]):
        self.ctx = ctx
        self.screen_size = screen_size
        
        # Initialize fonts
        pg.font.init()
        self.title_font = pg.font.Font(None, 72)
        self.menu_font = pg.font.Font(None, 48)
        self.small_font = pg.font.Font(None, 32)
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.text_color = (220, 220, 220)
        self.text_hover_color = (255, 255, 100)
        self.text_disabled_color = (100, 100, 100)
        self.button_color = (40, 40, 60)
        self.button_hover_color = (60, 60, 90)
        
        # Create a menu texture
        self.menu_texture = None
        
        # Create shader program for menu rendering
        self._create_shader_program()
        self._create_quad()
    
    def _create_shader_program(self):
        """Create shader program for rendering menu."""
        with open('shaders/menu.vert', 'r') as f:
            vertex_shader = f.read()
        with open('shaders/menu.frag', 'r') as f:
            fragment_shader = f.read()
        
        self.program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
    
    def _create_quad(self):
        """Create a fullscreen quad for menu rendering."""
        # Vertices: position (x, y), texcoord (u, v)
        vertices = np.array([
            # pos        # texcoord
            -1.0, -1.0,  0.0, 0.0,  # bottom-left
             1.0, -1.0,  1.0, 0.0,  # bottom-right
             1.0,  1.0,  1.0, 1.0,  # top-right
            -1.0,  1.0,  0.0, 1.0,  # top-left
        ], dtype='f4')
        
        indices = np.array([0, 1, 2, 0, 2, 3], dtype='i4')
        
        vbo = self.ctx.buffer(vertices)
        ibo = self.ctx.buffer(indices)
        
        self.vao = self.ctx.vertex_array(
            self.program,
            [(vbo, '2f 2f', 'in_position', 'in_texcoord')],
            ibo
        )
    
    def render_to_screen(self, surface: pg.Surface):
        """Render the menu surface to the OpenGL screen."""
        # Convert surface to texture
        texture = self.surface_to_texture(surface)
        
        # Bind texture
        texture.use(location=0)
        self.program['u_menu_texture'] = 0
        
        # Disable depth test for 2D menu
        self.ctx.disable(mgl.DEPTH_TEST)  # type: ignore
        
        # Render fullscreen quad
        self.vao.render()
        
        # Re-enable depth test
        self.ctx.enable(mgl.DEPTH_TEST)  # type: ignore
    
    def render_text(self, surface: pg.Surface, text: str, pos: Tuple[int, int], 
                   font: pg.font.Font | None = None, color: Tuple[int, int, int] | None = None,
                   center=False) -> pg.Rect:
        """
        Render text to a surface.
        
        Args:
            surface: Surface to render to
            text: Text to render
            pos: Position (x, y)
            font: Font to use (default: menu_font)
            color: Text color (default: text_color)
            center: If True, center text at pos
            
        Returns:
            Rect of rendered text
        """
        if font is None:
            font = self.menu_font
        if color is None:
            color = self.text_color
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = pos
        else:
            text_rect.topleft = pos
        
        surface.blit(text_surface, text_rect)
        return text_rect
    
    def render_button(self, surface: pg.Surface, text: str, rect: pg.Rect,
                     hovered=False, enabled=True) -> pg.Rect:
        """
        Render a button.
        
        Args:
            surface: Surface to render to
            text: Button text
            rect: Button rectangle
            hovered: Is the button hovered
            enabled: Is the button enabled
            
        Returns:
            Rect of button
        """
        # Choose colors based on state
        if not enabled:
            text_color = self.text_disabled_color
            bg_color = self.button_color
        elif hovered:
            text_color = self.text_hover_color
            bg_color = self.button_hover_color
        else:
            text_color = self.text_color
            bg_color = self.button_color
        
        # Draw button background
        pg.draw.rect(surface, bg_color, rect)
        pg.draw.rect(surface, text_color, rect, 2)  # Border
        
        # Draw text centered on button
        text_surface = self.menu_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
        return rect
    
    def surface_to_texture(self, surface: pg.Surface) -> mgl.Texture:
        """
        Convert pygame surface to ModernGL texture.
        
        Args:
            surface: Pygame surface
            
        Returns:
            ModernGL texture
        """
        # Flip surface vertically because OpenGL and pygame have different coordinate systems
        flipped_surface = pg.transform.flip(surface, False, True)
        
        # Convert surface to string buffer
        texture_data = pg.image.tostring(flipped_surface, 'RGBA', False)
        
        # Create or update texture
        if self.menu_texture is None or \
           self.menu_texture.size != surface.get_size():
            if self.menu_texture:
                self.menu_texture.release()
            
            self.menu_texture = self.ctx.texture(
                surface.get_size(),
                4,
                texture_data
            )
            self.menu_texture.filter = (mgl.LINEAR, mgl.LINEAR)  # type: ignore
        else:
            self.menu_texture.write(texture_data)
        
        return self.menu_texture
    
    def create_menu_surface(self) -> pg.Surface:
        """Create a new surface for menu rendering."""
        surface = pg.Surface(self.screen_size, pg.SRCALPHA)
        surface.fill(self.bg_color)
        return surface
    
    def cleanup(self):
        """Release resources."""
        if self.menu_texture:
            self.menu_texture.release()
