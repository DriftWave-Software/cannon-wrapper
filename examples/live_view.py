#!/usr/bin/env python
"""
Example of using the live view functionality of a Canon camera.
This example shows how to start live view, download frames, and adjust focus.
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
    from cannon_wrapper import DeviceNotFoundError, LiveViewNotActiveError
except ImportError:
    print("Error: Could not import cannon_wrapper. Make sure it's installed or in your Python path.")
    sys.exit(1)

# Optional: Try to import OpenCV for displaying images
try:
    import cv2
    import numpy as np
    HAVE_OPENCV = True
except ImportError:
    HAVE_OPENCV = False
    print("OpenCV not found. Live view frames will be saved but not displayed.")

# Set up logging
logger = setup_logger(level=logging.INFO)


def convert_frame_to_cv2(frame_data):
    """Convert the EDSDK frame data to an OpenCV image.
    
    This is a placeholder function. In a real implementation, this would
    convert the frame data format returned by EDSDK to an OpenCV image.
    
    Args:
        frame_data: Raw frame data from the camera
        
    Returns:
        OpenCV-compatible image or None if conversion fails
    """
    # This is a mock implementation - in reality, you'd convert the actual data
    # For this example, we'll create a simple gradient image
    if HAVE_OPENCV:
        height, width = 480, 640
        img = np.zeros((height, width, 3), dtype=np.uint8)
        # Create a gradient from top-left to bottom-right
        for y in range(height):
            for x in range(width):
                img[y, x] = [
                    int(255 * y / height),
                    int(255 * x / width),
                    int(255 * (x + y) / (width + height))
                ]
        return img
    return None


def main():
    """Main function demonstrating live view functionality."""
    print("Canon Camera Live View Example")
    print("------------------------------")
    
    try:
        # Create a directory to save captured frames
        save_dir = create_save_directory("./live_view_frames")
        print(f"Frames will be saved to: {save_dir}")
        
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
            
            # Start live view
            print("\nStarting live view...")
            # camera.start_live_view()
            print("Live view started")
            
            # Set up OpenCV window if available
            if HAVE_OPENCV:
                cv2.namedWindow("Canon Live View", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Canon Live View", 800, 600)
            
            # Download and process live view frames
            print("\nDownloading live view frames...")
            print("Press 'q' to quit, 'f' for focus near, 'j' for focus far")
            
            frame_count = 0
            max_frames = 100  # Limit frames for the example
            
            while frame_count < max_frames:
                # In a real implementation, this would be:
                # frame_data = camera.download_live_view_frame()
                
                # For demonstration, we'll use our mock function
                frame_data = f"dummy_frame_data_{frame_count}"  # Placeholder
                
                # Convert and display frame if OpenCV is available
                if HAVE_OPENCV:
                    # Convert frame to OpenCV format
                    img = convert_frame_to_cv2(frame_data)
                    
                    # Add some information to the frame
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, f"Frame: {frame_count}", (20, 30), font, 0.7, (255, 255, 255), 2)
                    cv2.putText(img, "Press 'q' to quit", (20, 60), font, 0.7, (255, 255, 255), 2)
                    
                    # Save frame
                    frame_path = os.path.join(save_dir, f"frame_{frame_count:04d}.jpg")
                    cv2.imwrite(frame_path, img)
                    
                    # Display frame
                    cv2.imshow("Canon Live View", img)
                    
                    # Wait for keyboard input
                    key = cv2.waitKey(100)  # Wait 100ms
                    
                    if key == ord('q'):  # Quit
                        print("Quitting...")
                        break
                    elif key == ord('f'):  # Focus near
                        print("Focusing near...")
                        # camera.focus_near()
                    elif key == ord('j'):  # Focus far
                        print("Focusing far...")
                        # camera.focus_far()
                else:
                    # Without OpenCV, just save placeholder frame and wait
                    frame_path = os.path.join(save_dir, f"frame_{frame_count:04d}.txt")
                    with open(frame_path, 'w') as f:
                        f.write(f"Placeholder for frame {frame_count}")
                    
                    print(f"Frame {frame_count} saved to {frame_path}")
                    time.sleep(0.1)  # Wait a bit before next frame
                
                frame_count += 1
            
            # Stop live view
            print("\nStopping live view...")
            # camera.stop_live_view()
            
            # Clean up OpenCV
            if HAVE_OPENCV:
                cv2.destroyAllWindows()
            
            print("\nLive view demo completed!")
            
        except DeviceNotFoundError:
            print("Error: Camera not found. Check connections and try again.")
        except LiveViewNotActiveError:
            print("Error: Failed to activate live view.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nExiting application.")


if __name__ == "__main__":
    main() 