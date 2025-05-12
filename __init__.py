"""
Canon EDSDK Python Wrapper

A Pythonic interface for controlling Canon cameras using the Canon EDSDK.
This package provides easy-to-use Python bindings for Canon's EDSDK C++ API.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple, Union, Callable

# Setup package-level logger
logging.getLogger("cannon_wrapper").addHandler(logging.NullHandler())

# Try to import the C++ bindings
try:
    from .edsdk_bindings import *
    _has_bindings = True
except ImportError:
    _has_bindings = False
    logging.warning("Could not import EDSDK bindings. Make sure the C++ bindings have been built.")

# Main camera class
from .camera import Canon

# Exception classes
from .exceptions import (
    CanonError,              # Base exception
    DeviceNotFoundError,     # Camera not found
    DeviceBusyError,         # Camera is busy
    SessionNotOpenError,     # No session is open
    CommunicationError,      # Error communicating with camera
    NotSupportedError,       # Operation not supported
    OperationCancelledError, # Operation was cancelled
    FileIOError,             # File I/O error
    MemoryError,             # Memory allocation error
    InternalError,           # Internal EDSDK error
    LiveViewNotActiveError,  # Live view not active
    CameraNotInitializedError # Camera not initialized
)

# Utility functions
from .utils import (
    # Logger setup
    setup_logger,
    
    # Error handling
    check_errors,
    
    # Value conversion
    iso_value_to_string,
    aperture_value_to_string,
    shutter_value_to_string,
    
    # EDSDK library handling
    find_edsdk_dll,
    load_edsdk_library,
    safe_release,
    
    # File operations
    create_save_directory,
    
    # Validation 
    is_valid_property_id
)

__version__ = "0.1.0"
__author__ = "Canon EDSDK Team"
__license__ = "MIT"


def is_available() -> bool:
    """Check if the EDSDK bindings are available.
    
    Returns:
        True if the EDSDK bindings are available, False otherwise.
    """
    return _has_bindings 