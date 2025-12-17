import pygame as pg
from menu.base_menu import BaseMenu, MenuItem
from menu.menu_renderer import MenuRenderer
from typing import Callable


class MainMenu(BaseMenu):
    """Main menu implementation."""
    
    def __init__(self, renderer: MenuRenderer, 
                 on_new_game: Callable, 
                 on_settings: Callable,
                 on_exit: Callable):
        super().__init__()
        self.renderer = renderer
        
        # Create menu items
        self.items = [
            MenuItem("New Game", on_new_game, enabled=True),
            MenuItem("Load Game", None, enabled=False),  # Disabled for now
            MenuItem("Settings", on_settings, enabled=True),
            MenuItem("Exit", on_exit, enabled=True),
        ]
        
        self.title = "PyFPS"
        self.surface = None
    
    def update(self, delta_time: float):
        """Update main menu logic."""
        # Nothing to update for static menu
        pass
    
    def render(self, surface: pg.Surface):
        """Render main menu."""
        # Clear surface
        surface.fill(self.renderer.bg_color)
        
        # Get screen dimensions
        screen_width, screen_height = surface.get_size()
        center_x = screen_width // 2
        
        # Render title
        title_y = screen_height // 4
        self.renderer.render_text(
            surface, self.title,
            (center_x, title_y),
            font=self.renderer.title_font,
            center=True
        )
        
        # Render menu items
        button_width = 300
        button_height = 60
        button_spacing = 20
        start_y = screen_height // 2
        
        for i, item in enumerate(self.items):
            y = start_y + i * (button_height + button_spacing)
            x = center_x - button_width // 2
            
            item.rect = pg.Rect(x, y, button_width, button_height)
            
            # Highlight selected item
            is_hovered = (i == self.selected_index) or item.hovered
            
            self.renderer.render_button(
                surface, item.text, item.rect,
                hovered=is_hovered,
                enabled=item.enabled
            )
        
        self.surface = surface
    
    def handle_event(self, event: pg.event.Event):
        """Handle input events."""
        if event.type == pg.MOUSEMOTION:
            self.handle_mouse_motion(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos, event.button)
        elif event.type == pg.KEYDOWN:
            self.handle_keyboard_navigation(event)
