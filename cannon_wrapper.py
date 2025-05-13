"""
Canon Wrapper Module
A high-level Python wrapper for interacting with Canon cameras via EDSDK_bindings.
"""

import os
import time
import logging
import threading
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import numpy as np
from datetime import datetime

try:
    import edsdk_bindings as eds
except ImportError:
    raise ImportError("Could not import edsdk_bindings. Make sure the C++ bindings have been built.")

# Set up logging
logger = logging.getLogger("cannon_wrapper")

# Custom exceptions
class CanonError(Exception):
    """Base exception for Canon camera errors."""
    pass

class DeviceNotFoundError(CanonError):
    """Exception raised when no camera is found."""
    pass

class ConnectionError(CanonError):
    """Exception raised when there's an error connecting to the camera."""
    pass

class OperationError(CanonError):
    """Exception raised when a camera operation fails."""
    pass

# Function to get camera references from EDSDK
def get_camera_list() -> List[Any]:
    """Get a list of connected Canon cameras.
    
    Returns:
        List of camera references.
        
    Raises:
        DeviceNotFoundError: If no cameras are found.
    """
    try:
        # Initialize the SDK
        if eds.EdsInitializeSDK() != eds.EdsError.OK:
            raise ConnectionError("Failed to initialize EDSDK")
            
        # Get the camera list
        camera_list = eds.EdsGetCameraList()
        if camera_list is None:
            raise DeviceNotFoundError("Failed to get camera list")
            
        # Get the number of cameras
        camera_count = eds.EdsGetChildCount(camera_list)
        if camera_count == 0:
            raise DeviceNotFoundError("No cameras found")
            
        # Get camera references
        camera_refs = []
        for i in range(camera_count):
            camera_ref = eds.EdsGetChildAtIndex(camera_list, i)
            if camera_ref is not None:
                camera_refs.append(camera_ref)
                
        # Release the camera list
        eds.EdsRelease(camera_list)
        
        return camera_refs
        
    except Exception as e:
        if isinstance(e, DeviceNotFoundError):
            raise
        raise DeviceNotFoundError(f"Error getting camera list: {str(e)}")
    finally:
        # Terminate the SDK
        eds.EdsTerminateSDK()

class EdsEventListener(eds.Observer):
    """Event listener for Canon camera events."""
    
    def __init__(self, camera):
        super().__init__()  # Required for pybind11 subclassing
        self.camera = camera
        self.callbacks = {}
    
    def update(self, event):
        """Called when an event is received from the camera."""
        event_name = event.get_event()
        event_data = event.get_arg()
        
        logger.debug(f"Received event: {event_name}")
        
        # Handle the event if we have a callback registered
        if event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                try:
                    callback(event_data)
                except Exception as e:
                    logger.error(f"Error in event callback for {event_name}: {str(e)}")
    
    def add_callback(self, event_name: str, callback: Callable):
        """Add a callback for a specific event."""
        if event_name not in self.callbacks:
            self.callbacks[event_name] = []
        self.callbacks[event_name].append(callback)
    
    def remove_callback(self, event_name: str, callback: Callable):
        """Remove a callback for a specific event."""
        if event_name in self.callbacks and callback in self.callbacks[event_name]:
            self.callbacks[event_name].remove(callback)


