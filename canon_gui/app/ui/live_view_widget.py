"""
Live View Widget Module
Widget for displaying camera live view.
"""

import logging
import numpy as np
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSizePolicy, QFrame, 
    QSlider, QHBoxLayout, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QPen

logger = logging.getLogger("canon_gui.ui.live_view")

class LiveViewWidget(QWidget):
    """Widget for displaying camera live view."""
    
    def __init__(self, live_view_manager, parent=None):
        """Initialize the live view widget.
        
        Args:
            live_view_manager: Live view manager
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._live_view_manager = live_view_manager
        self._current_frame = None
        self._zoom_factor = 1.0
        self._show_focus_peaking = False
        self._show_histogram = False
        self._show_grid = False
        
        # Set up the UI
        self._setup_ui()
        
        # Connect signals
        self._setup_connections()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        
        # Live view display
        self._view_frame = QLabel()
        self._view_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._view_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self._view_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._view_frame.setMinimumSize(640, 480)
        self._view_frame.setText("No live view available")
        layout.addWidget(self._view_frame)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        
        # Zoom control
        zoom_layout = QVBoxLayout()
        zoom_layout.addWidget(QLabel("Zoom:"))
        self._zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self._zoom_slider.setRange(10, 200)  # 10% to 200%
        self._zoom_slider.setValue(100)  # 100%
        self._zoom_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._zoom_slider.setTickInterval(10)
        zoom_layout.addWidget(self._zoom_slider)
        controls_layout.addLayout(zoom_layout)
        
        # Display options
        options_layout = QVBoxLayout()
        options_layout.addWidget(QLabel("Display Options:"))
        options_hbox = QHBoxLayout()
        
        # Focus peaking button
        self._focus_peaking_btn = QPushButton("Focus Peaking")
        self._focus_peaking_btn.setCheckable(True)
        options_hbox.addWidget(self._focus_peaking_btn)
        
        # Histogram button
        self._histogram_btn = QPushButton("Histogram")
        self._histogram_btn.setCheckable(True)
        options_hbox.addWidget(self._histogram_btn)
        
        # Grid button
        self._grid_btn = QPushButton("Grid")
        self._grid_btn.setCheckable(True)
        options_hbox.addWidget(self._grid_btn)
        
        options_layout.addLayout(options_hbox)
        controls_layout.addLayout(options_layout)
        
        # Add all controls to the main layout
        layout.addLayout(controls_layout)
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Connect live view manager signals
        self._live_view_manager.frame_available.connect(self._on_frame)
        self._live_view_manager.live_view_started.connect(self._on_live_view_started)
        self._live_view_manager.live_view_stopped.connect(self._on_live_view_stopped)
        
        # Connect control signals
        self._zoom_slider.valueChanged.connect(self._on_zoom_changed)
        self._focus_peaking_btn.toggled.connect(self._on_focus_peaking_toggled)
        self._histogram_btn.toggled.connect(self._on_histogram_toggled)
        self._grid_btn.toggled.connect(self._on_grid_toggled)
    
    @pyqtSlot(object)
    def _on_frame(self, frame: np.ndarray):
        """Handle new frame from the camera.
        
        Args:
            frame: Camera frame as NumPy array or bytes
        """
        if frame is None:
            return
        
        # If frame is bytes, convert to NumPy array
        if isinstance(frame, bytes):
            try:
                # Assuming RGB format with width=640, height=480
                frame_np = np.frombuffer(frame, dtype=np.uint8).reshape(480, 640, 3)
                self._current_frame = frame_np.copy()
            except Exception as e:
                logger.error(f"Error converting bytes to array: {e}")
                return
        else:
            # Frame is already a NumPy array
            self._current_frame = frame.copy()
            
        # Process the frame (apply selected enhancements)
        processed_frame = self._process_frame(self._current_frame)
        
        # Convert the frame to QImage
        if len(processed_frame.shape) == 3 and processed_frame.shape[2] == 3:
            # RGB image
            height, width, channels = processed_frame.shape
            bytes_per_line = channels * width
            q_img = QImage(processed_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        else:
            # Grayscale image
            height, width = processed_frame.shape
            q_img = QImage(processed_frame.data, width, height, width, QImage.Format.Format_Grayscale8)
        
        # Apply zoom
        if self._zoom_factor != 1.0:
            pixmap = QPixmap.fromImage(q_img)
            scaled_width = int(width * self._zoom_factor)
            scaled_height = int(height * self._zoom_factor)
            pixmap = pixmap.scaled(scaled_width, scaled_height, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            pixmap = QPixmap.fromImage(q_img)
        
        # Apply overlays (grid, etc.)
        if self._show_grid:
            pixmap = self._add_grid_overlay(pixmap)
        
        # Update the display
        self._view_frame.setPixmap(pixmap)
    
    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a frame with selected enhancements.
        
        Args:
            frame: Raw frame
            
        Returns:
            Processed frame
        """
        # Make a copy to avoid modifying the original
        result = frame.copy()
        
        # Apply focus peaking if enabled
        if self._show_focus_peaking:
            result = self._apply_focus_peaking(result)
        
        # Apply other processing as needed
        
        return result
    
    def _apply_focus_peaking(self, frame: np.ndarray) -> np.ndarray:
        """Apply focus peaking to the frame.
        
        Args:
            frame: Input frame
            
        Returns:
            Frame with focus peaking
        """
        # This is a simple implementation using edge detection
        # For a real implementation, you might want to use more sophisticated methods
        
        try:
            import cv2
            
            # Convert to grayscale if needed
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            else:
                gray = frame.copy()
            
            # Apply Laplacian for edge detection
            edges = cv2.Laplacian(gray, cv2.CV_64F)
            
            # Normalize and threshold
            edges = np.absolute(edges)
            edges_norm = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            _, thresh = cv2.threshold(edges_norm, 50, 255, cv2.THRESH_BINARY)
            
            # Create a color overlay
            if len(frame.shape) == 3:
                result = frame.copy()
                # Add blue highlighting to edges
                result[thresh > 0, 2] = 255  # Set blue channel to max for edge pixels
                return result
            else:
                # For grayscale, convert to color first
                result = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
                result[thresh > 0, 2] = 255  # Set blue channel to max for edge pixels
                return result
                
        except ImportError:
            logger.warning("OpenCV not available for focus peaking")
            return frame
        except Exception as e:
            logger.error(f"Error applying focus peaking: {str(e)}")
            return frame
    
    def _add_grid_overlay(self, pixmap: QPixmap) -> QPixmap:
        """Add a grid overlay to the pixmap.
        
        Args:
            pixmap: Input pixmap
            
        Returns:
            Pixmap with grid overlay
        """
        # Create a copy of the pixmap to draw on
        result = QPixmap(pixmap)
        painter = QPainter(result)
        
        # Set up the pen
        pen = QPen(QColor(255, 255, 255, 128))  # Semi-transparent white
        pen.setWidth(1)
        painter.setPen(pen)
        
        # Get dimensions
        width = pixmap.width()
        height = pixmap.height()
        
        # Draw the rule of thirds grid
        h1 = height // 3
        h2 = h1 * 2
        w1 = width // 3
        w2 = w1 * 2
        
        # Draw horizontal lines
        painter.drawLine(0, h1, width, h1)
        painter.drawLine(0, h2, width, h2)
        
        # Draw vertical lines
        painter.drawLine(w1, 0, w1, height)
        painter.drawLine(w2, 0, w2, height)
        
        # Finish painting
        painter.end()
        
        return result
    
    def _on_live_view_started(self):
        """Handle live view started event."""
        # Clear any previous message
        self._view_frame.clear()
    
    def _on_live_view_stopped(self):
        """Handle live view stopped event."""
        self._view_frame.setText("Live view stopped")
        self._view_frame.setPixmap(QPixmap())  # Clear any pixmap
    
    def _on_zoom_changed(self, value: int):
        """Handle zoom slider value changed.
        
        Args:
            value: New zoom value (10-200)
        """
        self._zoom_factor = value / 100.0
        # If we have a current frame, update the display
        if self._current_frame is not None:
            self._on_frame(self._current_frame)
    
    def _on_focus_peaking_toggled(self, checked: bool):
        """Handle focus peaking button toggled.
        
        Args:
            checked: Whether the button is checked
        """
        self._show_focus_peaking = checked
        # If we have a current frame, update the display
        if self._current_frame is not None:
            self._on_frame(self._current_frame)
    
    def _on_histogram_toggled(self, checked: bool):
        """Handle histogram button toggled.
        
        Args:
            checked: Whether the button is checked
        """
        self._show_histogram = checked
        # TODO: Implement histogram display
    
    def _on_grid_toggled(self, checked: bool):
        """Handle grid button toggled.
        
        Args:
            checked: Whether the button is checked
        """
        self._show_grid = checked
        # If we have a current frame, update the display
        if self._current_frame is not None:
            self._on_frame(self._current_frame)
    
    def sizeHint(self) -> QSize:
        """Get the recommended size for the widget.
        
        Returns:
            Recommended size
        """
        return QSize(800, 600) 