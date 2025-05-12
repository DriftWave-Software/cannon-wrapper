"""
Core module for the Canon EDSDK wrapper.

This module contains the core functionality for interfacing with the EDSDK library.
"""

# Make all utility functions available from core
from ..utils import *

# Re-export the error checking function
from ..exceptions import CanonError 