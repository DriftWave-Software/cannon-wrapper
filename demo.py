#!/usr/bin/env python
"""
Canon Camera Control Demo
This script demonstrates the use of the Canon camera control wrapper and GUI.
"""

import argparse
import logging
import sys
import os
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("demo")

def run_api_demo():
    """Run a demonstration of the direct camera control API."""
    try:
        from cannon_wrapper import Canon, DeviceNotFoundError, ConnectionError, OperationError
        import edsdk_bindings as eds
        
        logger.info("Initializing camera...")
        camera = Canon()
        
        # In a real application, you would get the camera reference from EDSDK
        # For this demo, we're using a placeholder
        camera_ref = "CAMERA_REF_PLACEHOLDER"
        
        try:
            # Connect to the camera
            logger.info("Connecting to camera...")
            camera.connect(camera_ref)
            
            # Get information about the camera
            model_name = camera.get_model_name()
            logger.info(f"Connected to camera: {model_name}")
            
            # Show camera settings
            try:
                iso = camera.get_iso()
                logger.info(f"ISO: {iso}")
                
                aperture = camera.get_aperture()
                logger.info(f"Aperture: {aperture}")
                
                shutter_speed = camera.get_shutter_speed()
                logger.info(f"Shutter Speed: {shutter_speed}")
            except Exception as e:
                logger.warning(f"Could not read some camera settings: {e}")
            
            # Take a picture
            logger.info("Taking a picture...")
            result = camera.take_picture()
            logger.info(f"Picture taken: {result}")
            
            # Wait for the camera to process the image
            time.sleep(2)
            
            # Start live view
            logger.info("Starting live view...")
            camera.start_live_view()
            logger.info("Live view started")
            
            # Download a few frames
            for i in range(3):
                logger.info(f"Downloading frame {i+1}...")
                frame = camera.download_live_view_frame()
                if frame is not None:
                    logger.info(f"Frame shape: {frame.shape}")
                time.sleep(1)
            
            # Stop live view
            logger.info("Stopping live view...")
            camera.stop_live_view()
            logger.info("Live view stopped")
            
            # Disconnect from the camera
            logger.info("Disconnecting from camera...")
            camera.disconnect()
            logger.info("Camera disconnected")
            
        except DeviceNotFoundError:
            logger.error("No camera found. Please make sure a camera is connected and turned on.")
        except ConnectionError as e:
            logger.error(f"Error connecting to camera: {e}")
        except OperationError as e:
            logger.error(f"Camera operation error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            
    except ImportError as e:
        logger.error(f"Could not import required modules: {e}")
        logger.error("Make sure the Canon wrapper is properly installed.")

def run_gui():
    """Run the camera control GUI."""
    try:
        # Add the current directory to the Python path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Import the GUI module
        from canon_gui.main import main as run_gui_main
        
        # Run the GUI
        logger.info("Starting Canon Camera Control GUI...")
        run_gui_main()
        
    except ImportError as e:
        logger.error(f"Could not import GUI modules: {e}")
        logger.error("Make sure all GUI dependencies are installed: pip install -r canon_gui/requirements.txt")
    except Exception as e:
        logger.error(f"Error starting GUI: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Canon Camera Control Demo')
    parser.add_argument('--mode', choices=['api', 'gui', 'both'], default='both',
                       help='Demo mode: api, gui, or both')
    
    args = parser.parse_args()
    
    if args.mode == 'api' or args.mode == 'both':
        logger.info("=== API Demonstration ===")
        run_api_demo()
        
    if args.mode == 'gui' or args.mode == 'both':
        logger.info("=== GUI Demonstration ===")
        run_gui()

if __name__ == "__main__":
    main() 