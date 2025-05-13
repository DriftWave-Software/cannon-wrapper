"""
Main Window Module
The main application window for the Canon Camera Control GUI.
"""

import os
import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStatusBar, QToolBar, QDockWidget, QMessageBox, QSplitter, QApplication
)
from PyQt6.QtCore import Qt, QSize, QSettings
from PyQt6.QtGui import QIcon, QAction

from app.camera.camera_manager import CameraManager
from app.camera.live_view import LiveViewManager
from app.camera.settings import CameraSettings
from app.ui.live_view_widget import LiveViewWidget
from app.ui.control_panel import ControlPanel
from app.ui.settings_dialog import SettingsDialog

logger = logging.getLogger("canon_gui.ui")

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Set up the window
        self.setWindowTitle("Canon Camera Control")
        self.setMinimumSize(1024, 768)
        
        # Initialize settings
        self._settings = QSettings("CanonControl", "CanonGUI")
        
        # Initialize camera components
        self._camera_manager = CameraManager()
        self._live_view_manager = LiveViewManager(self._camera_manager)
        self._camera_settings = CameraSettings(self._camera_manager)
        
        # Set up the UI
        self._setup_ui()
        self._setup_connections()
        
        # Restore window settings
        self._restore_window_state()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Create central widget
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(self._central_widget)
        
        # Create splitter for main panels
        self._main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self._main_splitter)
        
        # Add live view panel
        self._live_view_widget = LiveViewWidget(self._live_view_manager)
        self._main_splitter.addWidget(self._live_view_widget)
        
        # Add control panel
        self._control_panel = ControlPanel(self._camera_manager, self._live_view_manager, self._camera_settings)
        self._main_splitter.addWidget(self._control_panel)
        
        # Set initial splitter sizes
        self._main_splitter.setSizes([700, 300])
        
        # Status bar
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        
        # Camera status label
        self._camera_status_label = QLabel("Camera: Not connected")
        self._status_bar.addPermanentWidget(self._camera_status_label)
        
        # Create toolbar
        self._setup_toolbar()
        
        # Create menu
        self._setup_menu()
    
    def _setup_toolbar(self):
        """Set up the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setObjectName("mainToolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        
        # Connect camera action
        self._connect_action = QAction("Connect", self)
        self._connect_action.setStatusTip("Connect to camera")
        self._connect_action.triggered.connect(self._on_connect_camera)
        toolbar.addAction(self._connect_action)
        
        # Disconnect camera action
        self._disconnect_action = QAction("Disconnect", self)
        self._disconnect_action.setStatusTip("Disconnect from camera")
        self._disconnect_action.setEnabled(False)
        self._disconnect_action.triggered.connect(self._on_disconnect_camera)
        toolbar.addAction(self._disconnect_action)
        
        toolbar.addSeparator()
        
        # Live view actions
        self._start_live_view_action = QAction("Start Live View", self)
        self._start_live_view_action.setStatusTip("Start camera live view")
        self._start_live_view_action.setEnabled(False)
        self._start_live_view_action.triggered.connect(self._on_start_live_view)
        toolbar.addAction(self._start_live_view_action)
        
        self._stop_live_view_action = QAction("Stop Live View", self)
        self._stop_live_view_action.setStatusTip("Stop camera live view")
        self._stop_live_view_action.setEnabled(False)
        self._stop_live_view_action.triggered.connect(self._on_stop_live_view)
        toolbar.addAction(self._stop_live_view_action)
        
        toolbar.addSeparator()
        
        # Capture actions
        self._capture_action = QAction("Capture", self)
        self._capture_action.setStatusTip("Take a photo")
        self._capture_action.setEnabled(False)
        self._capture_action.triggered.connect(self._on_capture)
        toolbar.addAction(self._capture_action)
        
        self._record_action = QAction("Record", self)
        self._record_action.setStatusTip("Start/stop video recording")
        self._record_action.setEnabled(False)
        self._record_action.triggered.connect(self._on_record)
        toolbar.addAction(self._record_action)
    
    def _setup_menu(self):
        """Set up the menu bar."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        # Connect/disconnect actions
        file_menu.addAction(self._connect_action)
        file_menu.addAction(self._disconnect_action)
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Camera menu
        camera_menu = self.menuBar().addMenu("&Camera")
        camera_menu.addAction(self._start_live_view_action)
        camera_menu.addAction(self._stop_live_view_action)
        camera_menu.addSeparator()
        camera_menu.addAction(self._capture_action)
        camera_menu.addAction(self._record_action)
        
        # Settings menu
        settings_menu = self.menuBar().addMenu("&Settings")
        
        # Camera settings action
        camera_settings_action = QAction("Camera Settings", self)
        camera_settings_action.setStatusTip("Configure camera settings")
        camera_settings_action.triggered.connect(self._on_camera_settings)
        settings_menu.addAction(camera_settings_action)
        
        # Application settings action
        app_settings_action = QAction("Application Settings", self)
        app_settings_action.setStatusTip("Configure application settings")
        app_settings_action.triggered.connect(self._on_app_settings)
        settings_menu.addAction(app_settings_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.setStatusTip("About Canon Camera Control")
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)
    
    def _setup_connections(self):
        """Set up signal/slot connections."""
        # Camera manager signals
        self._camera_manager.camera_connected.connect(self._on_camera_connected)
        self._camera_manager.camera_disconnected.connect(self._on_camera_disconnected)
        self._camera_manager.camera_error.connect(self._on_camera_error)
        self._camera_manager.status_changed.connect(self._on_status_changed)
        
        # Live view manager signals
        self._live_view_manager.live_view_started.connect(self._on_live_view_started)
        self._live_view_manager.live_view_stopped.connect(self._on_live_view_stopped)
        self._live_view_manager.error.connect(self._on_live_view_error)
    
    def _restore_window_state(self):
        """Restore the window state from settings."""
        if self._settings.contains("MainWindow/geometry"):
            self.restoreGeometry(self._settings.value("MainWindow/geometry"))
        if self._settings.contains("MainWindow/state"):
            self.restoreState(self._settings.value("MainWindow/state"))
        if self._settings.contains("MainWindow/splitterSizes"):
            self._main_splitter.restoreState(self._settings.value("MainWindow/splitterSizes"))
    
    def _on_connect_camera(self):
        """Handle camera connection."""
        self._status_bar.showMessage("Connecting to camera...")
        self._camera_manager.connect_camera()
    
    def _on_disconnect_camera(self):
        """Handle camera disconnection."""
        self._status_bar.showMessage("Disconnecting from camera...")
        self._camera_manager.disconnect_camera()
    
    def _on_camera_connected(self, camera_model: str):
        """Handle camera connected signal.
        
        Args:
            camera_model: Camera model name
        """
        self._camera_status_label.setText(f"Camera: {camera_model}")
        
        # Update UI state
        self._connect_action.setEnabled(False)
        self._disconnect_action.setEnabled(True)
        self._start_live_view_action.setEnabled(True)
        self._capture_action.setEnabled(True)
        
        # Enable video recording based on camera capabilities
        camera = self._camera_manager.get_camera()
        if camera and hasattr(camera, "can_record_video") and camera.can_record_video():
            self._record_action.setEnabled(True)
        else:
            self._record_action.setEnabled(False)
    
    def _on_camera_disconnected(self):
        """Handle camera disconnected signal."""
        self._camera_status_label.setText("Camera: Not connected")
        
        # Update UI state
        self._connect_action.setEnabled(True)
        self._disconnect_action.setEnabled(False)
        self._start_live_view_action.setEnabled(False)
        self._stop_live_view_action.setEnabled(False)
        self._capture_action.setEnabled(False)
        self._record_action.setEnabled(False)
    
    def _on_camera_error(self, error_message: str):
        """Handle camera error signal.
        
        Args:
            error_message: Error message
        """
        QMessageBox.critical(self, "Camera Error", error_message)
    
    def _on_status_changed(self, status_message: str):
        """Handle status changed signal.
        
        Args:
            status_message: Status message
        """
        self._status_bar.showMessage(status_message, 5000)  # Show for 5 seconds
    
    def _on_start_live_view(self):
        """Handle start live view action."""
        self._status_bar.showMessage("Starting live view...")
        self._live_view_manager.start_live_view()
    
    def _on_stop_live_view(self):
        """Handle stop live view action."""
        self._status_bar.showMessage("Stopping live view...")
        self._live_view_manager.stop_live_view()
    
    def _on_live_view_started(self):
        """Handle live view started signal."""
        self._start_live_view_action.setEnabled(False)
        self._stop_live_view_action.setEnabled(True)
    
    def _on_live_view_stopped(self):
        """Handle live view stopped signal."""
        self._start_live_view_action.setEnabled(True)
        self._stop_live_view_action.setEnabled(False)
    
    def _on_live_view_error(self, error_message: str):
        """Handle live view error signal.
        
        Args:
            error_message: Error message
        """
        QMessageBox.warning(self, "Live View Error", error_message)
    
    def _on_capture(self):
        """Handle capture action."""
        camera = self._camera_manager.get_camera()
        if not camera:
            return
            
        try:
            self._status_bar.showMessage("Taking photo...")
            # You'd need to implement this to choose a save path
            save_path = os.path.join(os.path.expanduser("~"), "Pictures", "CanonControl")
            camera.take_picture(save_path)
            self._status_bar.showMessage("Photo taken", 3000)
        except Exception as e:
            logger.error(f"Error taking photo: {str(e)}")
            QMessageBox.warning(self, "Capture Error", f"Error taking photo: {str(e)}")
    
    def _on_record(self):
        """Handle record action."""
        camera = self._camera_manager.get_camera()
        if not camera or not hasattr(camera, "is_recording") or not hasattr(camera, "start_recording") or not hasattr(camera, "stop_recording"):
            return
            
        try:
            if camera.is_recording():
                self._status_bar.showMessage("Stopping recording...")
                camera.stop_recording()
                self._record_action.setText("Record")
                self._status_bar.showMessage("Recording stopped", 3000)
            else:
                self._status_bar.showMessage("Starting recording...")
                # You'd need to implement this to choose a save path
                save_path = os.path.join(os.path.expanduser("~"), "Videos", "CanonControl")
                camera.start_recording(save_path)
                self._record_action.setText("Stop Recording")
                self._status_bar.showMessage("Recording started", 3000)
        except Exception as e:
            logger.error(f"Error with recording: {str(e)}")
            QMessageBox.warning(self, "Recording Error", f"Error with recording: {str(e)}")
    
    def _on_camera_settings(self):
        """Handle camera settings action."""
        dialog = SettingsDialog(self._camera_settings, self)
        dialog.exec()
    
    def _on_app_settings(self):
        """Handle application settings action."""
        # Implement application settings dialog
        QMessageBox.information(self, "Application Settings", "Application settings dialog not implemented yet.")
    
    def _on_about(self):
        """Handle about action."""
        QMessageBox.about(
            self,
            "About Canon Camera Control",
            "<h1>Canon Camera Control</h1>"
            "<p>Version 1.0.0</p>"
            "<p>A PyQt6-based application for controlling Canon cameras.</p>"
            "<p>Using cannon_wrapper for camera control.</p>"
        )
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Save window state
        self._settings.setValue("MainWindow/geometry", self.saveGeometry())
        self._settings.setValue("MainWindow/state", self.saveState())
        self._settings.setValue("MainWindow/splitterSizes", self._main_splitter.saveState())
        
        # Disconnect camera if connected
        if self._camera_manager.is_connected():
            # Stop live view if active
            if self._live_view_manager.is_active():
                self._live_view_manager.stop_live_view()
            
            # Disconnect camera
            self._camera_manager.disconnect_camera()
        
        # Accept the close event
        event.accept() 