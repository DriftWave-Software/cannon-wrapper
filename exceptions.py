"""
Exceptions for the Canon EDSDK Python wrapper.
"""

from typing import Dict, Optional, Any

try:
    from . import edsdk_bindings
except ImportError:
    # Allow importing this file even if bindings aren't available
    edsdk_bindings = None


class CanonError(Exception):
    """Base exception for all Canon camera errors."""
    
    def __init__(self, message: str, error_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        """Initialize a Canon error.
        
        Args:
            message: Error message.
            error_code: Optional EDSDK error code.
            details: Optional additional error details.
        """
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)
        
    @classmethod
    def from_edsdk_error(cls, error_code: int, message: Optional[str] = None):
        """Create an appropriate exception based on an EDSDK error code.
        
        Args:
            error_code: EDSDK error code.
            message: Optional custom message.
            
        Returns:
            An instance of the appropriate CanonError subclass.
        """
        if not edsdk_bindings:
            return cls(f"EDSDK error code: {error_code}", error_code)
            
        # Map EDSDK error codes to specific exception classes
        error_map = {
            edsdk_bindings.EdsError.DEVICE_NOT_FOUND: DeviceNotFoundError,
            edsdk_bindings.EdsError.DEVICE_BUSY: DeviceBusyError,
            edsdk_bindings.EdsError.SESSION_NOT_OPEN: SessionNotOpenError,
            edsdk_bindings.EdsError.COMMUNICATION_ERROR: CommunicationError,
            edsdk_bindings.EdsError.FILE_IO_ERROR: FileIOError,
            edsdk_bindings.EdsError.INTERNAL_ERROR: InternalError,
            edsdk_bindings.EdsError.MEM_ALLOC_FAILED: MemoryError,
            edsdk_bindings.EdsError.NOT_SUPPORTED: NotSupportedError,
            edsdk_bindings.EdsError.OPERATION_CANCELLED: OperationCancelledError,
        }
        
        exception_class = error_map.get(error_code, cls)
        
        # Use a default message based on error code if none provided
        if message is None:
            message = cls.get_error_message(error_code)
            
        return exception_class(message, error_code)
        
    @staticmethod
    def get_error_message(error_code: int) -> str:
        """Get a human-readable error message for an EDSDK error code.
        
        Args:
            error_code: EDSDK error code.
            
        Returns:
            Human-readable error message.
        """
        if not edsdk_bindings:
            return f"EDSDK error code: {error_code}"
            
        error_messages = {
            edsdk_bindings.EdsError.OK: "No error",
            edsdk_bindings.EdsError.UNIMPLEMENTED: "Not implemented",
            edsdk_bindings.EdsError.INTERNAL_ERROR: "Internal error",
            edsdk_bindings.EdsError.MEM_ALLOC_FAILED: "Memory allocation failed",
            edsdk_bindings.EdsError.MEM_FREE_FAILED: "Memory free failed",
            edsdk_bindings.EdsError.OPERATION_CANCELLED: "Operation cancelled",
            edsdk_bindings.EdsError.INCOMPATIBLE_VERSION: "Incompatible version",
            edsdk_bindings.EdsError.NOT_SUPPORTED: "Operation not supported",
            edsdk_bindings.EdsError.UNEXPECTED_EXCEPTION: "Unexpected exception occurred",
            edsdk_bindings.EdsError.PROTECTION_VIOLATION: "Protection violation",
            edsdk_bindings.EdsError.FILE_IO_ERROR: "File I/O error",
            edsdk_bindings.EdsError.DEVICE_NOT_FOUND: "Device not found",
            edsdk_bindings.EdsError.DEVICE_BUSY: "Device busy",
            edsdk_bindings.EdsError.DEVICE_INVALID: "Invalid device",
            edsdk_bindings.EdsError.COMMUNICATION_ERROR: "Communication error",
            edsdk_bindings.EdsError.SESSION_NOT_OPEN: "Session not open",
        }
        
        return error_messages.get(error_code, f"Unknown error code: {error_code}")


class DeviceNotFoundError(CanonError):
    """Raised when a camera device is not found."""
    pass


class DeviceBusyError(CanonError):
    """Raised when the camera device is busy."""
    pass


class SessionNotOpenError(CanonError):
    """Raised when an operation is attempted but no session is open."""
    pass


class CommunicationError(CanonError):
    """Raised when there is an error communicating with the camera."""
    pass


class NotSupportedError(CanonError):
    """Raised when an operation is not supported by the camera."""
    pass


class OperationCancelledError(CanonError):
    """Raised when an operation is cancelled."""
    pass


class FileIOError(CanonError):
    """Raised when there is an error with file I/O operations."""
    pass


class MemoryError(CanonError):
    """Raised when there is a memory allocation error."""
    pass


class InternalError(CanonError):
    """Raised when there is an internal EDSDK error."""
    pass


class LiveViewNotActiveError(CanonError):
    """Raised when attempting to use live view features when live view is not active."""
    pass


class CameraNotInitializedError(CanonError):
    """Raised when attempting to use camera features when the camera is not initialized."""
    
    def __init__(self, message: str = None):
        """Initialize with a default message if none provided."""
        super().__init__(message or "Camera not initialized. Call connect_to_camera() first.") 