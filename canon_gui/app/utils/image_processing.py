"""
Image processing utilities for Canon Camera Control GUI.
"""

import logging
import os
from typing import Optional, Tuple, Union, Any
import numpy as np
import io

# Try to import optional libraries
try:
    from PIL import Image, ImageEnhance
    _has_pil = True
except ImportError:
    _has_pil = False

try:
    import cv2
    _has_cv2 = True
except ImportError:
    _has_cv2 = False

logger = logging.getLogger("canon_gui.utils.image")


def save_image(image_data: Union[np.ndarray, bytes], file_path: str, 
               format: str = "JPEG", quality: int = 95) -> bool:
    """Save image data to a file.
    
    Args:
        image_data: Image data as NumPy array or bytes
        file_path: Path to save the image
        format: Image format (JPEG, PNG, etc.)
        quality: JPEG quality (0-100)
    
    Returns:
        True if saved successfully, False otherwise
    """
    if not _has_pil:
        logger.error("PIL library not available, cannot save image")
        return False
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Convert image data to PIL Image
        if isinstance(image_data, np.ndarray):
            # Convert NumPy array to PIL Image
            if len(image_data.shape) == 3 and image_data.shape[2] == 3:
                # RGB image
                img = Image.fromarray(image_data, "RGB")
            elif len(image_data.shape) == 2:
                # Grayscale image
                img = Image.fromarray(image_data, "L")
            else:
                logger.error(f"Unsupported image data shape: {image_data.shape}")
                return False
        elif isinstance(image_data, bytes):
            # Convert bytes to PIL Image
            img = Image.open(io.BytesIO(image_data))
        else:
            logger.error(f"Unsupported image data type: {type(image_data)}")
            return False
        
        # Save the image
        img.save(file_path, format=format, quality=quality)
        return True
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        return False


def apply_auto_contrast(image: np.ndarray) -> np.ndarray:
    """Apply automatic contrast adjustment to an image.
    
    Args:
        image: Input image as NumPy array
    
    Returns:
        Processed image as NumPy array
    """
    if _has_cv2:
        try:
            # Convert to LAB color space
            lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
            
            # Split into L, A, B channels
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to the L channel
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            
            # Merge the CLAHE enhanced L channel with the original A and B channels
            limg = cv2.merge((cl, a, b))
            
            # Convert back to RGB
            enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
            return enhanced
        except Exception as e:
            logger.error(f"Error applying auto contrast with OpenCV: {str(e)}")
            return image
    elif _has_pil:
        try:
            # Convert to PIL Image
            pil_img = Image.fromarray(image)
            
            # Apply auto contrast
            enhancer = ImageEnhance.Contrast(pil_img)
            enhanced = enhancer.enhance(1.5)  # Adjust contrast factor as needed
            
            # Convert back to NumPy array
            return np.array(enhanced)
        except Exception as e:
            logger.error(f"Error applying auto contrast with PIL: {str(e)}")
            return image
    else:
        logger.warning("No image processing library available, returning original image")
        return image


def apply_focus_peaking(image: np.ndarray, threshold: int = 50) -> np.ndarray:
    """Apply focus peaking to an image.
    
    Args:
        image: Input image as NumPy array
        threshold: Edge detection threshold
    
    Returns:
        Image with focus peaking as NumPy array
    """
    if not _has_cv2:
        logger.warning("OpenCV not available, cannot apply focus peaking")
        return image
    
    try:
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # Apply Laplacian edge detection
        edges = cv2.Laplacian(gray, cv2.CV_64F)
        
        # Normalize and threshold
        edges = np.absolute(edges)
        edges_norm = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        _, thresh = cv2.threshold(edges_norm, threshold, 255, cv2.THRESH_BINARY)
        
        # Create a color overlay
        if len(image.shape) == 3:
            result = image.copy()
            # Add blue highlighting to edges
            result[thresh > 0, 2] = 255  # Set blue channel to max for edge pixels
            return result
        else:
            # For grayscale, convert to color first
            result = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            result[thresh > 0, 2] = 255  # Set blue channel to max for edge pixels
            return result
    except Exception as e:
        logger.error(f"Error applying focus peaking: {str(e)}")
        return image


def generate_histogram(image: np.ndarray) -> Optional[np.ndarray]:
    """Generate a histogram image from an input image.
    
    Args:
        image: Input image as NumPy array
    
    Returns:
        Histogram image as NumPy array or None if failed
    """
    if not _has_cv2:
        logger.warning("OpenCV not available, cannot generate histogram")
        return None
    
    try:
        # Split the image into RGB channels
        height, width = 200, 256
        hist_image = np.zeros((height, width, 3), dtype=np.uint8)
        
        if len(image.shape) == 3:  # Color image
            color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # RGB
            for i, col in enumerate(color):
                hist = cv2.calcHist([image], [i], None, [width], [0, 256])
                cv2.normalize(hist, hist, 0, height, cv2.NORM_MINMAX)
                
                for x, y in enumerate(hist):
                    cv2.line(hist_image, (x, height), (x, height - int(y)), col, 1)
        else:  # Grayscale image
            hist = cv2.calcHist([image], [0], None, [width], [0, 256])
            cv2.normalize(hist, hist, 0, height, cv2.NORM_MINMAX)
            
            for x, y in enumerate(hist):
                cv2.line(hist_image, (x, height), (x, height - int(y)), (200, 200, 200), 1)
        
        return hist_image
    except Exception as e:
        logger.error(f"Error generating histogram: {str(e)}")
        return None


def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize an image to the specified dimensions.
    
    Args:
        image: Input image as NumPy array
        width: Target width
        height: Target height
    
    Returns:
        Resized image as NumPy array
    """
    if _has_cv2:
        try:
            return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
        except Exception as e:
            logger.error(f"Error resizing image with OpenCV: {str(e)}")
            return image
    elif _has_pil:
        try:
            pil_img = Image.fromarray(image)
            resized = pil_img.resize((width, height), Image.LANCZOS)
            return np.array(resized)
        except Exception as e:
            logger.error(f"Error resizing image with PIL: {str(e)}")
            return image
    else:
        logger.warning("No image processing library available, returning original image")
        return image


def annotate_image(image: np.ndarray, text: str, position: Tuple[int, int],
                  font_scale: float = 1.0, color: Tuple[int, int, int] = (255, 255, 255),
                  thickness: int = 2) -> np.ndarray:
    """Add text to an image.
    
    Args:
        image: Input image as NumPy array
        text: Text to add
        position: Position (x, y) coordinates
        font_scale: Font scale factor
        color: Text color as RGB tuple
        thickness: Text thickness
    
    Returns:
        Image with text as NumPy array
    """
    if not _has_cv2:
        logger.warning("OpenCV not available, cannot annotate image")
        return image
    
    try:
        result = image.copy()
        cv2.putText(result, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                    font_scale, color, thickness, cv2.LINE_AA)
        return result
    except Exception as e:
        logger.error(f"Error annotating image: {str(e)}")
        return image 