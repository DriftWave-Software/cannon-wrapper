"""
Mock implementation of the cannon_wrapper module.

This module provides placeholder classes for the Canon, CanonError, and DeviceNotFoundError
classes from the cannon_wrapper module. This allows the application to run without
the actual cannon_wrapper module installed.
"""

import logging
import random
from typing import Dict, Any, Optional, List, Tuple

logger = logging.getLogger("cannon_wrapper")

class CanonError(Exception):
    """Base exception for Canon camera errors."""
    pass

class DeviceNotFoundError(CanonError):
    """Raised when no Canon device is found."""
    pass

class Canon:
    """Mock implementation of the Canon camera class."""
    
    def __init__(self):
        """Initialize the mock Canon camera."""
        self._connected = False
        self._live_view_active = False
        self._recording = False
        self._initialized = False
        
        # Mock camera info
        self._camera_info = {
            "product_name": "Canon EOS Mock",
            "serial_number": "12345678",
            "firmware_version": "1.0.0",
            "battery_level": 75
        }
        
    def connect(self) -> None:
        """Connect to a Canon camera.
        
        Raises:
            DeviceNotFoundError: If no camera is found
        """
        # Simulate a 20% chance of no camera found
        if random.random() < 0.2:
            raise DeviceNotFoundError("No Canon camera found")
            
        logger.info("Connected to mock Canon camera")
        self._connected = True
        self._initialized = True
        
    def disconnect(self) -> None:
        """Disconnect from the camera."""
        if self._live_view_active:
            self.stop_live_view()
            
        if self._recording:
            self.stop_recording()
            
        logger.info("Disconnected from mock Canon camera")
        self._connected = False
        
    def get_device_info(self) -> Dict[str, Any]:
        """Get information about the connected camera.
        
        Returns:
            Dictionary with camera information
        """
        return self._camera_info
        
    def get_battery_level(self) -> int:
        """Get the camera's battery level.
        
        Returns:
            Battery level (0-100)
        """
        return self._camera_info["battery_level"]
        
    def start_live_view(self) -> None:
        """Start the camera's live view."""
        if not self._connected:
            raise CanonError("Camera not connected")
            
        logger.info("Started mock live view")
        self._live_view_active = True
        
    def stop_live_view(self) -> None:
        """Stop the camera's live view."""
        if not self._connected:
            raise CanonError("Camera not connected")
            
        logger.info("Stopped mock live view")
        self._live_view_active = False
        
    def download_live_view_frame(self) -> Optional[bytes]:
        """Download a live view frame.
        
        Returns:
            Frame data or None if live view is not active
        """
        if not self._live_view_active:
            return None
            
        try:
            import numpy as np
            
            # Create a more interesting test pattern - a gradient background with a clock
            width, height = 640, 480
            
            # Create a gradient background
            x = np.linspace(0, 1, width)
            y = np.linspace(0, 1, height)
            X, Y = np.meshgrid(x, y)
            
            # Make a colorful gradient
            r = np.clip((X + Y) / 2, 0, 1)
            g = np.clip((1 - X + Y) / 2, 0, 1)
            b = np.clip((X + 1 - Y) / 2, 0, 1)
            
            # Convert to uint8
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:, :, 0] = r * 255
            frame[:, :, 1] = g * 255
            frame[:, :, 2] = b * 255
            
            # Draw a checkerboard pattern in the center
            checker_size = 40
            center_x, center_y = width // 2, height // 2
            offset_x, offset_y = 100, 100
            
            for i in range(-offset_x, offset_x, checker_size):
                for j in range(-offset_y, offset_y, checker_size):
                    x1 = center_x + i
                    y1 = center_y + j
                    x2 = min(x1 + checker_size, width)
                    y2 = min(y1 + checker_size, height)
                    
                    if x1 >= 0 and y1 >= 0 and x2 < width and y2 < height:
                        if (i // checker_size + j // checker_size) % 2 == 0:
                            frame[y1:y2, x1:x2, :] = 255 - frame[y1:y2, x1:x2, :]
                            
            # Add simulated date/time and info text
            import time
            import cv2
            
            # Add timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Add camera info
            cv2.putText(frame, "Canon EOS Mock", (10, height - 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "MOCK LIVE VIEW", (width - 200, height - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2, cv2.LINE_AA)
            
            return frame
        except ImportError:
            # If numpy or cv2 is not available, fall back to black frame
            return b'\x00' * (640 * 480 * 3)
        
    def take_photo(self, save_path: str = None) -> None:
        """Take a photo.
        
        Args:
            save_path: Path to save the photo
        """
        if not self._connected:
            raise CanonError("Camera not connected")
            
        logger.info(f"Taking mock photo, saving to {save_path}")
        
    def start_recording(self, save_path: str) -> None:
        """Start video recording.
        
        Args:
            save_path: Path to save the video
        """
        if not self._connected:
            raise CanonError("Camera not connected")
            
        logger.info(f"Started mock video recording, saving to {save_path}")
        self._recording = True
        
    def stop_recording(self) -> None:
        """Stop video recording."""
        if not self._connected:
            raise CanonError("Camera not connected")
            
        if not self._recording:
            raise CanonError("Not recording")
            
        logger.info("Stopped mock video recording")
        self._recording = False
        
    def is_recording(self) -> bool:
        """Check if the camera is recording.
        
        Returns:
            True if recording, False otherwise
        """
        return self._recording
        
    def can_record_video(self) -> bool:
        """Check if the camera can record video.
        
        Returns:
            True if the camera can record video, False otherwise
        """
        return True
        
    # Mock camera settings methods
    
    def get_iso(self) -> int:
        """Get the current ISO setting.
        
        Returns:
            ISO value
        """
        return 100
        
    def set_iso(self, value: int) -> None:
        """Set the ISO setting.
        
        Args:
            value: ISO value
        """
        logger.info(f"Setting mock ISO to {value}")
        
    def get_aperture(self) -> int:
        """Get the current aperture setting.
        
        Returns:
            Aperture value
        """
        return 5  # f/4.0
        
    def set_aperture(self, value: int) -> None:
        """Set the aperture setting.
        
        Args:
            value: Aperture value
        """
        logger.info(f"Setting mock aperture to {value}")
        
    def get_shutter_speed(self) -> int:
        """Get the current shutter speed setting.
        
        Returns:
            Shutter speed value
        """
        return 12  # 1/60
        
    def set_shutter_speed(self, value: int) -> None:
        """Set the shutter speed setting.
        
        Args:
            value: Shutter speed value
        """
        logger.info(f"Setting mock shutter speed to {value}")
        
    def get_white_balance(self) -> int:
        """Get the current white balance setting.
        
        Returns:
            White balance value
        """
        return 0  # Auto
        
    def set_white_balance(self, value: int) -> None:
        """Set the white balance setting.
        
        Args:
            value: White balance value
        """
        logger.info(f"Setting mock white balance to {value}")
        
    def get_available_iso_values(self) -> List[Tuple[int, str]]:
        """Get available ISO values.
        
        Returns:
            List of (value, label) tuples
        """
        return [
            (100, "100"),
            (200, "200"),
            (400, "400"),
            (800, "800"),
            (1600, "1600"),
            (3200, "3200"),
            (6400, "6400")
        ]
        
    def get_available_aperture_values(self) -> List[Tuple[int, str]]:
        """Get available aperture values.
        
        Returns:
            List of (value, label) tuples
        """
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
        
    def get_available_shutter_values(self) -> List[Tuple[int, str]]:
        """Get available shutter speed values.
        
        Returns:
            List of (value, label) tuples
        """
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
        
    def get_available_white_balance_values(self) -> List[Tuple[int, str]]:
        """Get available white balance values.
        
        Returns:
            List of (value, label) tuples
        """
        return [
            (0, "Auto"),
            (1, "Daylight"),
            (2, "Cloudy"),
            (3, "Tungsten"),
            (4, "Fluorescent"),
            (5, "Flash"),
            (6, "Custom")
        ] 