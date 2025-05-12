"""
Live View Manager Module
Handles live view operations from the camera.
"""

import logging
import time
from typing import Optional, Any, Callable
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QMutex, QWaitCondition

# Try to import OpenCV for advanced image processing (optional)
try:
    import cv2
    _has_cv2 = True
except ImportError:
    _has_cv2 = False

logger = logging.getLogger("canon_gui.live_view")

class LiveViewThread(QThread):
    """Thread for handling live view streaming from the camera."""
    
    # Signal emitted when a new frame is available
    frame_ready = pyqtSignal(object)  # Numpy array
    error = pyqtSignal(str)  # Error message
    
    def __init__(self, camera, parent=None):
        """Initialize the live view thread.
        
        Args:
            camera: Canon camera object
            parent: Parent object
        """
        super().__init__(parent)
        self._camera = camera
        self._running = False
        self._mutex = QMutex()
        self._condition = QWaitCondition()
        self._frame_interval = 0.1  # 10 fps by default
    
    def run(self):
        """Thread execution function."""
        self._running = True
        
        while self._running:
            try:
                # Acquire the live view frame
                frame = self._camera.download_live_view_frame()
                
                if frame is not None:
                    # Convert to NumPy array if needed
                    if not isinstance(frame, np.ndarray):
                        # This depends on how the frame is returned from the camera
                        # You might need to adjust based on the actual implementation
                        frame_data = np.array(frame)
                    else:
                        frame_data = frame
                    
                    # Emit the frame
                    self.frame_ready.emit(frame_data)
                
                # Sleep for the frame interval
                time.sleep(self._frame_interval)
                
            except Exception as e:
                logger.error(f"Error in live view thread: {str(e)}")
                self.error.emit(f"Live view error: {str(e)}")
                # Add a small delay to avoid spamming errors
                time.sleep(0.5)
        
        logger.debug("Live view thread stopped")
    
    def stop(self):
        """Stop the live view thread."""
        self._mutex.lock()
        self._running = False
        self._mutex.unlock()
        self.wait()  # Wait for the thread to finish
    
    def set_frame_rate(self, fps: float):
        """Set the frame rate.
        
        Args:
            fps: Frames per second
        """
        if fps <= 0:
            fps = 1.0
        self._frame_interval = 1.0 / fps


class LiveViewManager(QObject):
    """Manager class for camera live view."""
    
    # Define signals
    live_view_started = pyqtSignal()
    live_view_stopped = pyqtSignal()
    frame_available = pyqtSignal(object)  # Numpy array
    error = pyqtSignal(str)  # Error message
    
    def __init__(self, camera_manager):
        """Initialize the live view manager.
        
        Args:
            camera_manager: Camera manager instance
        """
        super().__init__()
        self._camera_manager = camera_manager
        self._live_view_thread = None
        self._is_active = False
        
        # Connect to camera manager signals
        self._camera_manager.camera_disconnected.connect(self.stop_live_view)
    
    def start_live_view(self, fps: float = 10.0) -> bool:
        """Start the live view.
        
        Args:
            fps: Frames per second (default: 10.0)
        
        Returns:
            True if started successfully, False otherwise
        """
        if self._is_active:
            return True
            
        camera = self._camera_manager.get_camera()
        if not camera:
            self.error.emit("Cannot start live view: No camera connected")
            return False
            
        try:
            # Activate live view on the camera
            camera.start_live_view()
            
            # Create and start the live view thread
            self._live_view_thread = LiveViewThread(camera)
            self._live_view_thread.frame_ready.connect(self.frame_available)
            self._live_view_thread.error.connect(self.error)
            self._live_view_thread.set_frame_rate(fps)
            self._live_view_thread.start()
            
            self._is_active = True
            self.live_view_started.emit()
            return True
            
        except Exception as e:
            logger.error(f"Error starting live view: {str(e)}")
            self.error.emit(f"Error starting live view: {str(e)}")
            return False
    
    def stop_live_view(self) -> bool:
        """Stop the live view.
        
        Returns:
            True if stopped successfully, False otherwise
        """
        if not self._is_active:
            return True
            
        try:
            # Stop the live view thread
            if self._live_view_thread:
                self._live_view_thread.stop()
                self._live_view_thread = None
            
            # Deactivate live view on the camera
            camera = self._camera_manager.get_camera()
            if camera:
                camera.stop_live_view()
            
            self._is_active = False
            self.live_view_stopped.emit()
            return True
            
        except Exception as e:
            logger.error(f"Error stopping live view: {str(e)}")
            self.error.emit(f"Error stopping live view: {str(e)}")
            return False
    
    def is_active(self) -> bool:
        """Check if live view is active.
        
        Returns:
            True if live view is active, False otherwise
        """
        return self._is_active
    
    def set_frame_rate(self, fps: float):
        """Set the frame rate.
        
        Args:
            fps: Frames per second
        """
        if self._live_view_thread:
            self._live_view_thread.set_frame_rate(fps)
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a live view frame.
        
        Args:
            frame: Raw frame data
        
        Returns:
            Processed frame data
        """
        # Add image processing as needed
        if _has_cv2:
            # Example: Apply a simple processing (auto-contrast)
            # This is just a placeholder - adjust based on your needs
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Apply auto-contrast/histogram equalization
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
                cl = clahe.apply(l)
                limg = cv2.merge((cl, a, b))
                frame = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
        
        return frame 