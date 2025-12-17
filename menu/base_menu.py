from abc import ABC, abstractmethod
import pygame as pg
from typing import List, Tuple


class MenuItem:
    """Represents a single menu item."""
    
    def __init__(self, text: str, action=None, enabled=True):
        self.text = text
        self.action = action
        self.enabled = enabled
        self.hovered = False
        self.rect = pg.Rect(0, 0, 0, 0)  # Set during rendering
    
    def execute(self):
        """Execute the menu item's action."""
        if self.enabled and self.action:
            self.action()


class BaseMenu(ABC):
    """Abstract base class for all menus."""
    
    def __init__(self):
        self.items: List[MenuItem] = []
        self.selected_index = 0
        self.is_active = True
    
    @abstractmethod
    def update(self, delta_time: float):
        """
        Update menu logic.
        
        Args:
            delta_time: Time since last frame in milliseconds
        """
        pass
    
    @abstractmethod
    def render(self, surface: pg.Surface):
        """
        Render menu to a pygame surface.
        
        Args:
            surface: Pygame surface to render to
        """
        pass
    
    @abstractmethod
    def handle_event(self, event: pg.event.Event):
        """
        Handle input events.
        
        Args:
            event: Pygame event
        """
        pass
    
    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Update hover states based on mouse position."""
        for i, item in enumerate(self.items):
            if item.enabled and item.rect.collidepoint(pos):
                item.hovered = True
                self.selected_index = i
            else:
                item.hovered = False
    
    def handle_mouse_click(self, pos: Tuple[int, int], button: int):
        """Handle mouse click on menu items."""
        if button == 1:  # Left click
            for item in self.items:
                if item.enabled and item.rect.collidepoint(pos):
                    item.execute()
    
    def handle_keyboard_navigation(self, event: pg.event.Event):
        """Handle keyboard navigation (arrow keys, enter)."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self._select_previous()
            elif event.key == pg.K_DOWN:
                self._select_next()
            elif event.key == pg.K_RETURN:
                if 0 <= self.selected_index < len(self.items):
                    self.items[self.selected_index].execute()
    
    def _select_next(self):
        """Select next enabled menu item."""
        start_index = self.selected_index
        while True:
            self.selected_index = (self.selected_index + 1) % len(self.items)
            if self.items[self.selected_index].enabled or self.selected_index == start_index:
                break
    
    def _select_previous(self):
        """Select previous enabled menu item."""
        start_index = self.selected_index
        while True:
            self.selected_index = (self.selected_index - 1) % len(self.items)
            if self.items[self.selected_index].enabled or self.selected_index == start_index:
                break
