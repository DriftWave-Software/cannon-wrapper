"""
Camera settings module for Canon EDSDK.

This module provides classes and constants for working with camera settings
like ISO, aperture, shutter speed, etc.
"""

import logging
from typing import Dict, Any, List, Optional, Union

try:
    from ..edsdk_bindings import *
except ImportError:
    logging.warning("Could not import EDSDK bindings.")

logger = logging.getLogger(__name__)


class ISOSettings:
    """ISO settings for Canon cameras."""
    
    # Common ISO values
    AUTO = 0x00000000
    ISO_50 = 0x00000040
    ISO_100 = 0x00000048
    ISO_125 = 0x0000004B
    ISO_160 = 0x0000004D
    ISO_200 = 0x00000050
    ISO_250 = 0x00000053
    ISO_320 = 0x00000055
    ISO_400 = 0x00000058
    ISO_500 = 0x0000005B
    ISO_640 = 0x0000005D
    ISO_800 = 0x00000060
    ISO_1000 = 0x00000063
    ISO_1250 = 0x00000065
    ISO_1600 = 0x00000068
    ISO_2000 = 0x0000006B
    ISO_2500 = 0x0000006D
    ISO_3200 = 0x00000070
    ISO_4000 = 0x00000073
    ISO_5000 = 0x00000075
    ISO_6400 = 0x00000078
    ISO_8000 = 0x0000007B
    ISO_10000 = 0x0000007D
    ISO_12800 = 0x00000080
    ISO_16000 = 0x00000083
    ISO_20000 = 0x00000085
    ISO_25600 = 0x00000088
    ISO_32000 = 0x0000008B
    ISO_40000 = 0x0000008D
    ISO_51200 = 0x00000090
    ISO_102400 = 0x00000098
    
    @classmethod
    def get_label(cls, iso_value: int) -> str:
        """Get human-readable label for ISO value.
        
        Args:
            iso_value: ISO value code
            
        Returns:
            Human-readable ISO label (e.g., "ISO 100")
        """
        try:
            # First try to use the EDSDK function if available
            return Iso.get_label(iso_value)
        except (NameError, AttributeError):
            # Fallback implementation
            if iso_value == cls.AUTO:
                return "ISO Auto"
                
            # Map codes to values
            iso_map = {
                cls.ISO_50: "ISO 50",
                cls.ISO_100: "ISO 100",
                cls.ISO_125: "ISO 125",
                cls.ISO_160: "ISO 160",
                cls.ISO_200: "ISO 200",
                cls.ISO_250: "ISO 250",
                cls.ISO_320: "ISO 320",
                cls.ISO_400: "ISO 400",
                cls.ISO_500: "ISO 500",
                cls.ISO_640: "ISO 640",
                cls.ISO_800: "ISO 800",
                cls.ISO_1000: "ISO 1000",
                cls.ISO_1250: "ISO 1250",
                cls.ISO_1600: "ISO 1600",
                cls.ISO_2000: "ISO 2000",
                cls.ISO_2500: "ISO 2500",
                cls.ISO_3200: "ISO 3200",
                cls.ISO_4000: "ISO 4000",
                cls.ISO_5000: "ISO 5000",
                cls.ISO_6400: "ISO 6400",
                cls.ISO_8000: "ISO 8000",
                cls.ISO_10000: "ISO 10000",
                cls.ISO_12800: "ISO 12800",
                cls.ISO_16000: "ISO 16000",
                cls.ISO_20000: "ISO 20000",
                cls.ISO_25600: "ISO 25600",
                cls.ISO_32000: "ISO 32000",
                cls.ISO_40000: "ISO 40000",
                cls.ISO_51200: "ISO 51200",
                cls.ISO_102400: "ISO 102400",
            }
            
            return iso_map.get(iso_value, f"ISO {iso_value}")


