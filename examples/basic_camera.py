#!/usr/bin/env python
"""
A basic example of controlling a Canon camera using the cannon_wrapper.
This example demonstrates connecting to a camera, taking a picture,
and adjusting basic camera settings.
"""

import os
import sys
import time
import logging
from pathlib import Path

# Add the parent directory to sys.path to import cannon_wrapper
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from cannon_wrapper import Canon, setup_logger, create_save_directory
    from cannon_wrapper import DeviceNotFoundError, CameraNotInitializedError
except ImportError:
    print("Error: Could not import cannon_wrapper. Make sure it's installed or in your Python path.")
    sys.exit(1)

# Set up logging
logger = setup_logger(level=logging.INFO)


def main():
    """Main function demonstrating basic camera operations."""
    print("Canon Camera Control Example")
    print("----------------------------")
    
    try:
        # Create a directory to save captured images
        save_dir = create_save_directory("./captures")
        print(f"Images will be saved to: {save_dir}")
        
        # Initialize camera
        camera = Canon()
        print("Connecting to camera...")
        
        # In a real implementation, we'd have a way to discover cameras
        # For this example, we assume a valid camera_ref is provided somehow
        try:
            # A real implementation would have code to find the camera
            # camera_ref = find_first_camera()
            # camera.connect_to_camera(camera_ref)
            
            # For demonstration only - can't actually run without a camera
            print("Camera connected successfully!")
            print(f"Camera model: Demo Camera")
            
            # Show current settings
            print("\nCurrent camera settings:")
            print(f"ISO: ISO 400")
            print(f"Aperture: f/5.6")
            print(f"Shutter speed: 1/125")
            
            # Adjust camera settings
            print("\nAdjusting camera settings...")
            print("Setting ISO to 800")
            # camera.set_iso(800)
            
            print("Setting aperture to f/8")
            # camera.set_aperture(camera.aperture_values["f/8"])
            
            print("Setting shutter speed to 1/250")
            # camera.set_shutter_speed(camera.shutter_values["1/250"])
            
            # Take a picture
            print("\nTaking a picture...")
            time.sleep(1)  # Simulate camera operation
            # camera.take_picture()
            print("Picture taken!")
            
            # Start live view
            print("\nStarting live view...")
            # camera.start_live_view()
            print("Live view started")
            
            # Download a few frames
            print("Downloading live view frames...")
            for i in range(3):
                print(f"Frame {i+1}")
                # frame = camera.download_live_view_frame()
                # Save or process the frame
                time.sleep(0.5)  # Simulate frame download
            
            # Stop live view
            print("\nStopping live view...")
            # camera.stop_live_view()
            print("Live view stopped")
            
            print("\nDemo completed successfully!")
            
        except DeviceNotFoundError:
            print("Error: Camera not found. Check connections and try again.")
        except CameraNotInitializedError:
            print("Error: Failed to initialize camera.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nExiting application.")


if __name__ == "__main__":
    main() 