import pygame as pg
from menu.base_menu import BaseMenu, MenuItem
from menu.menu_renderer import MenuRenderer
from config_manager import ConfigManager
from typing import Callable, List, Tuple


class SettingsMenu(BaseMenu):
    """Settings menu for video configuration."""
    
    RESOLUTIONS = [
        None,  # Auto-detect
        (1280, 720),
        (1600, 900),
        (1920, 1080),
        (2560, 1440),
    ]
    
    DISPLAY_MODES = ['windowed', 'fullscreen', 'borderless']
    
    def __init__(self, renderer: MenuRenderer, 
                 config_manager: ConfigManager,
                 on_back: Callable,
                 on_apply_settings: Callable):
        super().__init__()
        self.renderer = renderer
        self.config = config_manager
        self.on_back = on_back
        self.on_apply_settings = on_apply_settings
        
        # Current settings (working copy)
        self.current_resolution_index = 0
        self.current_display_mode_index = 0
        
        # Load current settings
        self._load_current_settings()
        
        # Create menu items
        self.items = [
            MenuItem("Resolution", self._cycle_resolution, enabled=True),
            MenuItem("Display Mode", self._cycle_display_mode, enabled=True),
            MenuItem("Apply", self._apply_settings, enabled=True),
            MenuItem("Back", self._cancel, enabled=True),
        ]
        
        self.surface = None
    
    def _load_current_settings(self):
        """Load current settings from config."""
        current_res = self.config.get('video', 'resolution')
        
        # Check if it's auto-detect
        if current_res is None or (isinstance(current_res, list) and current_res == [0, 0]):
            self.current_resolution_index = 0
        else:
            current_res = tuple(current_res)
            try:
                self.current_resolution_index = self.RESOLUTIONS.index(current_res)
            except ValueError:
                self.current_resolution_index = 0
            self.current_resolution_index = 0
        
        current_mode = self.config.get('video', 'display_mode')
        try:
            self.current_display_mode_index = self.DISPLAY_MODES.index(current_mode)
        except ValueError:
            self.current_display_mode_index = 0
    
    def _cycle_resolution(self):
        """Cycle to next resolution."""
        self.current_resolution_index = (self.current_resolution_index + 1) % len(self.RESOLUTIONS)
    
    def _cycle_display_mode(self):
        """Cycle to next display mode."""
        self.current_display_mode_index = (self.current_display_mode_index + 1) % len(self.DISPLAY_MODES)
    
    def _apply_settings(self):
        """Apply and save settings."""
        # Update config
        resolution = self.RESOLUTIONS[self.current_resolution_index]
        if resolution is None:
            # Auto-detect - save as [0, 0]
            resolution = [0, 0]
        else:
            resolution = list(resolution)
        
        display_mode = self.DISPLAY_MODES[self.current_display_mode_index]
        
        self.config.set('video', 'resolution', value=resolution)
        self.config.set('video', 'display_mode', value=display_mode)
        self.config.save()
        
        # Apply settings immediately
        self.on_apply_settings()
        
        # Go back to main menu
        self.on_back()
    
    def _cancel(self):
        """Cancel and go back without saving."""
        self._load_current_settings()  # Reset to saved values
        self.on_back()
    
    def update(self, delta_time: float):
        """Update settings menu logic."""
        pass
    
    def render(self, surface: pg.Surface):
        """Render settings menu."""
        # Clear surface
        surface.fill(self.renderer.bg_color)
        
        # Get screen dimensions
        screen_width, screen_height = surface.get_size()
        center_x = screen_width // 2
        
        # Render title
        title_y = 100
        self.renderer.render_text(
            surface, "Settings",
            (center_x, title_y),
            font=self.renderer.title_font,
            center=True
        )
        
        # Render menu items with current values
        button_width = 500
        button_height = 60
        button_spacing = 20
        start_y = 250
        
        for i, item in enumerate(self.items):
            y = start_y + i * (button_height + button_spacing)
            x = center_x - button_width // 2
            
            item.rect = pg.Rect(x, y, button_width, button_height)
            
            # Build display text with current value
            if item.text == "Resolution":
                res = self.RESOLUTIONS[self.current_resolution_index]
                if res is None:
                    display_text = "Resolution: Auto"
                else:
                    display_text = f"Resolution: {res[0]}x{res[1]}"
            elif item.text == "Display Mode":
                mode = self.DISPLAY_MODES[self.current_display_mode_index]
                display_text = f"Display: {mode.capitalize()}"
            else:
                display_text = item.text
            
            # Highlight selected item
            is_hovered = (i == self.selected_index) or item.hovered
            
            self.renderer.render_button(
                surface, display_text, item.rect,
                hovered=is_hovered,
                enabled=item.enabled
            )
        
        # Render hint text
        hint_y = screen_height - 50
        self.renderer.render_text(
            surface, "Arrow keys/Click to change • Enter/Click Apply to save",
            (center_x, hint_y),
            font=self.renderer.small_font,
            color=(150, 150, 150),
            center=True
        )
        
        self.surface = surface
    
    def handle_event(self, event: pg.event.Event):
        """Handle input events."""
        if event.type == pg.MOUSEMOTION:
            self.handle_mouse_motion(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos, event.button)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._cancel()
            else:
                self.handle_keyboard_navigation(event)
