"""Menu system for PyFPS game."""

from menu.base_menu import BaseMenu, MenuItem
from menu.menu_renderer import MenuRenderer
from menu.main_menu import MainMenu
from menu.settings_menu import SettingsMenu

__all__ = [
    'BaseMenu',
    'MenuItem',
    'MenuRenderer',
    'MainMenu',
    'SettingsMenu',
]
