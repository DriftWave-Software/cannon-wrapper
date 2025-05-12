# cannon_wrapper

A Python wrapper for Canon EDSDK, designed to provide easy-to-use Pythonic interfaces for Canon camera control and image capture.

## Overview

This package provides Python bindings for the Canon EDSDK C++ API using pybind11. It allows you to control Canon cameras programmatically, taking photos, adjusting camera settings, using live view, and much more.

Key features:
- Easy-to-use Pythonic interface
- Object-oriented design
- Proper error handling with Python exceptions
- Type hints for better IDE support
- Compatible with Windows, macOS, and Linux (where EDSDK is available)

## Structure

```
cannon_wrapper/
├── __init__.py           # Package initializer with imports
├── bindings.cpp          # C++ bindings using pybind11
├── camera.py             # Main Camera control class
├── exceptions.py         # Python exceptions for error handling
├── utils.py              # Core utility functions
├── api/                  # High-level API
│   ├── __init__.py       # API module initializer
│   ├── camera.py         # Camera class re-exports
│   ├── live_view.py      # Live view specialized functionality
│   └── settings.py       # Camera settings constants
├── core/                 # Core functionality
│   ├── __init__.py       # Core module initializer
│   ├── binding_helpers.py # Helpers for binding interaction
│   └── image_utils.py    # Image processing utilities
├── edsdk/                # Canon EDSDK C++ source files
│   ├── include/          # Header files
│   ├── src/              # Source files
│   ├── resources/        # Resources and assets
│   ├── docs/             # Documentation
│   └── projects/         # Project files
└── examples/             # Example scripts
    ├── __init__.py       # Examples module initializer
    ├── basic_camera.py   # Basic camera operations example
    └── live_view.py      # Live view example
```

## Installation

### Prerequisites

- Python 3.6+
- Canon EDSDK (must be obtained from Canon)
- A C++ compiler (MSVC on Windows, GCC on Linux, Clang on macOS)
- CMake 3.14+
- pybind11

### Building from source

1. Clone the repository
2. Install build requirements: `pip install pybind11 scikit-build cmake`
3. Build the package: `pip install -e .`

## Usage

### Basic Usage

```python
from cannon_wrapper import Canon

# Connect to a camera
camera = Canon()
camera.connect_to_camera()

# Take a picture
camera.take_picture()

# Adjust camera settings
camera.set_iso(800)
camera.set_aperture(camera.AV_F8)
camera.set_shutter_speed(camera.TV_1_125)

# Use live view
camera.start_live_view()
frame = camera.download_live_view_frame()
# Process frame...
camera.stop_live_view()

# Use context manager for auto-cleanup
with Canon() as cam:
    cam.connect_to_camera()
    cam.take_picture()
```

### Advanced Live View Usage

```python
from cannon_wrapper.api.live_view import LiveViewManager
from cannon_wrapper import Canon

# Connect to camera
camera = Canon()
camera.connect_to_camera()

# Get the camera model
model = camera._model  # Internal access, normally not recommended

# Create a live view manager
live_view = LiveViewManager(model)

# Use as context manager
with live_view:
    # Live view is automatically started
    
    # Set zoom level
    live_view.set_zoom_level(5)
    
    # Set zoom position
    live_view.set_zoom_position(320, 240)
    
    # Download frame
    frame = live_view.download_frame()
    
    # Focus operations
    live_view.drive_lens_near(step=2)
    live_view.drive_lens_far(step=1)
    live_view.auto_focus(320, 240)
    
    # Get focus info
    focus_info = live_view.get_focus_info()
    print(f"Zoom level: {focus_info['zoom_level']}")
    
    # Live view is automatically stopped when exiting the context
```

### Using Camera Settings

```python
from cannon_wrapper.api.settings import ISOSettings, ApertureSettings, ShutterSpeedSettings
from cannon_wrapper import Canon

camera = Canon()
camera.connect_to_camera()

# Set ISO using predefined constants
camera.set_iso(ISOSettings.ISO_800)
print(f"ISO: {ISOSettings.get_label(camera.get_iso())}")

# Set aperture using predefined constants
camera.set_aperture(ApertureSettings.F8_0)
print(f"Aperture: {ApertureSettings.get_label(camera.get_aperture())}")

# Set shutter speed using predefined constants
camera.set_shutter_speed(ShutterSpeedSettings.SEC_1_125)
print(f"Shutter speed: {ShutterSpeedSettings.get_label(camera.get_shutter_speed())}")
```

## API Reference

See the examples directory for more detailed usage examples.

## Error Handling

```python
from cannon_wrapper import Canon, DeviceNotFoundError, DeviceBusyError

try:
    camera = Canon()
    camera.connect_to_camera()
    camera.take_picture()
except DeviceNotFoundError:
    print("Camera not found. Check connections.")
except DeviceBusyError:
    print("Camera is busy. Try again later.")
except Exception as e:
    print(f"An error occurred: {e}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Canon for providing the EDSDK
- pybind11 for making C++ binding creation easier 