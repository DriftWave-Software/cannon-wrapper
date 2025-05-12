"""
Configuration module for Canon Camera Control GUI.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("canon_gui.utils.config")

# Default configuration
DEFAULT_CONFIG = {
    "app": {
        "auto_connect": False,
        "auto_download": True,
        "save_path": os.path.expanduser("~/Pictures/CanonControl"),
        "log_level": "INFO"
    },
    "camera": {
        "default_iso": 100,
        "default_aperture": 8,
        "default_shutter": 1/125,
        "default_wb": "auto"
    },
    "live_view": {
        "fps": 10,
        "show_focus_peaking": False,
        "show_histogram": False,
        "show_grid": False
    },
    "capture": {
        "filename_template": "IMG_{date}_{time}_{seq}",
        "self_timer": 0,
        "interval": 10,
        "num_shots": 10,
        "format": "JPEG",
        "jpeg_quality": "Fine",
        "jpeg_size": "Large"
    }
}

class Config:
    """Configuration class for the application."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize the configuration.
        
        Args:
            config_file: Path to the configuration file
        """
        self._config_file = config_file
        self._config = DEFAULT_CONFIG.copy()
        
        # Load configuration from file if it exists
        self.load()
    
    def load(self) -> bool:
        """Load configuration from file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if os.path.exists(self._config_file):
                with open(self._config_file, "r") as f:
                    loaded_config = json.load(f)
                
                # Update configuration with loaded values
                self._update_config(self._config, loaded_config)
                logger.info(f"Configuration loaded from {self._config_file}")
                return True
            else:
                logger.info(f"Configuration file {self._config_file} doesn't exist, using defaults")
                return False
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            return False
    
    def save(self) -> bool:
        """Save configuration to file.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self._config_file, "w") as f:
                json.dump(self._config, f, indent=4)
            
            logger.info(f"Configuration saved to {self._config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def _update_config(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Recursively update configuration dictionary.
        
        Args:
            target: Target dictionary to update
            source: Source dictionary with new values
        """
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    # Recursively update nested dictionaries
                    self._update_config(target[key], value)
                else:
                    # Update value
                    target[key] = value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
        
        Returns:
            Configuration value or default if not found
        """
        if section in self._config and key in self._config[section]:
            return self._config[section][key]
        return default
    
    def set(self, section: str, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Configuration value
        """
        if section not in self._config:
            self._config[section] = {}
        
        self._config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get a configuration section.
        
        Args:
            section: Configuration section
        
        Returns:
            Configuration section or empty dictionary if not found
        """
        return self._config.get(section, {})


# Global configuration instance
config = Config()


def setup_logging() -> None:
    """Set up logging based on configuration."""
    log_level_str = config.get("app", "log_level", "INFO")
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger.info(f"Logging initialized with level {log_level_str}") 