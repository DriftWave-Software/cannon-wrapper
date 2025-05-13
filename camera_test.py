#!/usr/bin/env python
"""
Canon Camera Control Test Script
This script demonstrates how to use the Canon wrapper to control a camera.
"""

import time
import logging
import argparse
from cannon_wrapper import Canon, DeviceNotFoundError, ConnectionError, OperationError
import edsdk_bindings as eds

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("camera_test")

def test_camera_connection(camera_ref=None):
    """Test basic camera connection/disconnection."""
    logger.info("Testing camera connection...")
    
    try:
        # Create the camera object
        camera = Canon()
        
        # Connect to the camera
        logger.info("Connecting to camera...")
        eds.EdsInitializeSDK()
        cam_list = eds.EdsGetCameraList()
        count = eds.EdsGetChildCount(cam_list)
        if count > 0:
            camera_ref = eds.EdsGetChildAtIndex(cam_list, 0)
            camera.connect(camera_ref)
        else:
            logger.error("No cameras found")
        eds.EdsRelease(cam_list)
        eds.EdsTerminateSDK()
        
        # Get and display camera information
        model_name = camera.get_model_name()
        logger.info(f"Connected to camera: {model_name}")
        
        # Disconnect from the camera
        logger.info("Disconnecting from camera...")
        camera.disconnect()
        logger.info("Camera disconnected.")
        
        return True
        
    except DeviceNotFoundError:
        logger.error("No camera found. Please make sure a camera is connected and turned on.")
        return False
    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        return False
    except OperationError as e:
        logger.error(f"Operation error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def test_camera_settings(camera_ref=None):
    """Test reading and modifying camera settings."""
    logger.info("Testing camera settings...")
    
    try:
        # Create and connect to the camera
        camera = Canon()
        eds.EdsInitializeSDK()
        cam_list = eds.EdsGetCameraList()
        count = eds.EdsGetChildCount(cam_list)
        if count > 0:
            camera_ref = eds.EdsGetChildAtIndex(cam_list, 0)
            camera.connect(camera_ref)
        else:
            logger.error("No cameras found")
        eds.EdsRelease(cam_list)
        eds.EdsTerminateSDK()
        model_name = camera.get_model_name()
        logger.info(f"Connected to camera: {model_name}")
        
        # Get current settings
        try:
            iso = camera.get_iso()
            logger.info(f"Current ISO: {camera.get_iso()}")
            
            aperture = camera.get_aperture()
            logger.info(f"Current Aperture: {camera.get_aperture()}")
            
            shutter_speed = camera.get_shutter_speed()
            logger.info(f"Current Shutter Speed: {camera.get_shutter_speed()}")
        except Exception as e:
            logger.warning(f"Could not read some camera settings: {str(e)}")
        
        # Get available options
        try:
            iso_options = camera.get_available_iso_values()
            logger.info(f"Available ISO values: {iso_options}")
            
            aperture_options = camera.get_available_aperture_values()
            logger.info(f"Available Aperture values: {aperture_options}")
            
            shutter_options = camera.get_available_shutter_values()
            logger.info(f"Available Shutter Speed values: {shutter_options}")
        except Exception as e:
            logger.warning(f"Could not get available options: {str(e)}")
        
        # Modify a setting
        if iso_options and len(iso_options) > 0:
            test_iso = iso_options[0][0]  # Use the first available value
            logger.info(f"Setting ISO to {test_iso}...")
            camera.set_iso(test_iso)
            new_iso = camera.get_iso()
            logger.info(f"New ISO: {new_iso}")
        
        # Disconnect from the camera
        camera.disconnect()
        logger.info("Camera disconnected.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in settings test: {str(e)}")
        return False

def test_live_view(camera_ref=None):
    """Test live view operations."""
    logger.info("Testing live view...")
    
    try:
        # Create and connect to the camera
        camera = Canon()
        eds.EdsInitializeSDK()
        cam_list = eds.EdsGetCameraList()
        count = eds.EdsGetChildCount(cam_list)
        if count > 0:
            camera_ref = eds.EdsGetChildAtIndex(cam_list, 0)
            camera.connect(camera_ref)
        else:
            logger.error("No cameras found")
        eds.EdsRelease(cam_list)
        eds.EdsTerminateSDK()
        model_name = camera.get_model_name()
        logger.info(f"Connected to camera: {model_name}")
        
        # Start live view
        logger.info("Starting live view...")
        camera.start_live_view()
        logger.info("Live view started.")
        
        # Download a few frames
        for i in range(3):
            logger.info(f"Downloading frame {i+1}...")
            frame = camera.download_live_view_frame()
            logger.info(f"Frame shape: {frame.shape}")
            time.sleep(1)
        
        # Drive the lens
        logger.info("Testing focus near...")
        camera.focus(1, 2)  # Near, level 2
        time.sleep(1)
        
        logger.info("Testing focus far...")
        camera.focus(-1, 2)  # Far, level 2
        time.sleep(1)
        
        # Stop live view
        logger.info("Stopping live view...")
        camera.stop_live_view()
        logger.info("Live view stopped.")
        
        # Disconnect from the camera
        camera.disconnect()
        logger.info("Camera disconnected.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in live view test: {str(e)}")
        return False

def test_take_picture(camera_ref=None):
    """Test taking pictures."""
    logger.info("Testing picture taking...")
    
    try:
        # Create and connect to the camera
        camera = Canon()
        eds.EdsInitializeSDK()
        cam_list = eds.EdsGetCameraList()
        count = eds.EdsGetChildCount(cam_list)
        if count > 0:
            camera_ref = eds.EdsGetChildAtIndex(cam_list, 0)
            camera.connect(camera_ref)
        else:
            logger.error("No cameras found")
        eds.EdsRelease(cam_list)
        eds.EdsTerminateSDK()
        model_name = camera.get_model_name()
        logger.info(f"Connected to camera: {model_name}")
        
        # Take a picture
        logger.info("Taking a picture...")
        result = camera.take_picture()
        logger.info(f"Picture taken: {result}")
        
        # Wait for the camera to process the image
        logger.info("Waiting for image processing...")
        time.sleep(2)
        
        # Take another picture using shutter button simulation
        logger.info("Testing shutter button simulation...")
        
        # Press halfway (focus)
        logger.info("Pressing shutter button halfway...")
        camera.press_shutter(eds.EdsCameraCommand.SHUTTER_BUTTON_HALFWAY)
        time.sleep(1)
        
        # Press completely (take picture)
        logger.info("Pressing shutter button completely...")
        camera.press_shutter(eds.EdsCameraCommand.SHUTTER_BUTTON_COMPLETELY)
        time.sleep(0.5)
        
        # Release shutter
        logger.info("Releasing shutter button...")
        camera.press_shutter(eds.EdsCameraCommand.SHUTTER_BUTTON_OFF)
        
        # Wait for the camera to process the image
        logger.info("Waiting for image processing...")
        time.sleep(2)
        
        # Disconnect from the camera
        camera.disconnect()
        logger.info("Camera disconnected.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in picture taking test: {str(e)}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Canon Camera Control Test')
    parser.add_argument('--test', choices=['connection', 'settings', 'live_view', 'picture', 'all'], 
                        default='all', help='Test to run')
    args = parser.parse_args()
    
    # Run the selected test
    if args.test == 'connection' or args.test == 'all':
        test_camera_connection()
        
    if args.test == 'settings' or args.test == 'all':
        test_camera_settings()
        
    if args.test == 'live_view' or args.test == 'all':
        test_live_view()
        
    if args.test == 'picture' or args.test == 'all':
        test_take_picture()

if __name__ == "__main__":
    main() 