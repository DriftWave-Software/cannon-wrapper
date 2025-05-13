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
- PyQt6-based GUI application for visual camera control

## Structure

```
cannon_wrapper/
├── __init__.py           # Package initializer with imports
├── bindings.cpp          # C++ bindings using pybind11
├── camera.py             # Main Camera control class
├── exceptions.py         # Python exceptions for error handling
├── utils.py              # Core utility functions
├── cannon_wrapper.py     # High-level Python wrapper for EDSDK bindings
├── camera_test.py        # Test script for camera functionality
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
├── examples/             # Example scripts
│   ├── __init__.py       # Examples module initializer
│   ├── basic_camera.py   # Basic camera operations example
│   └── live_view.py      # Live view example
└── canon_gui/            # GUI application for camera control
    ├── app/              # Application modules
    │   ├── camera/       # Camera control modules
    │   ├── ui/           # UI components
    │   └── utils/        # Utility functions and classes
    ├── resources/        # Resources and assets
    ├── main.py           # Main application entry point
    └── requirements.txt  # GUI application dependencies
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

### Installing GUI dependencies

If you want to use the GUI application, install additional dependencies:

```bash
pip install -r canon_gui/requirements.txt
```

## Usage

### Basic Usage

```python
from cannon_wrapper import Canon, DeviceNotFoundError, ConnectionError

try:
    # Connect to a camera
    camera = Canon()
    camera.connect(camera_ref)  # Use camera_ref from EDSDK initialization
    
    # Get camera information
    model_name = camera.get_model_name()
    print(f"Connected to camera: {model_name}")
    
    # Take a picture
    camera.take_picture()
    
    # Adjust camera settings
    camera.set_iso(800)
    camera.set_aperture(5)  # Aperture value from EDSDK
    camera.set_shutter_speed(12)  # Shutter speed value from EDSDK
    
    # Use live view
    camera.start_live_view()
    frame = camera.download_live_view_frame()
    # Process frame...
    camera.stop_live_view()
    
    # Disconnect
    camera.disconnect()
    
except DeviceNotFoundError:
    print("No camera found. Please make sure a camera is connected and turned on.")
except ConnectionError as e:
    print(f"Error connecting to camera: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Using the Context Manager

```python
from cannon_wrapper import Canon, DeviceNotFoundError, ConnectionError

try:
    # Use context manager for auto-cleanup
    with Canon() as camera:
        camera.connect(camera_ref)
        camera.take_picture()
        # More operations...
        
except DeviceNotFoundError:
    print("No camera found. Please make sure a camera is connected and turned on.")
except ConnectionError as e:
    print(f"Error connecting to camera: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Using the GUI Application

The package includes a PyQt6-based GUI application for camera control:

```bash
# Run the GUI application
python -m canon_gui.main
```

The GUI application provides:
- Camera connection and disconnection
- Live view display
- Camera settings adjustment
- Photo capture
- Focus control
- And more...

### Testing Camera Functionality

A simple test script is provided to verify camera functionality:

```bash
# Test all functionality
python camera_test.py

# Test specific functionality
python camera_test.py --test connection
python camera_test.py --test settings
python camera_test.py --test live_view
python camera_test.py --test picture
```

## API Reference

### Main Classes

- `Canon`: High-level interface for Canon cameras
- `EdsEventListener`: Event listener for camera events
- `DeviceNotFoundError`, `ConnectionError`, `OperationError`: Exception classes

### Key Methods

#### Camera Connection
- `connect(camera_ref=None)`: Connect to a camera
- `disconnect()`: Disconnect from the camera
- `is_connected()`: Check if the camera is connected
- `get_model_name()`: Get the camera model name
- `get_device_info()`: Get information about the connected camera

#### Camera Operations
- `take_picture()`: Take a picture
- `press_shutter(mode)`: Press the shutter button in a specific mode

#### Live View Operations
- `start_live_view()`: Start the camera's live view mode
- `stop_live_view()`: Stop the camera's live view mode
- `download_live_view_frame()`: Download the current live view frame
- `focus(direction, level=3)`: Focus the lens in the specified direction

#### Camera Settings
- `get_iso()`, `set_iso(iso)`: Get/set ISO value
- `get_aperture()`, `set_aperture(aperture)`: Get/set aperture value
- `get_shutter_speed()`, `set_shutter_speed(shutter_speed)`: Get/set shutter speed
- `get_available_iso_values()`: Get available ISO values
- `get_available_aperture_values()`: Get available aperture values
- `get_available_shutter_values()`: Get available shutter speed values

## Error Handling

```python
from cannon_wrapper import Canon, DeviceNotFoundError, ConnectionError, OperationError

try:
    camera = Canon()
    camera.connect(camera_ref)
    camera.take_picture()
except DeviceNotFoundError:
    print("Camera not found. Check connections.")
except ConnectionError:
    print("Error connecting to camera.")
except OperationError as e:
    print(f"Camera operation error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Canon for providing the EDSDK
- pybind11 for making C++ binding creation easier 