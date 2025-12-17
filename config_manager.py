import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages game configuration persistence."""
    
    DEFAULT_SETTINGS = {
        'video': {
            'resolution': [0, 0],  # [0, 0] means auto-detect
            'display_mode': 'windowed',  # windowed | fullscreen | borderless
            'vsync': True
        }
    }
    
    def __init__(self, config_file='config/settings.json'):
        self.config_file = config_file
        self.settings = self.load()
    
    def load(self) -> Dict[str, Any]:
        """
        Load settings from JSON file.
        
        Returns:
            Settings dictionary
        """
        config_path = Path(self.config_file)
        
        # Create config directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load from file if it exists
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    settings = json.load(f)
                    # Validate and merge with defaults
                    return self._merge_with_defaults(settings)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.get_default_settings()
        
        # Return defaults and save them
        defaults = self.get_default_settings()
        self.save(defaults)
        return defaults
    
    def save(self, settings: Dict[str, Any] | None = None) -> bool:
        """
        Save settings to JSON file.
        
        Args:
            settings: Settings to save. If None, saves current settings.
            
        Returns:
            True if successful, False otherwise
        """
        if settings is None:
            settings = self.settings
        
        # Validate settings
        if not self.validate_settings(settings):
            print("Invalid settings. Not saving.")
            return False
        
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(settings, f, indent=2)
            self.settings = settings
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Return a copy of default settings."""
        import copy
        return copy.deepcopy(self.DEFAULT_SETTINGS)
    
    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Validate settings structure and values.
        
        Args:
            settings: Settings dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(settings, dict):
            return False
        
        # Check video settings
        if 'video' not in settings:
            return False
        
        video = settings['video']
        if not isinstance(video, dict):
            return False
        
        # Validate resolution
        if 'resolution' in video:
            res = video['resolution']
            # Allow [0, 0] for auto-detect
            if not (isinstance(res, list) and len(res) == 2 and 
                    all(isinstance(x, int) and x >= 0 for x in res)):
                return False
        
        # Validate display mode
        if 'display_mode' in video:
            if video['display_mode'] not in ['windowed', 'fullscreen', 'borderless']:
                return False
        
        return True
    
    def _merge_with_defaults(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded settings with defaults to ensure all keys exist."""
        import copy
        merged = copy.deepcopy(self.DEFAULT_SETTINGS)
        
        # Deep merge
        for key, value in settings.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key].update(value)
            else:
                merged[key] = value
        
        return merged
    
    def get(self, *keys: str, default=None) -> Any:
        """Get a setting value using dot notation."""
        value = self.settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, *keys: str, value: Any) -> bool:
        """Set a setting value using dot notation."""
        if len(keys) == 0:
            return False
        
        # Navigate to parent
        current = self.settings
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set value
        current[keys[-1]] = value
        return True
