# Canon Camera Control GUI - Mock Mode

This guide explains how to use the Canon Camera Control GUI application in "mock mode" - where it simulates a Canon camera without requiring the actual hardware or the real `cannon_wrapper` module.

## Using Mock Mode

The application automatically uses mock mode when it can't find the real `cannon_wrapper` module. This allows you to:

1. Test the UI and functionality without a physical camera
2. Develop and debug the application without depending on camera hardware
3. Demonstrate the application to users who don't have a camera connected

## Features Available in Mock Mode

In mock mode, the application provides:

- A simulated camera connection
- Mock live view with a test pattern (colorful gradient with a checkerboard pattern)
- Simulated camera settings (ISO, aperture, shutter speed, etc.)
- Mock photo capture and video recording functionality
- All UI components and workflows

## How to Use Mock Mode

1. Start the application:
   ```
   python main.py
   ```

2. You'll see a message in the status bar indicating you're using the mock camera.

3. Click "Connect" to establish a connection to the simulated camera.

4. Use the application as you normally would:
   - Start live view to see the test pattern
   - Configure camera settings
   - Take mock photos and record mock videos
   - Explore all UI features

## Limitations of Mock Mode

- No actual photos or videos are captured (though the application logs the actions)
- The simulated live view shows a test pattern, not actual camera output
- Camera settings don't affect the test pattern
- No actual files are written when taking photos or recording videos

## Switching to Real Mode

To use the application with a real Canon camera:

1. Install the actual `cannon_wrapper` module
2. Connect a supported Canon camera to your computer
3. Start the application

The application will automatically detect the real `cannon_wrapper` module and use it instead of the mock implementation.

## Troubleshooting

If you have issues with the mock mode:

- Make sure you have NumPy and OpenCV installed for the enhanced test pattern:
  ```
  pip install numpy opencv-python
  ```
- If the test pattern doesn't show, a simpler black frame is used as fallback
- Check the console output for any error messages or warnings 