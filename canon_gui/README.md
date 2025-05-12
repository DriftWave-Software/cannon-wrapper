# Canon Camera Control GUI

A PyQt6-based GUI application for controlling Canon cameras using the cannon_wrapper.

## Features

- Connect to Canon cameras via USB
- Live view display with focus peaking, grid overlays
- Camera control interface for all major settings
  - ISO, aperture, shutter speed, white balance
  - Shooting modes and drive modes
  - Image quality and format settings
- Image capture with various options
  - Single-shot capture
  - Self-timer
  - Interval shooting
- Video recording
- File management for captured images and videos

## Requirements

- Python 3.6 or higher
- cannon_wrapper (Canon EDSDK Python wrapper)
- PyQt6
- NumPy
- OpenCV (optional, for advanced image processing)
- Pillow (for basic image processing)

## Installation

1. Make sure the cannon_wrapper is installed and properly configured.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application from the command line:

```bash
python main.py
```

### Basic workflow:

1. Connect to your camera using the "Connect" button
2. Configure camera settings in the Settings tab
3. Start live view to see a real-time preview
4. Capture images or record video
5. Disconnect when done

## Structure

- `main.py` - Application entry point
- `app/` - Main application code
  - `camera/` - Camera control modules
  - `ui/` - User interface components
  - `utils/` - Utility functions
- `resources/` - Application resources like icons

## Development

### Adding new features

To add new camera functionality:

1. Add the feature to the cannon_wrapper library first
2. Add UI components in the appropriate module
3. Connect the UI to the camera functionality

## License

MIT License

## Credits

Developed using the cannon_wrapper library for Canon EDSDK. 