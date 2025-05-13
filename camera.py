"""
High-level Python wrapper for Canon EDSDK camera control.
"""

import inspect
import functools
from typing import Dict, List, Any, Optional, Tuple, Union, Callable

try:
    from . import edsdk_bindings
except ImportError:
    raise ImportError("Could not import edsdk_bindings. Make sure the C++ bindings have been built.")


class Canon:
    """Main Canon camera interface providing a Pythonic wrapper."""
    
    def __init__(self):
        """Initialize the Canon camera interface."""
        self._controller = edsdk_bindings.CameraController()
        self._model = None
        self._initialized = False

    def initialize(self):
        """Initialize the camera connection."""
        if self._initialized:
            return
            
        self._controller.run()
        self._initialized = True

    def connect_to_camera(self, camera_ref=None):
        """Connect to a Canon camera.
        
        Args:
            camera_ref: Optional camera reference. If None, uses the first available camera.
        """
        # Placeholder for getting camera ref - would need to use EDSDK methods
        if camera_ref is None:
            # In a real implementation, would search for cameras and use the first one
            # For now, assume the caller provides a valid camera_ref
            raise ValueError("camera_ref must be provided")
            
        self._model = edsdk_bindings.CameraModel(camera_ref)
        self._controller.set_camera_model(self._model)
        self.initialize()
        
    # --------------------------------------------------------------------------
    # Camera operations
    # --------------------------------------------------------------------------
    
    def take_picture(self, save_path: str = None) -> bool:
        """Take a picture with the connected camera.
        
        Args:
            save_path: Optional path to save the photo.
        
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        if save_path is not None:
            return self._model.take_picture(save_path)
        else:
            return self._model.take_picture()
        
    def press_shutter_halfway(self) -> bool:
        """Press the shutter button halfway (for focusing).
        
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        return self._model.press_shutter_button(edsdk_bindings.EdsCameraCommand.SHUTTER_BUTTON_HALFWAY)
        
    def press_shutter_completely(self) -> bool:
        """Press the shutter button completely (to take a picture).
        
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        return self._model.press_shutter_button(edsdk_bindings.EdsCameraCommand.SHUTTER_BUTTON_COMPLETELY)
        
    def release_shutter(self) -> bool:
        """Release the shutter button.
        
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        return self._model.press_shutter_button(edsdk_bindings.EdsCameraCommand.SHUTTER_BUTTON_OFF)
        
    # --------------------------------------------------------------------------
    # Live View (EVF) methods
    # --------------------------------------------------------------------------
    
    def start_live_view(self) -> bool:
        """Start the camera's live view (EVF) mode.
        
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        return self._model.start_evf()
        
    def stop_live_view(self) -> bool:
        """Stop the camera's live view (EVF) mode.
        
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        return self._model.end_evf()
        
    def download_live_view_frame(self) -> Any:
        """Download the current live view frame.
        
        Returns:
            Live view image data.
        """
        self._ensure_connected()
        return self._model.download_evf()
        
    def set_evf_zoom(self, zoom: int) -> None:
        """Set the live view zoom level.
        
        Args:
            zoom: Zoom level value.
        """
        self._ensure_connected()
        self._model.set_evf_zoom(zoom)
        
    def set_evf_zoom_position(self, x: int, y: int) -> None:
        """Set the live view zoom position.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
        """
        self._ensure_connected()
        point = edsdk_bindings.EdsPoint()
        point.x = x
        point.y = y
        self._model.set_evf_zoom_position(point)
        
    def set_evf_af_mode(self, af_mode: int) -> None:
        """Set the live view autofocus mode.
        
        Args:
            af_mode: Autofocus mode value.
        """
        self._ensure_connected()
        self._model.set_evf_af_mode(af_mode)
        
    def focus_near(self, level: int = 3) -> bool:
        """Focus the lens to a nearer distance.
        
        Args:
            level: Focus adjustment level (1-3), where 3 is the largest step.
            
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        if level == 3:
            drive_lens = edsdk_bindings.EdsEvfDriveLens.NEAR_3
        elif level == 2:
            drive_lens = edsdk_bindings.EdsEvfDriveLens.NEAR_2
        else:
            drive_lens = edsdk_bindings.EdsEvfDriveLens.NEAR_1
            
        cmd = edsdk_bindings.DriveLensCommand(self._model.get_camera_object(), drive_lens)
        return cmd.execute()
        
    def focus_far(self, level: int = 3) -> bool:
        """Focus the lens to a farther distance.
        
        Args:
            level: Focus adjustment level (1-3), where 3 is the largest step.
            
        Returns:
            True if successful, False otherwise.
        """
        self._ensure_connected()
        if level == 3:
            drive_lens = edsdk_bindings.EdsEvfDriveLens.FAR_3
        elif level == 2:
            drive_lens = edsdk_bindings.EdsEvfDriveLens.FAR_2
        else:
            drive_lens = edsdk_bindings.EdsEvfDriveLens.FAR_1
            
        cmd = edsdk_bindings.DriveLensCommand(self._model.get_camera_object(), drive_lens)
        return cmd.execute()
        
    # --------------------------------------------------------------------------
    # Camera settings methods
    # --------------------------------------------------------------------------
    
    def get_model_name(self) -> str:
        """Get the camera model name.
        
        Returns:
            Camera model name as a string.
        """
        self._ensure_connected()
        return self._model.get_model_name()
        
    def get_iso(self) -> int:
        """Get the current ISO value.
        
        Returns:
            ISO value.
        """
        self._ensure_connected()
        return self._model.get_iso()
        
    def set_iso(self, iso: int) -> None:
        """Set the ISO value.
        
        Args:
            iso: ISO value to set.
        """
        self._ensure_connected()
        self._model.set_iso(iso)
        
    def get_iso_label(self, iso: int) -> str:
        """Get the human-readable label for an ISO value.
        
        Args:
            iso: ISO value.
            
        Returns:
            Human-readable ISO label.
        """
        return edsdk_bindings.Iso.get_label(iso)
        
    def get_aperture(self) -> int:
        """Get the current aperture value.
        
        Returns:
            Aperture value.
        """
        self._ensure_connected()
        return self._model.get_av()
        
    def set_aperture(self, aperture: int) -> None:
        """Set the aperture value.
        
        Args:
            aperture: Aperture value to set.
        """
        self._ensure_connected()
        self._model.set_av(aperture)
        
    def get_aperture_label(self, aperture: int) -> str:
        """Get the human-readable label for an aperture value.
        
        Args:
            aperture: Aperture value.
            
        Returns:
            Human-readable aperture label (e.g., "f/2.8").
        """
        return edsdk_bindings.Av.get_label(aperture)
        
    def get_shutter_speed(self) -> int:
        """Get the current shutter speed value.
        
        Returns:
            Shutter speed value.
        """
        self._ensure_connected()
        return self._model.get_tv()
        
    def set_shutter_speed(self, shutter_speed: int) -> None:
        """Set the shutter speed value.
        
        Args:
            shutter_speed: Shutter speed value to set.
        """
        self._ensure_connected()
        self._model.set_tv(shutter_speed)
        
    def get_shutter_speed_label(self, shutter_speed: int) -> str:
        """Get the human-readable label for a shutter speed value.
        
        Args:
            shutter_speed: Shutter speed value.
            
        Returns:
            Human-readable shutter speed label (e.g., "1/250").
        """
        return edsdk_bindings.Tv.get_label(shutter_speed)
        
    def get_ae_mode(self) -> int:
        """Get the current AE (Auto Exposure) mode.
        
        Returns:
            AE mode value.
        """
        self._ensure_connected()
        return self._model.get_ae_mode()
        
    def set_ae_mode(self, ae_mode: int) -> None:
        """Set the AE (Auto Exposure) mode.
        
        Args:
            ae_mode: AE mode value to set.
        """
        self._ensure_connected()
        self._model.set_ae_mode(ae_mode)
        
    def get_ae_mode_label(self, ae_mode: int) -> str:
        """Get the human-readable label for an AE mode value.
        
        Args:
            ae_mode: AE mode value.
            
        Returns:
            Human-readable AE mode label (e.g., "Manual", "Aperture Priority").
        """
        return edsdk_bindings.AEMode.get_label(ae_mode)
        
    def get_metering_mode(self) -> int:
        """Get the current metering mode.
        
        Returns:
            Metering mode value.
        """
        self._ensure_connected()
        return self._model.get_metering_mode()
        
    def set_metering_mode(self, metering_mode: int) -> None:
        """Set the metering mode.
        
        Args:
            metering_mode: Metering mode value to set.
        """
        self._ensure_connected()
        self._model.set_metering_mode(metering_mode)
        
    def get_metering_mode_label(self, metering_mode: int) -> str:
        """Get the human-readable label for a metering mode value.
        
        Args:
            metering_mode: Metering mode value.
            
        Returns:
            Human-readable metering mode label.
        """
        return edsdk_bindings.MeteringMode.get_label(metering_mode)
        
    def get_exposure_compensation(self) -> int:
        """Get the current exposure compensation value.
        
        Returns:
            Exposure compensation value.
        """
        self._ensure_connected()
        return self._model.get_exposure_compensation()
        
    def set_exposure_compensation(self, exposure_comp: int) -> None:
        """Set the exposure compensation value.
        
        Args:
            exposure_comp: Exposure compensation value to set.
        """
        self._ensure_connected()
        self._model.set_exposure_compensation(exposure_comp)
        
    def get_exposure_compensation_label(self, exposure_comp: int) -> str:
        """Get the human-readable label for an exposure compensation value.
        
        Args:
            exposure_comp: Exposure compensation value.
            
        Returns:
            Human-readable exposure compensation label.
        """
        return edsdk_bindings.ExposureComp.get_label(exposure_comp)
        
    def get_image_quality(self) -> int:
        """Get the current image quality setting.
        
        Returns:
            Image quality value.
        """
        self._ensure_connected()
        return self._model.get_image_quality()
        
    def set_image_quality(self, image_quality: int) -> None:
        """Set the image quality.
        
        Args:
            image_quality: Image quality value to set.
        """
        self._ensure_connected()
        self._model.set_image_quality(image_quality)
        
    def get_image_quality_label(self, image_quality: int) -> str:
        """Get the human-readable label for an image quality value.
        
        Args:
            image_quality: Image quality value.
            
        Returns:
            Human-readable image quality label.
        """
        return edsdk_bindings.ImageQuality.get_label(image_quality)
        
    # --------------------------------------------------------------------------
    # Utility methods
    # --------------------------------------------------------------------------
    
    def _ensure_connected(self):
        """Ensure the camera is connected before performing operations."""
        if not self._initialized or self._model is None:
            raise RuntimeError("Camera not connected. Call connect_to_camera() first.")
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit.
        
        Ensures the session is closed properly.
        """
        if self._initialized:
            # Gracefully close the session
            pass 