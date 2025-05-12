"""
Settings Dialog Module
Provides a dialog for configuring camera settings.
"""

import logging
from typing import Optional, Dict, Any, List, Tuple
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QComboBox, QTabWidget, QWidget, QFormLayout,
    QDialogButtonBox, QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSlot

logger = logging.getLogger("canon_gui.ui.settings")

class SettingsDialog(QDialog):
    """Dialog for configuring camera settings."""
    
    def __init__(self, camera_settings, parent=None):
        """Initialize the settings dialog.
        
        Args:
            camera_settings: Camera settings object
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._camera_settings = camera_settings
        self._settings_widgets = {}
        
        # Set up the dialog
        self.setWindowTitle("Camera Settings")
        self.resize(450, 550)
        
        # Create UI
        self._setup_ui()
        
        # Connect signals
        self._setup_connections()
        
        # Load current settings
        self._load_settings()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create tabs
        self._tab_widget = QTabWidget()
        main_layout.addWidget(self._tab_widget)
        
        # Exposure tab
        exposure_tab = QWidget()
        self._tab_widget.addTab(exposure_tab, "Exposure")
        self._setup_exposure_tab(exposure_tab)
        
        # Image tab
        image_tab = QWidget()
        self._tab_widget.addTab(image_tab, "Image")
        self._setup_image_tab(image_tab)
        
        # Advanced tab
        advanced_tab = QWidget()
        self._tab_widget.addTab(advanced_tab, "Advanced")
        self._setup_advanced_tab(advanced_tab)
        
        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._apply_settings)
        main_layout.addWidget(button_box)
    
    def _setup_exposure_tab(self, tab: QWidget):
        """Set up the exposure tab.
        
        Args:
            tab: Tab widget
        """
        layout = QFormLayout(tab)
        
        # Shooting mode
        self._shooting_mode_combo = QComboBox()
        self._settings_widgets[self._camera_settings.SETTING_SHOOT_MODE] = self._shooting_mode_combo
        layout.addRow("Shooting Mode:", self._shooting_mode_combo)
        
        # ISO
        self._iso_combo = QComboBox()
        self._settings_widgets[self._camera_settings.SETTING_ISO] = self._iso_combo
        layout.addRow("ISO:", self._iso_combo)
        
        # Aperture
        self._aperture_combo = QComboBox()
        self._settings_widgets[self._camera_settings.SETTING_APERTURE] = self._aperture_combo
        layout.addRow("Aperture:", self._aperture_combo)
        
        # Shutter speed
        self._shutter_combo = QComboBox()
        self._settings_widgets[self._camera_settings.SETTING_SHUTTER] = self._shutter_combo
        layout.addRow("Shutter Speed:", self._shutter_combo)
        
        # Exposure compensation
        self._exposure_comp_combo = QComboBox()
        self._settings_widgets[self._camera_settings.SETTING_EXPOSURE_COMP] = self._exposure_comp_combo
        layout.addRow("Exposure Compensation:", self._exposure_comp_combo)
    
    def _setup_image_tab(self, tab: QWidget):
        """Set up the image tab.
        
        Args:
            tab: Tab widget
        """
        layout = QFormLayout(tab)
        
        # White balance
        self._wb_combo = QComboBox()
        self._settings_widgets[self._camera_settings.SETTING_WHITE_BALANCE] = self._wb_combo
        layout.addRow("White Balance:", self._wb_combo)
        
        # Image quality
        self._quality_combo = QComboBox()
        self._settings_widgets[self._camera_settings.SETTING_IMAGE_QUALITY] = self._quality_combo
        layout.addRow("Image Quality:", self._quality_combo)
        
        # Image format options
        self._raw_checkbox = QCheckBox("RAW")
        layout.addRow("Format:", self._raw_checkbox)
        
        # JPEG options (only enabled if RAW is not checked)
        jpeg_group = QGroupBox("JPEG Settings")
        jpeg_layout = QFormLayout(jpeg_group)
        
        self._jpeg_quality_combo = QComboBox()
        self._jpeg_quality_combo.addItems(["Fine", "Normal", "Basic"])
        jpeg_layout.addRow("Quality:", self._jpeg_quality_combo)
        
        self._jpeg_size_combo = QComboBox()
        self._jpeg_size_combo.addItems(["Large", "Medium", "Small"])
        jpeg_layout.addRow("Size:", self._jpeg_size_combo)
        
        layout.addRow("", jpeg_group)
    
    def _setup_advanced_tab(self, tab: QWidget):
        """Set up the advanced tab.
        
        Args:
            tab: Tab widget
        """
        layout = QFormLayout(tab)
        
        # Auto focus mode
        self._af_mode_combo = QComboBox()
        self._af_mode_combo.addItems(["One Shot", "AI Servo", "AI Focus"])
        layout.addRow("AF Mode:", self._af_mode_combo)
        
        # Drive mode
        self._drive_mode_combo = QComboBox()
        self._drive_mode_combo.addItems(["Single", "Continuous Low", "Continuous High", "Self-timer"])
        layout.addRow("Drive Mode:", self._drive_mode_combo)
        
        # Metering mode
        self._metering_combo = QComboBox()
        self._metering_combo.addItems(["Evaluative", "Partial", "Spot", "Center-weighted"])
        layout.addRow("Metering:", self._metering_combo)
        
        # Flash settings
        flash_group = QGroupBox("Flash Settings")
        flash_layout = QFormLayout(flash_group)
        
        self._flash_mode_combo = QComboBox()
        self._flash_mode_combo.addItems(["Auto", "On", "Off", "Red-eye Reduction"])
        flash_layout.addRow("Mode:", self._flash_mode_combo)
        
        self._flash_comp_spinbox = QSpinBox()
        self._flash_comp_spinbox.setRange(-3, 3)
        self._flash_comp_spinbox.setSingleStep(1)
        self._flash_comp_spinbox.setPrefix("± ")
        flash_layout.addRow("Compensation:", self._flash_comp_spinbox)
        
        layout.addRow("", flash_group)
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Camera settings signals
        self._camera_settings.settings_changed.connect(self._on_setting_changed)
        
        # RAW checkbox connections
        self._raw_checkbox.toggled.connect(self._on_raw_toggled)
    
    def _load_settings(self):
        """Load current settings from the camera."""
        # Load each setting into its corresponding widget
        for setting_name, widget in self._settings_widgets.items():
            self._update_setting_widget(setting_name, widget)
        
        # Initialize RAW/JPEG controls
        # In a real implementation, you'd get this from the camera
        self._raw_checkbox.setChecked(False)
        self._on_raw_toggled(False)
    
    def _update_setting_widget(self, setting_name: str, widget: QComboBox):
        """Update a setting widget with available options and current value.
        
        Args:
            setting_name: Setting name
            widget: Widget to update
        """
        # Get available options for this setting
        options = self._camera_settings.get_available_options(setting_name)
        
        # Get current value
        current_value = self._camera_settings.get_setting(setting_name)
        
        # Clear current items
        widget.blockSignals(True)
        widget.clear()
        
        # Add options
        selected_index = -1
        for i, (value, label) in enumerate(options):
            widget.addItem(label, value)
            if value == current_value:
                selected_index = i
        
        # Select current value if found
        if selected_index >= 0:
            widget.setCurrentIndex(selected_index)
            
        widget.blockSignals(False)
    
    def _on_setting_changed(self, setting_name: str, value: Any):
        """Handle setting changed event.
        
        Args:
            setting_name: Setting name
            value: New value
        """
        if setting_name in self._settings_widgets:
            widget = self._settings_widgets[setting_name]
            
            # Update the widget
            for i in range(widget.count()):
                if widget.itemData(i) == value:
                    widget.blockSignals(True)
                    widget.setCurrentIndex(i)
                    widget.blockSignals(False)
                    break
    
    def _on_raw_toggled(self, checked: bool):
        """Handle RAW checkbox toggled.
        
        Args:
            checked: Whether the checkbox is checked
        """
        # Enable/disable JPEG options based on RAW selection
        # In a real implementation, you might want to handle RAW+JPEG option
        self._jpeg_quality_combo.setEnabled(not checked)
        self._jpeg_size_combo.setEnabled(not checked)
    
    def _apply_settings(self):
        """Apply all settings to the camera."""
        # Apply each setting from its corresponding widget
        for setting_name, widget in self._settings_widgets.items():
            if isinstance(widget, QComboBox) and widget.currentIndex() >= 0:
                value = widget.currentData()
                self._camera_settings.set_setting(setting_name, value)
    
    def accept(self):
        """Handle dialog acceptance."""
        # Apply settings
        self._apply_settings()
        
        # Close the dialog
        super().accept()
        
    def reject(self):
        """Handle dialog rejection."""
        # Just close the dialog without applying settings
        super().reject() 