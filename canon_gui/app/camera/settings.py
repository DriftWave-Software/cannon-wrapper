"""
Camera Settings Module
Handles camera settings like ISO, shutter speed, aperture, etc.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger("canon_gui.settings")

class CameraSettings(QObject):
    """Class for managing camera settings."""
    
    # Define signals
    settings_changed = pyqtSignal(str, object)  # Setting name, new value
    settings_error = pyqtSignal(str)  # Error message
    
    # Define setting types
    SETTING_ISO = "iso"
    SETTING_APERTURE = "aperture"
    SETTING_SHUTTER = "shutter_speed"
    SETTING_WHITE_BALANCE = "white_balance"
    SETTING_EXPOSURE_COMP = "exposure_compensation"
    SETTING_SHOOT_MODE = "shooting_mode"
    SETTING_IMAGE_QUALITY = "image_quality"
    
    def __init__(self, camera_manager):
        """Initialize camera settings.
        
        Args:
            camera_manager: Camera manager instance
        """
        super().__init__()
        self._camera_manager = camera_manager
        self._settings = {}
        self._available_options = {}
        
        # Connect to camera manager signals
        self._camera_manager.camera_connected.connect(self._on_camera_connected)
        self._camera_manager.camera_disconnected.connect(self._on_camera_disconnected)
    
    def _on_camera_connected(self, camera_model: str):
        """Handle camera connection.
        
        Args:
            camera_model: Camera model name
        """
        # Try to get available settings from the camera
        self._update_available_settings()
        self._update_current_settings()
    
    def _on_camera_disconnected(self):
        """Handle camera disconnection."""
        self._settings = {}
        self._available_options = {}
    
    def _update_available_settings(self):
        """Update available settings from the camera."""
        camera = self._camera_manager.get_camera()
        if not camera:
            return
            
        try:
            # This is where you would query the camera for available settings
            # The implementation depends on how the cannon_wrapper exposes this information
            
            # For ISO
            iso_values = self._get_iso_options(camera)
            if iso_values:
                self._available_options[self.SETTING_ISO] = iso_values
            
            # For aperture
            aperture_values = self._get_aperture_options(camera)
            if aperture_values:
                self._available_options[self.SETTING_APERTURE] = aperture_values
            
            # For shutter speed
            shutter_values = self._get_shutter_options(camera)
            if shutter_values:
                self._available_options[self.SETTING_SHUTTER] = shutter_values
            
            # For white balance
            wb_values = self._get_white_balance_options(camera)
            if wb_values:
                self._available_options[self.SETTING_WHITE_BALANCE] = wb_values
            
            # Add other settings as needed
            
        except Exception as e:
            logger.error(f"Error updating available settings: {str(e)}")
            self.settings_error.emit(f"Error getting available settings: {str(e)}")
    
    def _update_current_settings(self):
        """Update current settings from the camera."""
        camera = self._camera_manager.get_camera()
        if not camera:
            return
            
        try:
            # This is where you would query the camera for current settings
            # The implementation depends on how the cannon_wrapper exposes this information
            
            # For ISO
            self._settings[self.SETTING_ISO] = self._get_current_iso(camera)
            
            # For aperture
            self._settings[self.SETTING_APERTURE] = self._get_current_aperture(camera)
            
            # For shutter speed
            self._settings[self.SETTING_SHUTTER] = self._get_current_shutter(camera)
            
            # For white balance
            self._settings[self.SETTING_WHITE_BALANCE] = self._get_current_white_balance(camera)
            
            # Add other settings as needed
            
        except Exception as e:
            logger.error(f"Error updating current settings: {str(e)}")
            self.settings_error.emit(f"Error getting current settings: {str(e)}")
    
    def _get_iso_options(self, camera) -> List[Tuple[int, str]]:
        """Get available ISO options.
        
        Args:
            camera: Camera object
        
        Returns:
            List of (value, label) tuples
        """
        # This is a placeholder - implementation depends on cannon_wrapper
        try:
            if hasattr(camera, "get_available_iso_values"):
                iso_values = camera.get_available_iso_values()
                return iso_values
            # Fallback to common values if not available
            return [
                (100, "100"),
                (200, "200"),
                (400, "400"),
                (800, "800"),
                (1600, "1600"),
                (3200, "3200"),
                (6400, "6400")
            ]
        except Exception as e:
            logger.warning(f"Could not get ISO options: {str(e)}")
            return []
    
    def _get_aperture_options(self, camera) -> List[Tuple[int, str]]:
        """Get available aperture options.
        
        Args:
            camera: Camera object
        
        Returns:
            List of (value, label) tuples
        """
        # This is a placeholder - implementation depends on cannon_wrapper
        try:
            if hasattr(camera, "get_available_aperture_values"):
                av_values = camera.get_available_aperture_values()
                return av_values
            # Fallback to common values if not available
            return [
                (1, "f/1.0"),
                (2, "f/1.4"),
                (3, "f/2.0"),
                (4, "f/2.8"),
                (5, "f/4.0"),
                (6, "f/5.6"),
                (7, "f/8.0"),
                (8, "f/11"),
                (9, "f/16"),
                (10, "f/22")
            ]
        except Exception as e:
            logger.warning(f"Could not get aperture options: {str(e)}")
            return []
    
    def _get_shutter_options(self, camera) -> List[Tuple[int, str]]:
        """Get available shutter speed options.
        
        Args:
            camera: Camera object
        
        Returns:
            List of (value, label) tuples
        """
        # This is a placeholder - implementation depends on cannon_wrapper
        try:
            if hasattr(camera, "get_available_shutter_values"):
                tv_values = camera.get_available_shutter_values()
                return tv_values
            # Fallback to common values if not available
            return [
                (1, "30\""),
                (2, "15\""),
                (3, "8\""),
                (4, "4\""),
                (5, "2\""),
                (6, "1\""),
                (7, "1/2"),
                (8, "1/4"),
                (9, "1/8"),
                (10, "1/15"),
                (11, "1/30"),
                (12, "1/60"),
                (13, "1/125"),
                (14, "1/250"),
                (15, "1/500"),
                (16, "1/1000"),
                (17, "1/2000"),
                (18, "1/4000"),
                (19, "1/8000")
            ]
        except Exception as e:
            logger.warning(f"Could not get shutter speed options: {str(e)}")
            return []
    
    def _get_white_balance_options(self, camera) -> List[Tuple[int, str]]:
        """Get available white balance options.
        
        Args:
            camera: Camera object
        
        Returns:
            List of (value, label) tuples
        """
        # This is a placeholder - implementation depends on cannon_wrapper
        try:
            if hasattr(camera, "get_available_white_balance_values"):
                wb_values = camera.get_available_white_balance_values()
                return wb_values
            # Fallback to common values if not available
            return [
                (0, "Auto"),
                (1, "Daylight"),
                (2, "Cloudy"),
                (3, "Tungsten"),
                (4, "Fluorescent"),
                (5, "Flash"),
                (6, "Custom")
            ]
        except Exception as e:
            logger.warning(f"Could not get white balance options: {str(e)}")
            return []
    
    def _get_current_iso(self, camera) -> Optional[int]:
        """Get current ISO setting.
        
        Args:
            camera: Camera object
        
        Returns:
            Current ISO value or None if not available
        """
        try:
            if hasattr(camera, "get_iso"):
                return camera.get_iso()
            return None
        except Exception as e:
            logger.warning(f"Could not get current ISO: {str(e)}")
            return None
    
    def _get_current_aperture(self, camera) -> Optional[int]:
        """Get current aperture setting.
        
        Args:
            camera: Camera object
        
        Returns:
            Current aperture value or None if not available
        """
        try:
            if hasattr(camera, "get_aperture"):
                return camera.get_aperture()
            return None
        except Exception as e:
            logger.warning(f"Could not get current aperture: {str(e)}")
            return None
    
    def _get_current_shutter(self, camera) -> Optional[int]:
        """Get current shutter speed setting.
        
        Args:
            camera: Camera object
        
        Returns:
            Current shutter speed value or None if not available
        """
        try:
            if hasattr(camera, "get_shutter_speed"):
                return camera.get_shutter_speed()
            return None
        except Exception as e:
            logger.warning(f"Could not get current shutter speed: {str(e)}")
            return None
    
    def _get_current_white_balance(self, camera) -> Optional[int]:
        """Get current white balance setting.
        
        Args:
            camera: Camera object
        
        Returns:
            Current white balance value or None if not available
        """
        try:
            if hasattr(camera, "get_white_balance"):
                return camera.get_white_balance()
            return None
        except Exception as e:
            logger.warning(f"Could not get current white balance: {str(e)}")
            return None
    
    def get_setting(self, setting_name: str) -> Any:
        """Get a camera setting.
        
        Args:
            setting_name: Setting name
        
        Returns:
            Setting value or None if not available
        """
        return self._settings.get(setting_name)
    
    def get_available_options(self, setting_name: str) -> List[Tuple[int, str]]:
        """Get available options for a setting.
        
        Args:
            setting_name: Setting name
        
        Returns:
            List of (value, label) tuples or empty list if not available
        """
        return self._available_options.get(setting_name, [])
    
    def set_setting(self, setting_name: str, value: Any) -> bool:
        """Set a camera setting.
        
        Args:
            setting_name: Setting name
            value: New value
        
        Returns:
            True if set successfully, False otherwise
        """
        camera = self._camera_manager.get_camera()
        if not camera:
            self.settings_error.emit("Cannot set setting: No camera connected")
            return False
            
        try:
            # Set the setting based on its name
            if setting_name == self.SETTING_ISO:
                if hasattr(camera, "set_iso"):
                    camera.set_iso(value)
            elif setting_name == self.SETTING_APERTURE:
                if hasattr(camera, "set_aperture"):
                    camera.set_aperture(value)
            elif setting_name == self.SETTING_SHUTTER:
                if hasattr(camera, "set_shutter_speed"):
                    camera.set_shutter_speed(value)
            elif setting_name == self.SETTING_WHITE_BALANCE:
                if hasattr(camera, "set_white_balance"):
                    camera.set_white_balance(value)
            else:
                logger.warning(f"Unknown setting: {setting_name}")
                self.settings_error.emit(f"Unknown setting: {setting_name}")
                return False
            
            # Update the settings cache
            self._settings[setting_name] = value
            self.settings_changed.emit(setting_name, value)
            return True
            
        except Exception as e:
            logger.error(f"Error setting {setting_name}: {str(e)}")
            self.settings_error.emit(f"Error setting {setting_name}: {str(e)}")
            return False
    
    def refresh_settings(self):
        """Refresh all settings from the camera."""
        self._update_available_settings()
        self._update_current_settings() 