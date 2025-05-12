"""
Live view functionality for Canon cameras.

This module provides specialized classes and functions for working with
Canon camera live view (EVF).
"""

import logging
from typing import Any, Optional, Dict, List, Union, Tuple

try:
    from ..edsdk_bindings import *
    from ..exceptions import LiveViewNotActiveError, CanonError
    from ..core.image_utils import edsdkimage_to_numpy
except ImportError:
    logging.warning("Could not import EDSDK bindings or other dependencies.")

logger = logging.getLogger(__name__)


class LiveViewManager:
    """Class for managing live view operations.
    
    This class provides a more detailed interface for working with live view
    compared to the basic functions in the Canon class.
    """
    
    def __init__(self, camera_model):
        """Initialize the LiveViewManager.
        
        Args:
            camera_model: The CameraModel object from EDSDK
        """
        self._model = camera_model
        self._is_active = False
        self._zoom_level = 1
        self._zoom_position = (0, 0)  # x, y
        
    @property
    def is_active(self) -> bool:
        """Get whether live view is currently active.
        
        Returns:
            True if live view is active, False otherwise
        """
        return self._is_active
        
    def start(self) -> bool:
        """Start live view.
        
        Returns:
            True if successful, False otherwise
        """
        if self._is_active:
            return True
            
        result = self._model.start_evf()
        if result:
            self._is_active = True
        return result
        
    def stop(self) -> bool:
        """Stop live view.
        
        Returns:
            True if successful, False otherwise
        """
        if not self._is_active:
            return True
            
        result = self._model.end_evf()
        if result:
            self._is_active = False
        return result
        
    def download_frame(self) -> Any:
        """Download the current live view frame.
        
        Returns:
            Live view image data
            
        Raises:
            LiveViewNotActiveError: If live view is not active
        """
        if not self._is_active:
            raise LiveViewNotActiveError("Live view is not active")
            
        return self._model.download_evf()
        
    def set_zoom_level(self, level: int) -> bool:
        """Set the live view zoom level.
        
        Args:
            level: Zoom level (1, 5, 10, etc.)
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            LiveViewNotActiveError: If live view is not active
        """
        if not self._is_active:
            raise LiveViewNotActiveError("Live view is not active")
            
        result = self._model.set_evf_zoom(level)
        if result:
            self._zoom_level = level
        return result
        
    def set_zoom_position(self, x: int, y: int) -> bool:
        """Set the live view zoom position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            LiveViewNotActiveError: If live view is not active
        """
        if not self._is_active:
            raise LiveViewNotActiveError("Live view is not active")
            
        point = EdsPoint()
        point.x = x
        point.y = y
        
        result = self._model.set_evf_zoom_position(point)
        if result:
            self._zoom_position = (x, y)
        return result
        
    def drive_lens_near(self, step: int = 3) -> bool:
        """Drive the lens to focus nearer.
        
        Args:
            step: Focus step size (1-3)
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            LiveViewNotActiveError: If live view is not active
            ValueError: If step is invalid
        """
        if not self._is_active:
            raise LiveViewNotActiveError("Live view is not active")
            
        if step < 1 or step > 3:
            raise ValueError("Step must be 1, 2, or 3")
            
        lens_step = [
            EdsEvfDriveLens.NEAR_1,
            EdsEvfDriveLens.NEAR_2,
            EdsEvfDriveLens.NEAR_3
        ][step - 1]
        
        cmd = DriveLensCommand(self._model, lens_step)
        return cmd.execute()
        
    def drive_lens_far(self, step: int = 3) -> bool:
        """Drive the lens to focus farther.
        
        Args:
            step: Focus step size (1-3)
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            LiveViewNotActiveError: If live view is not active
            ValueError: If step is invalid
        """
        if not self._is_active:
            raise LiveViewNotActiveError("Live view is not active")
            
        if step < 1 or step > 3:
            raise ValueError("Step must be 1, 2, or 3")
            
        lens_step = [
            EdsEvfDriveLens.FAR_1,
            EdsEvfDriveLens.FAR_2,
            EdsEvfDriveLens.FAR_3
        ][step - 1]
        
        cmd = DriveLensCommand(self._model, lens_step)
        return cmd.execute()
        
    def auto_focus(self, x: int, y: int) -> bool:
        """Perform autofocus at a specific position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            LiveViewNotActiveError: If live view is not active
        """
        if not self._is_active:
            raise LiveViewNotActiveError("Live view is not active")
            
        point = EdsPoint()
        point.x = x
        point.y = y
        
        cmd = DoEvfAFCommand(self._model, point)
        return cmd.execute()
        
    def get_focus_info(self) -> Dict[str, Any]:
        """Get information about the current focus state.
        
        Returns:
            Dictionary with focus information
            
        Raises:
            LiveViewNotActiveError: If live view is not active
        """
        if not self._is_active:
            raise LiveViewNotActiveError("Live view is not active")
            
        # This would require custom implementation to extract focus info from EDSDK
        # For now, return a placeholder
        return {
            "zoom_level": self._zoom_level,
            "zoom_position": self._zoom_position,
        }
        
    def __enter__(self):
        """Context manager entry.
        
        Starts live view when entering the context.
        
        Returns:
            The LiveViewManager instance
        """
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit.
        
        Stops live view when exiting the context.
        """
        self.stop() 