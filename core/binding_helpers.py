"""
Helper functions for working with the pybind11 bindings.

This module provides utility functions for working with the EDSDK bindings
and converting between C++ and Python types.
"""

import os
import ctypes
import platform
import logging
from typing import Any, Optional, Dict, List, Union, Tuple

try:
    from ..edsdk_bindings import *
    from ..exceptions import CanonError, DeviceNotFoundError
except ImportError:
    # Allow importing this file even if bindings aren't available
    logging.warning("Could not import EDSDK bindings.")

logger = logging.getLogger(__name__)


def find_cameras() -> List[Any]:
    """Find available Canon cameras.
    
    Returns:
        List of camera references that can be used with Canon.connect_to_camera()
    
    Raises:
        DeviceNotFoundError: If no cameras are found
    """
    try:
        # Placeholder function - in a real implementation, 
        # this would use the EDSDK to list available cameras
        cameras = []
        return cameras
    except Exception as e:
        logger.error(f"Error finding cameras: {e}")
        raise DeviceNotFoundError("No Canon cameras found. Check connections.") from e


def get_first_camera() -> Any:
    """Get the first available Canon camera.
    
    Returns:
        Camera reference for the first available camera
        
    Raises:
        DeviceNotFoundError: If no camera is found
    """
    cameras = find_cameras()
    if not cameras:
        raise DeviceNotFoundError("No Canon cameras found. Check connections.")
    return cameras[0]


def setup_memory_callbacks() -> None:
    """Set up memory management callbacks for EDSDK.
    
    This function registers the memory allocation and deallocation callbacks
    required by the EDSDK.
    """
    # This would be implemented to register memory callbacks with EDSDK
    pass


def initialize_sdk() -> None:
    """Initialize the EDSDK library.
    
    This should be called once at the start of the program.
    
    Raises:
        CanonError: If initialization fails
    """
    # This would be implemented to initialize the EDSDK
    pass


def terminate_sdk() -> None:
    """Terminate the EDSDK library.
    
    This should be called once at the end of the program.
    """
    # This would be implemented to terminate the EDSDK
    pass 