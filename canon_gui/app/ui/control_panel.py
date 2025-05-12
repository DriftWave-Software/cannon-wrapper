"""
Control Panel Module
Provides camera control UI elements.
"""

import logging
import os
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QComboBox, QSpinBox, QFileDialog, QFormLayout,
    QSlider, QCheckBox, QTabWidget, QFrame, QSizePolicy,
    QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer, QSettings

logger = logging.getLogger("canon_gui.ui.control")

class ControlPanel(QWidget):
    """Main control panel for camera operations."""
    
    def __init__(self, camera_manager, live_view_manager, camera_settings, parent=None):
        """Initialize the control panel.
        
        Args:
            camera_manager: Camera manager object
            live_view_manager: Live view manager object
            camera_settings: Camera settings object
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._camera_manager = camera_manager
        self._live_view_manager = live_view_manager
        self._camera_settings = camera_settings
        
        # State tracking
        self._is_connected = False
        self._is_live_view_active = False
        self._settings_widgets = {}
        self._current_save_path = os.path.join(os.path.expanduser("~"), "Pictures", "CanonControl")
        
        # Load settings
        self._settings = QSettings("CanonControl", "CanonGUI")
        
        # UI setup
        self._setup_ui()
        
        # Connect signals
        self._setup_connections()
        
        # Initial UI state
        self._update_ui_state()
    
    def _setup_ui(self):
        """Set up the control panel UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create tabs
        self._tab_widget = QTabWidget()
        main_layout.addWidget(self._tab_widget)
        
        # Camera tab
        camera_tab = QWidget()
        self._tab_widget.addTab(camera_tab, "Camera")
        self._setup_camera_tab(camera_tab)
        
        # Settings tab
        settings_tab = QWidget()
        self._tab_widget.addTab(settings_tab, "Settings")
        self._setup_settings_tab(settings_tab)
        
        # Capture tab
        capture_tab = QWidget()
        self._tab_widget.addTab(capture_tab, "Capture")
        self._setup_capture_tab(capture_tab)
        
        # Make the panel have a fixed width
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
    
    def _setup_camera_tab(self, tab: QWidget):
        """Set up the camera tab.
        
        Args:
            tab: Tab widget
        """
        layout = QVBoxLayout(tab)
        
        # Camera connection group
        connection_group = QGroupBox("Camera Connection")
        connection_layout = QVBoxLayout(connection_group)
        
        # Connection status
        self._connection_status = QLabel("Not connected")
        connection_layout.addWidget(self._connection_status)
        
        # Connect/disconnect button
        self._connect_button = QPushButton("Connect")
        connection_layout.addWidget(self._connect_button)
        
        # Camera info
        self._camera_info = QLabel("No camera detected")
        connection_layout.addWidget(self._camera_info)
        
        # Battery level 
        battery_layout = QHBoxLayout()
        battery_layout.addWidget(QLabel("Battery:"))
        self._battery_progress = QProgressBar()
        self._battery_progress.setRange(0, 100)
        self._battery_progress.setValue(0)
        battery_layout.addWidget(self._battery_progress)
        connection_layout.addLayout(battery_layout)
        
        layout.addWidget(connection_group)
        
        # Live view group
        live_view_group = QGroupBox("Live View")
        live_view_layout = QVBoxLayout(live_view_group)
        
        # Start/stop button
        self._live_view_button = QPushButton("Start Live View")
        self._live_view_button.setEnabled(False)
        live_view_layout.addWidget(self._live_view_button)
        
        # FPS control
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self._fps_spinbox = QSpinBox()
        self._fps_spinbox.setRange(1, 60)
        self._fps_spinbox.setValue(10)
        self._fps_spinbox.setEnabled(False)
        fps_layout.addWidget(self._fps_spinbox)
        live_view_layout.addLayout(fps_layout)
        
        layout.addWidget(live_view_group)
        
        # Quick capture group
        quick_capture_group = QGroupBox("Quick Capture")
        quick_capture_layout = QVBoxLayout(quick_capture_group)
        
        # Capture button
        self._capture_button = QPushButton("Take Photo")
        self._capture_button.setEnabled(False)
        quick_capture_layout.addWidget(self._capture_button)
        
        # Record video button
        self._record_button = QPushButton("Record Video")
        self._record_button.setEnabled(False)
        quick_capture_layout.addWidget(self._record_button)
        
        # Save location
        save_layout = QHBoxLayout()
        save_layout.addWidget(QLabel("Save to:"))
        self._browse_button = QPushButton("Browse...")
        save_layout.addWidget(self._browse_button)
        quick_capture_layout.addLayout(save_layout)
        
        self._save_location = QLabel(self._current_save_path)
        self._save_location.setWordWrap(True)
        quick_capture_layout.addWidget(self._save_location)
        
        layout.addWidget(quick_capture_group)
        
        # Add a stretch at the end
        layout.addStretch()
    
    def _setup_settings_tab(self, tab: QWidget):
        """Set up the settings tab.
        
        Args:
            tab: Tab widget
        """
        layout = QVBoxLayout(tab)
        
        # Camera settings group
        settings_group = QGroupBox("Camera Settings")
        settings_layout = QFormLayout(settings_group)
        
        # ISO
        iso_layout = QHBoxLayout()
        self._iso_combo = QComboBox()
        self._iso_combo.setEnabled(False)
        iso_layout.addWidget(self._iso_combo)
        self._settings_widgets[self._camera_settings.SETTING_ISO] = self._iso_combo
        settings_layout.addRow("ISO:", self._iso_combo)
        
        # Aperture
        self._aperture_combo = QComboBox()
        self._aperture_combo.setEnabled(False)
        self._settings_widgets[self._camera_settings.SETTING_APERTURE] = self._aperture_combo
        settings_layout.addRow("Aperture:", self._aperture_combo)
        
        # Shutter speed
        self._shutter_combo = QComboBox()
        self._shutter_combo.setEnabled(False)
        self._settings_widgets[self._camera_settings.SETTING_SHUTTER] = self._shutter_combo
        settings_layout.addRow("Shutter Speed:", self._shutter_combo)
        
        # White balance
        self._wb_combo = QComboBox()
        self._wb_combo.setEnabled(False)
        self._settings_widgets[self._camera_settings.SETTING_WHITE_BALANCE] = self._wb_combo
        settings_layout.addRow("White Balance:", self._wb_combo)
        
        # Refresh button
        self._refresh_settings_button = QPushButton("Refresh Settings")
        self._refresh_settings_button.setEnabled(False)
        settings_layout.addRow("", self._refresh_settings_button)
        
        layout.addWidget(settings_group)
        
        # Application settings group
        app_settings_group = QGroupBox("Application Settings")
        app_settings_layout = QFormLayout(app_settings_group)
        
        # Auto-connect on startup
        self._auto_connect_checkbox = QCheckBox()
        self._auto_connect_checkbox.setChecked(self._settings.value("AutoConnect", False, bool))
        app_settings_layout.addRow("Auto-connect on startup:", self._auto_connect_checkbox)
        
        # Auto-download images
        self._auto_download_checkbox = QCheckBox()
        self._auto_download_checkbox.setChecked(self._settings.value("AutoDownload", True, bool))
        app_settings_layout.addRow("Auto-download captured images:", self._auto_download_checkbox)
        
        # Save settings button
        self._save_settings_button = QPushButton("Save App Settings")
        app_settings_layout.addRow("", self._save_settings_button)
        
        layout.addWidget(app_settings_group)
        
        # Add a stretch at the end
        layout.addStretch()
    
    def _setup_capture_tab(self, tab: QWidget):
        """Set up the capture tab.
        
        Args:
            tab: Tab widget
        """
        layout = QVBoxLayout(tab)
        
        # Single capture group
        single_capture_group = QGroupBox("Single Capture")
        single_capture_layout = QVBoxLayout(single_capture_group)
        
        # File name template
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(QLabel("Filename:"))
        self._filename_template = QComboBox()
        self._filename_template.setEditable(True)
        self._filename_template.addItems([
            "IMG_{date}_{time}_{seq}",
            "CAM_{date}_{seq}",
            "PHOTO_{seq}"
        ])
        filename_layout.addWidget(self._filename_template)
        single_capture_layout.addLayout(filename_layout)
        
        # Self-timer
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(QLabel("Self-timer:"))
        self._timer_spinbox = QSpinBox()
        self._timer_spinbox.setRange(0, 30)
        self._timer_spinbox.setValue(0)
        self._timer_spinbox.setSuffix(" sec")
        timer_layout.addWidget(self._timer_spinbox)
        single_capture_layout.addLayout(timer_layout)
        
        # Capture button
        self._single_capture_button = QPushButton("Capture")
        self._single_capture_button.setEnabled(False)
        single_capture_layout.addWidget(self._single_capture_button)
        
        layout.addWidget(single_capture_group)
        
        # Interval capture group
        interval_group = QGroupBox("Interval Shooting")
        interval_layout = QVBoxLayout(interval_group)
        
        # Interval
        interval_settings = QHBoxLayout()
        interval_settings.addWidget(QLabel("Interval:"))
        self._interval_spinbox = QSpinBox()
        self._interval_spinbox.setRange(1, 3600)
        self._interval_spinbox.setValue(10)
        self._interval_spinbox.setSuffix(" sec")
        interval_settings.addWidget(self._interval_spinbox)
        interval_layout.addLayout(interval_settings)
        
        # Number of shots
        shots_layout = QHBoxLayout()
        shots_layout.addWidget(QLabel("Shots:"))
        self._shots_spinbox = QSpinBox()
        self._shots_spinbox.setRange(1, 9999)
        self._shots_spinbox.setValue(10)
        self._shots_spinbox.setSpecialValueText("∞")  # Infinity for continuous
        shots_layout.addWidget(self._shots_spinbox)
        interval_layout.addLayout(shots_layout)
        
        # Start/stop interval
        self._interval_button = QPushButton("Start Interval")
        self._interval_button.setEnabled(False)
        interval_layout.addWidget(self._interval_button)
        
        # Interval status
        self._interval_status = QLabel("Ready")
        interval_layout.addWidget(self._interval_status)
        
        layout.addWidget(interval_group)
        
        # Add a stretch at the end
        layout.addStretch()
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Camera manager signals
        self._camera_manager.camera_connected.connect(self._on_camera_connected)
        self._camera_manager.camera_disconnected.connect(self._on_camera_disconnected)
        self._camera_manager.camera_error.connect(self._on_camera_error)
        
        # Live view manager signals
        self._live_view_manager.live_view_started.connect(self._on_live_view_started)
        self._live_view_manager.live_view_stopped.connect(self._on_live_view_stopped)
        
        # Camera settings signals
        self._camera_settings.settings_changed.connect(self._on_setting_changed)
        
        # Button signals
        self._connect_button.clicked.connect(self._on_connect_clicked)
        self._live_view_button.clicked.connect(self._on_live_view_clicked)
        self._capture_button.clicked.connect(self._on_capture_clicked)
        self._record_button.clicked.connect(self._on_record_clicked)
        self._browse_button.clicked.connect(self._on_browse_clicked)
        self._refresh_settings_button.clicked.connect(self._on_refresh_settings_clicked)
        self._save_settings_button.clicked.connect(self._on_save_app_settings_clicked)
        self._single_capture_button.clicked.connect(self._on_single_capture_clicked)
        self._interval_button.clicked.connect(self._on_interval_clicked)
        
        # Settings combobox signals
        self._iso_combo.currentIndexChanged.connect(
            lambda idx: self._on_setting_selected(self._camera_settings.SETTING_ISO, idx))
        self._aperture_combo.currentIndexChanged.connect(
            lambda idx: self._on_setting_selected(self._camera_settings.SETTING_APERTURE, idx))
        self._shutter_combo.currentIndexChanged.connect(
            lambda idx: self._on_setting_selected(self._camera_settings.SETTING_SHUTTER, idx))
        self._wb_combo.currentIndexChanged.connect(
            lambda idx: self._on_setting_selected(self._camera_settings.SETTING_WHITE_BALANCE, idx))
        
        # Other controls
        self._fps_spinbox.valueChanged.connect(self._on_fps_changed)
    
    def _update_ui_state(self):
        """Update the UI state based on camera connection status."""
        # Camera tab
        is_connected = self._camera_manager.is_connected()
        
        if is_connected:
            self._connect_button.setText("Disconnect")
            self._connection_status.setText("Connected")
            
            # Update camera info
            camera_info = self._camera_manager.get_camera_info()
            if camera_info:
                model = camera_info.get("model", "Unknown camera")
                serial = camera_info.get("serial", "Unknown")
                self._camera_info.setText(f"Model: {model}\nSerial: {serial}")
                
                # Update battery level
                battery = camera_info.get("battery", 0)
                self._battery_progress.setValue(int(battery))
        else:
            self._connect_button.setText("Connect")
            self._connection_status.setText("Not connected")
            self._camera_info.setText("No camera detected")
            self._battery_progress.setValue(0)
        
        # Live view
        self._live_view_button.setEnabled(is_connected)
        self._fps_spinbox.setEnabled(is_connected and self._is_live_view_active)
        
        if self._is_live_view_active:
            self._live_view_button.setText("Stop Live View")
        else:
            self._live_view_button.setText("Start Live View")
        
        # Capture controls
        self._capture_button.setEnabled(is_connected)
        self._single_capture_button.setEnabled(is_connected)
        
        # Check if camera supports video recording
        camera = self._camera_manager.get_camera()
        supports_video = camera and hasattr(camera, "can_record_video") and camera.can_record_video()
        self._record_button.setEnabled(is_connected and supports_video)
        
        # Interval capture
        self._interval_button.setEnabled(is_connected)
        
        # Settings tab
        self._refresh_settings_button.setEnabled(is_connected)
        
        # Enable/disable settings controls
        for widget in self._settings_widgets.values():
            widget.setEnabled(is_connected)
    
    def _update_settings_widgets(self):
        """Update settings widgets with available options."""
        if not self._camera_manager.is_connected():
            return
            
        # ISO
        self._update_combo_options(
            self._iso_combo, 
            self._camera_settings.get_available_options(self._camera_settings.SETTING_ISO),
            self._camera_settings.get_setting(self._camera_settings.SETTING_ISO)
        )
        
        # Aperture
        self._update_combo_options(
            self._aperture_combo, 
            self._camera_settings.get_available_options(self._camera_settings.SETTING_APERTURE),
            self._camera_settings.get_setting(self._camera_settings.SETTING_APERTURE)
        )
        
        # Shutter speed
        self._update_combo_options(
            self._shutter_combo, 
            self._camera_settings.get_available_options(self._camera_settings.SETTING_SHUTTER),
            self._camera_settings.get_setting(self._camera_settings.SETTING_SHUTTER)
        )
        
        # White balance
        self._update_combo_options(
            self._wb_combo, 
            self._camera_settings.get_available_options(self._camera_settings.SETTING_WHITE_BALANCE),
            self._camera_settings.get_setting(self._camera_settings.SETTING_WHITE_BALANCE)
        )
    
    def _update_combo_options(self, combo: QComboBox, options, current_value=None):
        """Update a combo box with options.
        
        Args:
            combo: Combo box widget
            options: List of (value, label) tuples
            current_value: Current selected value
        """
        # Disconnect signals temporarily to avoid triggering callbacks
        combo.blockSignals(True)
        
        # Clear current items
        combo.clear()
        
        # Add options
        selected_index = -1
        for i, (value, label) in enumerate(options):
            combo.addItem(label, value)
            if value == current_value:
                selected_index = i
        
        # Select current value if found
        if selected_index >= 0:
            combo.setCurrentIndex(selected_index)
        
        # Reconnect signals
        combo.blockSignals(False)
    
    def _on_connect_clicked(self):
        """Handle connect/disconnect button click."""
        if self._camera_manager.is_connected():
            self._camera_manager.disconnect_camera()
        else:
            self._camera_manager.connect_camera()
    
    def _on_camera_connected(self, camera_model: str):
        """Handle camera connected event.
        
        Args:
            camera_model: Camera model name
        """
        self._is_connected = True
        self._update_ui_state()
        self._update_settings_widgets()
    
    def _on_camera_disconnected(self):
        """Handle camera disconnected event."""
        self._is_connected = False
        self._is_live_view_active = False
        self._update_ui_state()
    
    def _on_camera_error(self, error_message: str):
        """Handle camera error event.
        
        Args:
            error_message: Error message
        """
        logger.error(f"Camera error: {error_message}")
        # Nothing to do here, as error is shown in a message box by MainWindow
    
    def _on_live_view_clicked(self):
        """Handle live view button click."""
        if self._is_live_view_active:
            self._live_view_manager.stop_live_view()
        else:
            fps = self._fps_spinbox.value()
            self._live_view_manager.start_live_view(fps)
    
    def _on_live_view_started(self):
        """Handle live view started event."""
        self._is_live_view_active = True
        self._update_ui_state()
    
    def _on_live_view_stopped(self):
        """Handle live view stopped event."""
        self._is_live_view_active = False
        self._update_ui_state()
    
    def _on_fps_changed(self, value: int):
        """Handle FPS value changed.
        
        Args:
            value: New FPS value
        """
        if self._is_live_view_active:
            self._live_view_manager.set_frame_rate(value)
    
    def _on_capture_clicked(self):
        """Handle capture button click."""
        self._take_photo()
    
    def _on_record_clicked(self):
        """Handle record button click."""
        camera = self._camera_manager.get_camera()
        if not camera or not hasattr(camera, "is_recording"):
            return
            
        if camera.is_recording():
            camera.stop_recording()
            self._record_button.setText("Record Video")
        else:
            save_path = self._current_save_path
            camera.start_recording(save_path)
            self._record_button.setText("Stop Recording")
    
    def _on_browse_clicked(self):
        """Handle browse button click."""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        
        if dialog.exec():
            selected_dir = dialog.selectedFiles()[0]
            self._current_save_path = selected_dir
            self._save_location.setText(selected_dir)
            
            # Save for next time
            self._settings.setValue("SavePath", selected_dir)
    
    def _on_refresh_settings_clicked(self):
        """Handle refresh settings button click."""
        self._camera_settings.refresh_settings()
        self._update_settings_widgets()
    
    def _on_save_app_settings_clicked(self):
        """Handle save app settings button click."""
        # Save settings
        self._settings.setValue("AutoConnect", self._auto_connect_checkbox.isChecked())
        self._settings.setValue("AutoDownload", self._auto_download_checkbox.isChecked())
    
    def _on_single_capture_clicked(self):
        """Handle single capture button click."""
        timer_value = self._timer_spinbox.value()
        
        if timer_value > 0:
            # Delayed capture
            # In a real implementation, you'd show a countdown
            # For simplicity, we'll just use a QTimer
            QTimer.singleShot(timer_value * 1000, self._take_photo)
        else:
            # Immediate capture
            self._take_photo()
    
    def _on_interval_clicked(self):
        """Handle interval button click."""
        # For a real implementation, you'd need state tracking and a QTimer for the interval
        # This is a simplified version
        if self._interval_button.text() == "Start Interval":
            self._interval_button.setText("Stop Interval")
            self._interval_status.setText("Running...")
            
            # In a real implementation, you'd start a timer here
            # and take photos at the specified interval
        else:
            self._interval_button.setText("Start Interval")
            self._interval_status.setText("Stopped")
            
            # In a real implementation, you'd stop the timer here
    
    def _on_setting_changed(self, setting_name: str, value: Any):
        """Handle setting changed event.
        
        Args:
            setting_name: Setting name
            value: New value
        """
        # Update the corresponding widget if it exists
        if setting_name in self._settings_widgets:
            widget = self._settings_widgets[setting_name]
            
            # Find the index with the matching value
            for i in range(widget.count()):
                if widget.itemData(i) == value:
                    widget.setCurrentIndex(i)
                    break
    
    def _on_setting_selected(self, setting_name: str, index: int):
        """Handle setting selection in combo box.
        
        Args:
            setting_name: Setting name
            index: Selected index
        """
        if index < 0:
            return
            
        widget = self._settings_widgets[setting_name]
        value = widget.itemData(index)
        
        # Set the value in camera settings
        self._camera_settings.set_setting(setting_name, value)
    
    def _take_photo(self):
        """Take a photo with the current settings."""
        camera = self._camera_manager.get_camera()
        if not camera:
            return
            
        # Make sure the directory exists
        if not os.path.exists(self._current_save_path):
            os.makedirs(self._current_save_path)
            
        try:
            camera.take_photo(self._current_save_path)
        except Exception as e:
            logger.error(f"Error taking photo: {str(e)}")
            # The error will be shown by MainWindow 