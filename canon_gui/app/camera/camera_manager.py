"""
Camera Manager Module
Handles camera connection, disconnection, and status monitoring.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple, Callable
from PyQt6.QtCore import QObject, pyqtSignal

# Import the cannon_wrapper
try:
    # Try to import the real cannon_wrapper
    from cannon_wrapper import Canon, CanonError, DeviceNotFoundError, ConnectionError, OperationError
    _has_camera = True
    _is_mock = False
    logging.info("Using real cannon_wrapper module")
except ImportError:
    try:
        # Try to import our mock implementation
        from app.utils.mocks.cannon_wrapper import Canon, CanonError, DeviceNotFoundError
        _has_camera = True
        _is_mock = True
        logging.info("Using mock cannon_wrapper module")
    except ImportError:
        logging.warning("Could not import cannon_wrapper. Camera functionality will be disabled.")
        _has_camera = False
        _is_mock = False
        # Create placeholder classes for type hints
        class Canon:
            pass
        class CanonError(Exception):
            pass
        class DeviceNotFoundError(Exception):
            pass

logger = logging.getLogger("canon_gui.camera")

class CameraManager(QObject):
    """Manager class for controlling Canon cameras."""
    
    # Define signals
    camera_connected = pyqtSignal(str)  # Camera model name
    camera_disconnected = pyqtSignal()
    camera_error = pyqtSignal(str)  # Error message
    status_changed = pyqtSignal(str)  # Status message
    
    def __init__(self):
        """Initialize the camera manager."""
        super().__init__()
        
        self._camera = None
        self._is_connected = False
        self._camera_info = {}
        
        # Check if camera functionality is available
        if not _has_camera:
            logger.warning("Camera functionality is disabled.")
            self.camera_error.emit("Could not load camera module. Camera functionality is disabled.")
        elif _is_mock:
            logger.info("Using mock camera implementation.")
            self.status_changed.emit("Using mock camera - real hardware not available")
    
    def is_available(self) -> bool:
        """Check if camera functionality is available.
        
        Returns:
            True if camera functionality is available, False otherwise.
        """
        return _has_camera
    
    def connect_camera(self) -> bool:
        """Connect to a camera.
        
        Returns:
            True if connected successfully, False otherwise.
        """
        if not _has_camera:
            self.camera_error.emit("Camera module not available")
            return False
            
        try:
            self.status_changed.emit("Connecting to camera...")
            self._camera = Canon()
            
            # Get the first available camera - in a real implementation, we should
            # discover cameras and let the user select one

            # The EDSDK C++ layer should handle camera discovery
            # For now, we'll assume there's a camera available
            # TODO: Add proper camera discovery
            camera_ref = "CAMERA_REF_PLACEHOLDER"  # This needs to be replaced with actual camera reference
            self._camera.connect(camera_ref)
            
            # Get camera information
            self._camera_info = {
                "model": self._camera.get_model_name(),
                "serial": "Unknown",  # Add if available in your wrapper
                "battery": self._camera.get_battery_level()
            }
            
            self._is_connected = True
            self.camera_connected.emit(self._camera_info["model"])
            self.status_changed.emit(f"Connected to {self._camera_info['model']}")
            return True
            
        except DeviceNotFoundError:
            self.camera_error.emit("No camera found. Please make sure a camera is connected and turned on.")
            self.status_changed.emit("Connection failed: No camera found")
            return False
        except ConnectionError as e:
            self.camera_error.emit(f"Error connecting to camera: {str(e)}")
            self.status_changed.emit("Connection failed")
            return False
        except CanonError as e:
            self.camera_error.emit(f"Error connecting to camera: {str(e)}")
            self.status_changed.emit("Connection failed")
            return False
    
    def disconnect_camera(self) -> bool:
        """Disconnect from the camera.
        
        Returns:
            True if disconnected successfully, False otherwise.
        """
        if not self._is_connected or not self._camera:
            return True
            
        try:
            self.status_changed.emit("Disconnecting camera...")
            self._camera.disconnect()
            self._is_connected = False
            self._camera = None
            self.camera_disconnected.emit()
            self.status_changed.emit("Camera disconnected")
            return True
        except OperationError as e:
            self.camera_error.emit(f"Error disconnecting camera: {str(e)}")
            return False
        except CanonError as e:
            self.camera_error.emit(f"Error disconnecting camera: {str(e)}")
            return False
    
    def is_connected(self) -> bool:
        """Check if a camera is connected.
        
        Returns:
            True if a camera is connected, False otherwise.
        """
        return self._is_connected
    
    def get_camera_info(self) -> Dict[str, Any]:
        """Get information about the connected camera.
        
        Returns:
            Dictionary with camera information.
        """
        return self._camera_info
    
    def get_camera(self) -> Optional[Canon]:
        """Get the camera object.
        
        Returns:
            Camera object if connected, None otherwise.
        """
        return self._camera 