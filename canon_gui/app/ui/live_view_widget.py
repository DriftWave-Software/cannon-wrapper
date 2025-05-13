"""
Live View Widget
Displays the camera's live view.
"""

import logging
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QColor

logger = logging.getLogger("canon_gui.live_view")

class LiveViewWidget(QWidget):
    """Widget for displaying the camera's live view."""
    
    def __init__(self, live_view_manager, parent=None):
        """Initialize the live view widget.
        
        Args:
            live_view_manager: Live view manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self._live_view_manager = live_view_manager
        self._current_frame = None
        self._display_overlays = True
        self._zoom_level = 1
        self._focus_points = []
        
        # Set up the UI
        self._setup_ui()
        
        # Connect signals
        self._setup_connections()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Live view display label
        self._display_label = QLabel("No live view")
        self._display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._display_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._display_label.setMinimumSize(640, 480)
        
        # Set initial style
        self._display_label.setStyleSheet(
            "QLabel { background-color: #222; color: #ddd; font-size: 14pt; }"
        )
        
        layout.addWidget(self._display_label)
    
    def _setup_connections(self):
        """Set up signal/slot connections."""
        self._live_view_manager.frame_available.connect(self.update_frame)
    
    @pyqtSlot(object)
    def update_frame(self, frame):
        """Update the displayed frame.
        
        Args:
            frame: NumPy array containing the frame data
        """
        try:
            if frame is None:
                return
                
            # Store the current frame
            self._current_frame = frame
            
            # Convert the frame to QImage
            height, width = frame.shape[0], frame.shape[1]
            
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                # RGB data
                format = QImage.Format.Format_RGB888
                bytes_per_line = 3 * width
                qimage = QImage(frame.data, width, height, bytes_per_line, format)
            elif len(frame.shape) == 2:
                # Grayscale data
                format = QImage.Format.Format_Grayscale8
                bytes_per_line = width
                qimage = QImage(frame.data, width, height, bytes_per_line, format)
            else:
                # Unknown format, try anyway
                logger.warning(f"Unknown frame format: {frame.shape}")
                format = QImage.Format.Format_RGB888
                bytes_per_line = 3 * width
                qimage = QImage(frame.data, width, height, bytes_per_line, format)
            
            # Create a pixmap from the image
            pixmap = QPixmap.fromImage(qimage)
            
            # Draw overlays if enabled
            if self._display_overlays:
                pixmap = self._draw_overlays(pixmap)
            
            # Resize to fit the display
            display_size = self._display_label.size()
            pixmap = pixmap.scaled(
                display_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Update the display
            self._display_label.setPixmap(pixmap)
            
        except Exception as e:
            logger.error(f"Error updating live view frame: {str(e)}")
    
    def _draw_overlays(self, pixmap):
        """Draw overlays on the live view image.
        
        Args:
            pixmap: QPixmap to draw on
            
        Returns:
            QPixmap with overlays
        """
        try:
            # Create a copy of the pixmap to draw on
            overlay_pixmap = QPixmap(pixmap)
            
            # Create a painter
            painter = QPainter(overlay_pixmap)
            
            # Draw grid lines
            self._draw_grid_lines(painter, overlay_pixmap.width(), overlay_pixmap.height())
            
            # Draw focus points
            if self._focus_points:
                self._draw_focus_points(painter, overlay_pixmap.width(), overlay_pixmap.height())
            
            # Draw zoom indicator
            if self._zoom_level > 1:
                self._draw_zoom_indicator(painter, overlay_pixmap.width(), overlay_pixmap.height())
            
            # End painting
            painter.end()
            
            return overlay_pixmap
            
        except Exception as e:
            logger.error(f"Error drawing overlays: {str(e)}")
            return pixmap
    
    def _draw_grid_lines(self, painter, width, height):
        """Draw grid lines on the image.
        
        Args:
            painter: QPainter to draw with
            width: Image width
            height: Image height
        """
        # Set up the pen
        pen = QPen(QColor(255, 255, 255, 128))  # Semi-transparent white
        pen.setWidth(1)
        painter.setPen(pen)
        
        # Draw rule of thirds grid
        painter.drawLine(width // 3, 0, width // 3, height)
        painter.drawLine(2 * width // 3, 0, 2 * width // 3, height)
        painter.drawLine(0, height // 3, width, height // 3)
        painter.drawLine(0, 2 * height // 3, width, 2 * height // 3)
    
    def _draw_focus_points(self, painter, width, height):
        """Draw focus points on the image.
        
        Args:
            painter: QPainter to draw with
            width: Image width
            height: Image height
        """
        # Set up the pen
        pen = QPen(QColor(0, 255, 0))  # Green
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Calculate scaling factor based on original image and display size
        orig_width = self._current_frame.shape[1]
        orig_height = self._current_frame.shape[0]
        scale_x = width / orig_width
        scale_y = height / orig_height
        
        # Draw each focus point
        for point in self._focus_points:
            x, y = int(point[0] * scale_x), int(point[1] * scale_y)
            painter.drawLine(x - 10, y, x + 10, y)
            painter.drawLine(x, y - 10, x, y + 10)
    
    def _draw_zoom_indicator(self, painter, width, height):
        """Draw zoom level indicator.
        
        Args:
            painter: QPainter to draw with
            width: Image width
            height: Image height
        """
        # Set up the pen and text
        painter.setPen(QColor(255, 255, 0))  # Yellow
        painter.setFont(self.font())
        
        # Draw zoom level indicator
        zoom_text = f"{self._zoom_level}x"
        painter.drawText(10, 30, zoom_text)
    
    def set_focus_points(self, points):
        """Set focus points to display.
        
        Args:
            points: List of (x, y) tuples representing focus points
        """
        self._focus_points = points
        
        # Refresh the display if we have a current frame
        if self._current_frame is not None:
            self.update_frame(self._current_frame)
    
    def set_zoom_level(self, level):
        """Set the zoom level indicator.
        
        Args:
            level: Zoom level value
        """
        self._zoom_level = level
        
        # Refresh the display if we have a current frame
        if self._current_frame is not None:
            self.update_frame(self._current_frame)
    
    def toggle_overlays(self, enabled=None):
        """Toggle display of overlays.
        
        Args:
            enabled: If provided, sets the overlay state, otherwise toggles it
        """
        if enabled is not None:
            self._display_overlays = enabled
        else:
            self._display_overlays = not self._display_overlays
        
        # Refresh the display if we have a current frame
        if self._current_frame is not None:
            self.update_frame(self._current_frame)
    
    def clear_display(self):
        """Clear the live view display."""
        self._display_label.clear()
        self._display_label.setText("No live view")
        self._current_frame = None
        self._focus_points = []
    
    def resizeEvent(self, event):
        """Handle resize events.
        
        Args:
            event: Resize event
        """
        super().resizeEvent(event)
        
        # Refresh the display if we have a current frame
        if self._current_frame is not None:
            self.update_frame(self._current_frame) 