class Canon:
    """High-level interface for Canon cameras using EDSDK."""
    
    def __init__(self):
        """Initialize the Canon camera interface."""
        self._model = None
        self._controller = eds.CameraController()
        self._processor = eds.Processor()
        self._event_listener = None
        self._is_connected = False
        self._live_view_active = False
        
        # Start the processor thread
        self._processor.run()
        
        # Initialize EDSDK (usually handled by the controller)
        self._controller.run()
    
    def connect(self, camera_ref=None):
        """Connect to a Canon camera.
        
        Args:
            camera_ref: Optional camera reference. If None, connects to the first available camera.
            
        Raises:
            DeviceNotFoundError: If no camera is found.
            ConnectionError: If the connection fails.
        """
        if self._is_connected:
            return
        
        try:
            # If no camera reference is provided, try to get the first available camera
            if camera_ref is None:
                camera_list = get_camera_list()
                if not camera_list:
                    raise DeviceNotFoundError("No cameras found")
                camera_ref = camera_list[0]
            
            # Create the camera model
            self._model = eds.CameraModel(camera_ref)
            self._controller.set_camera_model(self._model)
            
            # Create and set the event listener
            self._event_listener = EdsEventListener(self)
            self._model.add_observer(self._event_listener)
            
            # Open the session
            cmd = eds.OpenSessionCommand(self._model.get_camera_object())
            if not cmd.execute():
                raise ConnectionError("Failed to open camera session")
            
            # Set camera capacity (needed for some operations)
            capacity = eds.EdsCapacity()
            capacity.reset = 1
            capacity.bytes_per_sector = 0x1000
            capacity.number_of_free_clusters = 0x7FFFFFFF  # Max value
            capacity_cmd = eds.SetCapacityCommand(self._model.get_camera_object(), capacity)
            capacity_cmd.execute()
            
            self._is_connected = True
            logger.info(f"Connected to camera: {self.get_model_name()}")
            
        except Exception as e:
            if isinstance(e, (DeviceNotFoundError, ConnectionError)):
                raise
            raise ConnectionError(f"Error connecting to camera: {str(e)}")
    
    def disconnect(self):
        """Disconnect from the camera.
        
        Raises:
            OperationError: If the disconnection fails.
        """
        if not self._is_connected:
            return
        
        try:
            # Stop live view if it's active
            if self._live_view_active:
                self.stop_live_view()
            
            # Close the session
            cmd = eds.CloseSessionCommand(self._model.get_camera_object())
            if not cmd.execute():
                raise OperationError("Failed to close camera session")
            
            self._is_connected = False
            self._model = None
            self._event_listener = None
            
            logger.info("Disconnected from camera")
            
        except Exception as e:
            if isinstance(e, OperationError):
                raise
            raise OperationError(f"Error disconnecting from camera: {str(e)}")
    
    def is_connected(self) -> bool:
        """Check if the camera is connected.
        
        Returns:
            True if connected, False otherwise.
        """
        return self._is_connected
        
    def get_model_name(self) -> str:
        """Get the camera model name.
        
        Returns:
            Camera model name.
            
        Raises:
            OperationError: If getting the model name fails.
        """
        self._ensure_connected()
        try:
            return self._model.get_model_name()
        except Exception as e:
            raise OperationError(f"Error getting model name: {str(e)}")
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get information about the connected camera.
        
        Returns:
            Dictionary with camera information.
            
        Raises:
            OperationError: If getting the device info fails.
        """
        self._ensure_connected()
        
        try:
            # Collect basic camera information
            info = {
                "product_name": self._model.get_model_name(),
                # Add other properties as needed
            }
            
            return info
            
        except Exception as e:
            raise OperationError(f"Error getting device info: {str(e)}")
    
    def get_battery_level(self) -> int:
        """Get the camera battery level.
        
        Returns:
            Battery level percentage (0-100).
            
        Raises:
            OperationError: If getting the battery level fails.
        """
        self._ensure_connected()
        
        try:
            # Implement battery level retrieval if available in EDSDK
            # This is a placeholder - actual implementation depends on how EDSDK exposes this
            return 100  # Default to 100% if not available
            
        except Exception as e:
            raise OperationError(f"Error getting battery level: {str(e)}")
    
    # -------------------------------------------------------------------------
    # Camera operations
    # -------------------------------------------------------------------------
    
    def take_picture(self) -> bool:
        """Take a picture with the camera.
        
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If taking the picture fails.
        """
        self._ensure_connected()
        
        try:
            cmd = eds.TakePictureCommand(self._model.get_camera_object())
            return cmd.execute()
            
        except Exception as e:
            raise OperationError(f"Error taking picture: {str(e)}")
    
    def press_shutter(self, mode: int) -> bool:
        """Press the shutter button in a specific mode.
        
        Args:
            mode: Shutter button mode (from eds.EdsCameraCommand)
            
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If pressing the shutter fails.
        """
        self._ensure_connected()
        
        try:
            cmd = eds.PressShutterButtonCommand(self._model.get_camera_object(), mode)
            return cmd.execute()
            
        except Exception as e:
            raise OperationError(f"Error pressing shutter button: {str(e)}")
    
    # -------------------------------------------------------------------------
    # Live view operations
    # -------------------------------------------------------------------------
    
    def start_live_view(self) -> bool:
        """Start the camera's live view (EVF) mode.
        
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If starting live view fails.
        """
        self._ensure_connected()
        
        if self._live_view_active:
            return True
        
        try:
            # Set the camera to live view mode
            self._model.set_evf_mode(1)
            self._model.set_evf_output_device(3)  # PC live view
            
            # Execute the start command
            cmd = eds.StartEvfCommand(self._model.get_camera_object())
            if not cmd.execute():
                raise OperationError("Failed to start live view")
            
            self._live_view_active = True
            return True
            
        except Exception as e:
            raise OperationError(f"Error starting live view: {str(e)}")
    
    def stop_live_view(self) -> bool:
        """Stop the camera's live view (EVF) mode.
        
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If stopping live view fails.
        """
        self._ensure_connected()
        
        if not self._live_view_active:
            return True
        
        try:
            # Execute the end command
            cmd = eds.EndEvfCommand(self._model.get_camera_object())
            if not cmd.execute():
                raise OperationError("Failed to stop live view")
            
            self._live_view_active = False
            return True
            
        except Exception as e:
            raise OperationError(f"Error stopping live view: {str(e)}")
    
    def download_live_view_frame(self) -> np.ndarray:
        """Download the current live view frame.
        
        Returns:
            NumPy array containing the image data.
            
        Raises:
            OperationError: If downloading the frame fails.
        """
        self._ensure_connected()
        
        if not self._live_view_active:
            self.start_live_view()
        
        try:
            # Execute the download command
            cmd = eds.DownloadEvfCommand(self._model.get_camera_object())
            if not cmd.execute():
                raise OperationError("Failed to download live view frame")
            
            # Convert the EVF data to a NumPy array
            # This depends on how the data is returned from the EDSDK
            # Will need to be adjusted based on the actual implementation
            
            # For now, just return an empty image
            return np.zeros((480, 640, 3), dtype=np.uint8)
            
        except Exception as e:
            raise OperationError(f"Error downloading live view frame: {str(e)}")
    
    def focus(self, direction: int, level: int = 3) -> bool:
        """Focus the lens in the specified direction.
        
        Args:
            direction: Focus direction (1 for near, -1 for far)
            level: Focus adjustment level (1-3), where 3 is the largest step
            
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If focusing fails.
        """
        self._ensure_connected()
        
        if not self._live_view_active:
            self.start_live_view()
        
        try:
            # Determine the drive lens mode
            if direction > 0:  # Near
                if level == 3:
                    drive_lens = eds.EdsEvfDriveLens.NEAR_3
                elif level == 2:
                    drive_lens = eds.EdsEvfDriveLens.NEAR_2
                else:
                    drive_lens = eds.EdsEvfDriveLens.NEAR_1
            else:  # Far
                if level == 3:
                    drive_lens = eds.EdsEvfDriveLens.FAR_3
                elif level == 2:
                    drive_lens = eds.EdsEvfDriveLens.FAR_2
                else:
                    drive_lens = eds.EdsEvfDriveLens.FAR_1
            
            # Execute the drive lens command
            cmd = eds.DriveLensCommand(self._model.get_camera_object(), drive_lens)
            return cmd.execute()
            
        except Exception as e:
            raise OperationError(f"Error focusing lens: {str(e)}")
    
    # -------------------------------------------------------------------------
    # Camera settings
    # -------------------------------------------------------------------------
    
    def get_iso(self) -> int:
        """Get the current ISO value.
        
        Returns:
            ISO value.
            
        Raises:
            OperationError: If getting the ISO fails.
        """
        self._ensure_connected()
        
        try:
            return self._model.get_iso()
        except Exception as e:
            raise OperationError(f"Error getting ISO: {str(e)}")
    
    def set_iso(self, iso: int) -> bool:
        """Set the ISO value.
        
        Args:
            iso: ISO value to set.
            
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If setting the ISO fails.
        """
        self._ensure_connected()
        
        try:
            self._model.set_iso(iso)
            return True
        except Exception as e:
            raise OperationError(f"Error setting ISO: {str(e)}")
    
    def get_available_iso_values(self) -> List[Tuple[int, str]]:
        """Get the available ISO values.
        
        Returns:
            List of (value, label) tuples.
            
        Raises:
            OperationError: If getting the available values fails.
        """
        self._ensure_connected()
        
        try:
            # Get the ISO description
            iso_desc = self._model.get_property_desc(eds.EdsPropertyID.ISO_SPEED)
            
            # Convert to a list of (value, label) tuples
            result = []
            for value in iso_desc:
                label = eds.Iso.get_label(value)
                result.append((value, label))
            
            return result
        except Exception as e:
            raise OperationError(f"Error getting available ISO values: {str(e)}")
    
    def get_aperture(self) -> int:
        """Get the current aperture value.
        
        Returns:
            Aperture value.
            
        Raises:
            OperationError: If getting the aperture fails.
        """
        self._ensure_connected()
        
        try:
            return self._model.get_av()
        except Exception as e:
            raise OperationError(f"Error getting aperture: {str(e)}")
    
    def set_aperture(self, aperture: int) -> bool:
        """Set the aperture value.
        
        Args:
            aperture: Aperture value to set.
            
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If setting the aperture fails.
        """
        self._ensure_connected()
        
        try:
            self._model.set_av(aperture)
            return True
        except Exception as e:
            raise OperationError(f"Error setting aperture: {str(e)}")
    
    def get_available_aperture_values(self) -> List[Tuple[int, str]]:
        """Get the available aperture values.
        
        Returns:
            List of (value, label) tuples.
            
        Raises:
            OperationError: If getting the available values fails.
        """
        self._ensure_connected()
        
        try:
            # Get the aperture description
            av_desc = self._model.get_property_desc(eds.EdsPropertyID.AV)
            
            # Convert to a list of (value, label) tuples
            result = []
            for value in av_desc:
                label = eds.Av.get_label(value)
                result.append((value, label))
            
            return result
        except Exception as e:
            raise OperationError(f"Error getting available aperture values: {str(e)}")
    
    def get_shutter_speed(self) -> int:
        """Get the current shutter speed value.
        
        Returns:
            Shutter speed value.
            
        Raises:
            OperationError: If getting the shutter speed fails.
        """
        self._ensure_connected()
        
        try:
            return self._model.get_tv()
        except Exception as e:
            raise OperationError(f"Error getting shutter speed: {str(e)}")
    
    def set_shutter_speed(self, shutter_speed: int) -> bool:
        """Set the shutter speed value.
        
        Args:
            shutter_speed: Shutter speed value to set.
            
        Returns:
            True if successful, False otherwise.
            
        Raises:
            OperationError: If setting the shutter speed fails.
        """
        self._ensure_connected()
        
        try:
            self._model.set_tv(shutter_speed)
            return True
        except Exception as e:
            raise OperationError(f"Error setting shutter speed: {str(e)}")
    
    def get_available_shutter_values(self) -> List[Tuple[int, str]]:
        """Get the available shutter speed values.
        
        Returns:
            List of (value, label) tuples.
            
        Raises:
            OperationError: If getting the available values fails.
        """
        self._ensure_connected()
        
        try:
            # Get the shutter speed description
            tv_desc = self._model.get_property_desc(eds.EdsPropertyID.TV)
            
            # Convert to a list of (value, label) tuples
            result = []
            for value in tv_desc:
                label = eds.Tv.get_label(value)
                result.append((value, label))
            
            return result
        except Exception as e:
            raise OperationError(f"Error getting available shutter speed values: {str(e)}")
    
    def _ensure_connected(self):
        """Ensure that the camera is connected.
        
        Raises:
            ConnectionError: If the camera is not connected.
        """
        if not self._is_connected or not self._model:
            raise ConnectionError("Camera is not connected")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect() 