class ApertureSettings:
    """Aperture settings for Canon cameras."""
    
    # Common aperture values
    F1_0 = 0x00000008
    F1_2 = 0x0000000B
    F1_4 = 0x0000000D
    F1_6 = 0x00000010
    F1_8 = 0x00000013
    F2_0 = 0x00000015
    F2_2 = 0x00000018
    F2_5 = 0x0000001B
    F2_8 = 0x0000001D
    F3_2 = 0x00000020
    F3_5 = 0x00000023
    F4_0 = 0x00000025
    F4_5 = 0x00000028
    F5_0 = 0x0000002B
    F5_6 = 0x0000002D
    F6_3 = 0x00000030
    F7_1 = 0x00000033
    F8_0 = 0x00000035
    F9_0 = 0x00000038
    F10 = 0x0000003B
    F11 = 0x0000003D
    F13 = 0x00000040
    F14 = 0x00000043
    F16 = 0x00000045
    F18 = 0x00000048
    F20 = 0x0000004B
    F22 = 0x0000004D
    F25 = 0x00000050
    F29 = 0x00000053
    F32 = 0x00000055
    
    @classmethod
    def get_label(cls, av_value: int) -> str:
        """Get human-readable label for aperture value.
        
        Args:
            av_value: Aperture value code
            
        Returns:
            Human-readable aperture label (e.g., "f/2.8")
        """
        try:
            # First try to use the EDSDK function if available
            return Av.get_label(av_value)
        except (NameError, AttributeError):
            # Fallback implementation
            av_map = {
                cls.F1_0: "f/1.0",
                cls.F1_2: "f/1.2",
                cls.F1_4: "f/1.4",
                cls.F1_6: "f/1.6",
                cls.F1_8: "f/1.8",
                cls.F2_0: "f/2.0",
                cls.F2_2: "f/2.2",
                cls.F2_5: "f/2.5",
                cls.F2_8: "f/2.8",
                cls.F3_2: "f/3.2",
                cls.F3_5: "f/3.5",
                cls.F4_0: "f/4.0",
                cls.F4_5: "f/4.5",
                cls.F5_0: "f/5.0",
                cls.F5_6: "f/5.6",
                cls.F6_3: "f/6.3",
                cls.F7_1: "f/7.1",
                cls.F8_0: "f/8.0",
                cls.F9_0: "f/9.0",
                cls.F10: "f/10",
                cls.F11: "f/11",
                cls.F13: "f/13",
                cls.F14: "f/14",
                cls.F16: "f/16",
                cls.F18: "f/18",
                cls.F20: "f/20",
                cls.F22: "f/22",
                cls.F25: "f/25",
                cls.F29: "f/29",
                cls.F32: "f/32",
            }
            
            return av_map.get(av_value, f"f/{av_value}")


