"""
Utility functions for the Canon EDSDK Python wrapper.
"""

import os
import platform
import ctypes
import logging
from typing import List, Dict, Any, Optional, Tuple, Union, Callable

try:
    from . import edsdk_bindings
    from .exceptions import CanonError
except ImportError:
    # Allow importing this file even if bindings aren't available
    edsdk_bindings = None
    CanonError = Exception


# Configure logger
logger = logging.getLogger("cannon_wrapper")


def setup_logger(level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Set up the logger for the Canon wrapper.
    
    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
        log_file: Optional path to a log file
    
    Returns:
        Configured logger instance
    """
    logger.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Add file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def check_errors(error_code: int, operation_name: str = "operation") -> None:
    """Check EDSDK error code and raise appropriate exception if needed.
    
    Args:
        error_code: EDSDK error code
        operation_name: Name of the operation for error messages
        
    Raises:
        CanonError: If the error code indicates an error
    """
    if not edsdk_bindings:
        if error_code != 0:  # Assume 0 is success
            raise CanonError(f"Error performing {operation_name}: code {error_code}")
        return
        
    if error_code != edsdk_bindings.EdsError.OK:
        raise CanonError.from_edsdk_error(
            error_code, f"Error performing {operation_name}: {CanonError.get_error_message(error_code)}"
        )


def iso_value_to_string(iso_value: int) -> str:
    """Convert ISO numeric value to human-readable string.
    
    Args:
        iso_value: ISO value code
    
    Returns:
        Human-readable ISO string
    """
    if not edsdk_bindings:
        return f"ISO {iso_value}"
    
    return edsdk_bindings.Iso.get_label(iso_value)


def aperture_value_to_string(av_value: int) -> str:
    """Convert aperture numeric value to human-readable string.
    
    Args:
        av_value: Aperture value code
    
    Returns:
        Human-readable aperture string (e.g., "f/2.8")
    """
    if not edsdk_bindings:
        return f"f/{av_value}"
    
    return edsdk_bindings.Av.get_label(av_value)


def shutter_value_to_string(tv_value: int) -> str:
    """Convert shutter speed numeric value to human-readable string.
    
    Args:
        tv_value: Shutter speed value code
    
    Returns:
        Human-readable shutter speed string (e.g., "1/125")
    """
    if not edsdk_bindings:
        return f"TV {tv_value}"
    
    return edsdk_bindings.Tv.get_label(tv_value)


def find_edsdk_dll() -> Optional[str]:
    """Find the EDSDK DLL/SO/DYLIB path based on the operating system.
    
    Returns:
        Path to the EDSDK library if found, None otherwise
    """
    system = platform.system()
    
    # Define common locations for EDSDK libraries
    if system == "Windows":
        paths_to_check = [
            # Check new lib directories first
            os.path.abspath(os.path.join(os.path.dirname(__file__), "lib", "EDSDK")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "lib", "EDSDK_64")),
            # Default installation paths
            os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "Canon", "EOS Utility", "EDSDK"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "Canon", "EOS Utility", "EDSDK"),
            # Legacy paths
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "EDSDK")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "edsdk")),
        ]
        dll_name = "EDSDK.dll"
    elif system == "Darwin":  # macOS
        paths_to_check = [
            # Check new lib directory first
            os.path.abspath(os.path.join(os.path.dirname(__file__), "lib", "EDSDK.framework")),
            # Default paths
            "/Library/Frameworks/EDSDK.framework",
            os.path.expanduser("~/Library/Frameworks/EDSDK.framework"),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "EDSDK.framework")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "edsdk")),
        ]
        dll_name = "EDSDK"
    else:  # Linux
        paths_to_check = [
            # Check new lib directory first
            os.path.abspath(os.path.join(os.path.dirname(__file__), "lib", "edsdk")),
            # Default paths
            "/usr/lib",
            "/usr/local/lib",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "edsdk")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "edsdk")),
        ]
        dll_name = "libedsdk.so"
    
    # Check each path
    for path in paths_to_check:
        if system == "Darwin" and os.path.isdir(path):  # macOS framework
            return path
        
        full_path = os.path.join(path, dll_name)
        if os.path.exists(full_path):
            return full_path
    
    return None


def load_edsdk_library() -> Optional[object]:
    """Attempt to load the EDSDK library using ctypes.
    
    Returns:
        Loaded EDSDK library object if successful, None otherwise
    """
    dll_path = find_edsdk_dll()
    if not dll_path:
        logger.error("EDSDK library not found")
        return None
    
    try:
        if platform.system() == "Darwin":  # macOS
            return ctypes.cdll.LoadLibrary(os.path.join(dll_path, "EDSDK"))
        else:
            return ctypes.cdll.LoadLibrary(dll_path)
    except (OSError, ImportError) as e:
        logger.error(f"Failed to load EDSDK library: {e}")
        return None


def safe_release(eds_object) -> None:
    """Safely release an EDSDK object.
    
    Args:
        eds_object: EDSDK object to release
    """
    if not eds_object:
        return
        
    try:
        if hasattr(eds_object, 'release'):
            eds_object.release()
    except Exception as e:
        logger.warning(f"Error releasing EDSDK object: {e}")


def create_save_directory(base_dir: str, camera_name: Optional[str] = None) -> str:
    """Create a directory for saving images.
    
    Args:
        base_dir: Base directory for saving images
        camera_name: Optional camera name to include in the directory name
    
    Returns:
        Path to the created directory
    """
    import datetime
    
    # Create base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Create subdirectory with timestamp and camera name if provided
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if camera_name:
        # Remove invalid characters from camera name
        camera_name = ''.join(c for c in camera_name if c.isalnum() or c in '- _')
        subdir_name = f"{timestamp}_{camera_name}"
    else:
        subdir_name = timestamp
    
    save_dir = os.path.join(base_dir, subdir_name)
    os.makedirs(save_dir, exist_ok=True)
    
    return save_dir


def is_valid_property_id(property_id: int) -> bool:
    """Check if a property ID is valid for Canon EDSDK.
    
    Args:
        property_id: EDSDK property ID to check
        
    Returns:
        True if the property ID is valid, False otherwise
    """
    if not edsdk_bindings:
        return True  # Can't validate without bindings
    
    # Get all property IDs from the EdsPropertyID enum
    valid_ids = []
    if hasattr(edsdk_bindings, 'EdsPropertyID'):
        for attr_name in dir(edsdk_bindings.EdsPropertyID):
            if not attr_name.startswith('_'):
                valid_ids.append(getattr(edsdk_bindings.EdsPropertyID, attr_name))
    
    return property_id in valid_ids 