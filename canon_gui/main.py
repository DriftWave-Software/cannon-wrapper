#!/usr/bin/env python
"""
Canon Camera Control - Main Application
A PyQt6-based GUI application for controlling Canon cameras using the cannon_wrapper.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app.ui.main_window import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Canon Camera Control")
    app.setApplicationVersion("1.0.0")
    
    # Set the application icon
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 