class ShutterSpeedSettings:
    """Shutter speed settings for Canon cameras."""
    
    # Common shutter speed values
    BULB = 0x0000000C
    SEC_30 = 0x00000010
    SEC_25 = 0x00000013
    SEC_20 = 0x00000015
    SEC_15 = 0x00000018
    SEC_13 = 0x0000001B
    SEC_10 = 0x0000001D
    SEC_8 = 0x00000020
    SEC_6 = 0x00000023
    SEC_5 = 0x00000025
    SEC_4 = 0x00000028
    SEC_3_2 = 0x0000002B
    SEC_3 = 0x0000002D
    SEC_2_5 = 0x00000030
    SEC_2 = 0x00000033
    SEC_1_6 = 0x00000035
    SEC_1_3 = 0x00000038
    SEC_1 = 0x0000003B
    SEC_0_8 = 0x0000003D
    SEC_0_6 = 0x00000040
    SEC_0_5 = 0x00000043
    SEC_0_4 = 0x00000045
    SEC_0_3 = 0x00000048
    SEC_1_4 = 0x0000004B
    SEC_1_5 = 0x0000004D
    SEC_1_6_2 = 0x00000050
    SEC_1_8 = 0x00000053
    SEC_1_10 = 0x00000055
    SEC_1_13 = 0x00000058
    SEC_1_15 = 0x0000005B
    SEC_1_20 = 0x0000005D
    SEC_1_25 = 0x00000060
    SEC_1_30 = 0x00000063
    SEC_1_40 = 0x00000065
    SEC_1_50 = 0x00000068
    SEC_1_60 = 0x0000006B
    SEC_1_80 = 0x0000006D
    SEC_1_100 = 0x00000070
    SEC_1_125 = 0x00000073
    SEC_1_160 = 0x00000075
    SEC_1_200 = 0x00000078
    SEC_1_250 = 0x0000007B
    SEC_1_320 = 0x0000007D
    SEC_1_400 = 0x00000080
    SEC_1_500 = 0x00000083
    SEC_1_640 = 0x00000085
    SEC_1_800 = 0x00000088
    SEC_1_1000 = 0x0000008B
    SEC_1_1250 = 0x0000008D
    SEC_1_1600 = 0x00000090
    SEC_1_2000 = 0x00000093
    SEC_1_2500 = 0x00000095
    SEC_1_3200 = 0x00000098
    SEC_1_4000 = 0x0000009B
    SEC_1_5000 = 0x0000009D
    SEC_1_6400 = 0x000000A0
    SEC_1_8000 = 0x000000A3
    
    @classmethod
    def get_label(cls, tv_value: int) -> str:
        """Get human-readable label for shutter speed value.
        
        Args:
            tv_value: Shutter speed value code
            
        Returns:
            Human-readable shutter speed label (e.g., "1/125")
        """
        try:
            # First try to use the EDSDK function if available
            return Tv.get_label(tv_value)
        except (NameError, AttributeError):
            # Fallback implementation
            tv_map = {
                cls.BULB: "Bulb",
                cls.SEC_30: "30\"",
                cls.SEC_25: "25\"",
                cls.SEC_20: "20\"",
                cls.SEC_15: "15\"",
                cls.SEC_13: "13\"",
                cls.SEC_10: "10\"",
                cls.SEC_8: "8\"",
                cls.SEC_6: "6\"",
                cls.SEC_5: "5\"",
                cls.SEC_4: "4\"",
                cls.SEC_3_2: "3.2\"",
                cls.SEC_3: "3\"",
                cls.SEC_2_5: "2.5\"",
                cls.SEC_2: "2\"",
                cls.SEC_1_6: "1.6\"",
                cls.SEC_1_3: "1.3\"",
                cls.SEC_1: "1\"",
                cls.SEC_0_8: "0.8\"",
                cls.SEC_0_6: "0.6\"",
                cls.SEC_0_5: "0.5\"",
                cls.SEC_0_4: "0.4\"",
                cls.SEC_0_3: "0.3\"",
                cls.SEC_1_4: "1/4",
                cls.SEC_1_5: "1/5",
                cls.SEC_1_6_2: "1/6",
                cls.SEC_1_8: "1/8",
                cls.SEC_1_10: "1/10",
                cls.SEC_1_13: "1/13",
                cls.SEC_1_15: "1/15",
                cls.SEC_1_20: "1/20",
                cls.SEC_1_25: "1/25",
                cls.SEC_1_30: "1/30",
                cls.SEC_1_40: "1/40",
                cls.SEC_1_50: "1/50",
                cls.SEC_1_60: "1/60",
                cls.SEC_1_80: "1/80",
                cls.SEC_1_100: "1/100",
                cls.SEC_1_125: "1/125",
                cls.SEC_1_160: "1/160",
                cls.SEC_1_200: "1/200",
                cls.SEC_1_250: "1/250",
                cls.SEC_1_320: "1/320",
                cls.SEC_1_400: "1/400",
                cls.SEC_1_500: "1/500",
                cls.SEC_1_640: "1/640",
                cls.SEC_1_800: "1/800",
                cls.SEC_1_1000: "1/1000",
                cls.SEC_1_1250: "1/1250",
                cls.SEC_1_1600: "1/1600",
                cls.SEC_1_2000: "1/2000",
                cls.SEC_1_2500: "1/2500",
                cls.SEC_1_3200: "1/3200",
                cls.SEC_1_4000: "1/4000",
                cls.SEC_1_5000: "1/5000",
                cls.SEC_1_6400: "1/6400",
                cls.SEC_1_8000: "1/8000",
            }
            
            return tv_map.get(tv_value, f"TV {tv_value}") 