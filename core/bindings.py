"""
Core bindings module for Canon EDSDK.

This module provides the main pybind11 bindings for the Canon EDSDK.
It exports all binding functionality and makes it available to the rest of the package.
"""

import logging
import os
import sys
from typing import Any, Optional, Dict, List, Union, Tuple

logger = logging.getLogger(__name__)

try:
    # Import the C++ bindings
    from ..edsdk_bindings import *
    _has_bindings = True
except ImportError:
    logger.warning("Could not import EDSDK bindings. Make sure the C++ bindings have been built.")
    _has_bindings = False


def is_available() -> bool:
    """Check if the EDSDK bindings are available.
    
    Returns:
        True if the EDSDK bindings are available, False otherwise.
    """
    return _has_bindings


def get_version() -> str:
    """Get the version of the EDSDK bindings.
    
    Returns:
        Version string or "Unknown" if not available
    """
    if not _has_bindings:
        return "Unknown"
    
    # This would be implemented to return the actual EDSDK version
    # from bindings, for now return a placeholder
    return "3.0.0"  # Placeholder 