#!/usr/bin/env python
"""
Simple Canon Camera Control Demo
This script demonstrates the basic use of the Canon camera control wrapper.
"""

import os
import sys
import time
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("simple_demo")

def run_camera_demo():
    """Run a simple camera control demonstration."""
    try:
        # Import the Canon wrapper
        from cannon_wrapper import Canon, DeviceNotFoundError, ConnectionError, OperationError
        
        logger.info("Initializing Canon camera interface...")
        camera = Canon()
        
        try:
            # For this demo, we'll use a placeholder camera reference
            # In a real application, you'd need the actual camera reference from EDSDK
            # This is a placeholder and will cause an error, but it shows how the API works
            camera_ref = None  # This would need to be replaced with an actual camera reference
            
            logger.info("Connecting to camera...")
            camera.connect(camera_ref)
            
            # Camera is now connected, we can control it
            model_name = camera.get_model_name()
            logger.info(f"Connected to camera: {model_name}")
            
            # Take a picture
            logger.info("Taking a picture...")
            camera.take_picture()
            
            # Disconnect from the camera
            logger.info("Disconnecting from camera...")
            camera.disconnect()
            logger.info("Camera disconnected.")
            
        except DeviceNotFoundError:
            logger.error("No camera found. Please make sure a camera is connected and turned on.")
        except ConnectionError as e:
            logger.error(f"Error connecting to camera: {e}")
        except OperationError as e:
            logger.error(f"Camera operation error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            
    except ImportError as e:
        logger.error(f"Could not import cannon_wrapper module: {e}")
        logger.error("Make sure the EDSDK bindings are properly built and installed.")
        logger.error("You can build the bindings by running:")
        logger.error("  python -m pip install -e .")
        logger.error("Or by running the build_edsdk.bat script on Windows.")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Simple Canon Camera Control Demo')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Make sure we can find the module
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the demo
    run_camera_demo()


if __name__ == "__main__":
    main() 