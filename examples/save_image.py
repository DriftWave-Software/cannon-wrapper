import os
import time
import uuid

import edsdk
from edsdk import (
    CameraCommand,
    ObjectEvent,
    PropID,
    FileCreateDisposition,
    Access,
    SaveTo,
    EdsObject,
    PropertyEvent
)
import cv2
import numpy as np

if os.name == "nt":
    # If you're using the EDSDK on Windows,
    # you have to have a Windows message loop in your main thread,
    # otherwise callbacks won't happen.
    # (This is because the EDSDK uses the obsolete COM STA threading model
    # instead of real threads.)
    import pythoncom


def save_image(object_handle: EdsObject, save_to: str) -> int:
    try:
        dir_item_info = edsdk.GetDirectoryItemInfo(object_handle)
        # Attempt to get object format, handle unknowns gracefully
        object_format = dir_item_info.get("objectFormat")
        if object_format is not None:
            try:
                # Try to map to known format (if your wrapper provides a mapping)
                format_name = str(object_format)
            except Exception:
                format_name = f"Unknown ObjectFormat: {object_format}"
                print(format_name)
        out_stream = edsdk.CreateFileStream(
            os.path.join(save_to, str(uuid.uuid4()) + ".raw"),
            FileCreateDisposition.CreateAlways,
            Access.ReadWrite)
        edsdk.Download(object_handle, dir_item_info["size"], out_stream)
        edsdk.DownloadComplete(object_handle)
    except Exception as e:
        print(f"Error in save_image: {e}")
    return 0


def callback_property(event: PropertyEvent, property_id: PropID, parameter: int) -> int:
    print("event: ", event)
    print("Property changed:", property_id)
    print("Parameter:", parameter)
    return 0


def callback_object(event: ObjectEvent, object_handle: EdsObject) -> int:
    print("event: ", event, "object_handle:", object_handle)
    if event == ObjectEvent.DirItemRequestTransfer:
        save_image(object_handle, ".")
    return 0


def start_live_view(cam, retries=5, delay=1.0):
    # Enable live view mode (EVF) with retry on DEVICE_BUSY
    for attempt in range(retries):
        try:
            # Set EVF mode ON
            edsdk.SetPropertyData(cam, PropID.Evf_Mode, 0, 1)  # 1 = ON
            # Set output device to PC
            edsdk.SetPropertyData(cam, PropID.Evf_OutputDevice, 0, 1)  # 1 = PC
            print("Live view (EVF) started successfully.")
            return
        except edsdk.EdsError as e:
            if str(e) == "EDS_ERR_DEVICE_BUSY":
                print(f"Camera busy, retrying live view in {delay} seconds... (attempt {attempt+1}/{retries})")
                time.sleep(delay)
            else:
                print(f"Failed to start live view: {e}")
                break
    else:
        print("Failed to start live view after several attempts. Camera may be unstable.")


def stop_live_view(cam):
    try:
        edsdk.SetPropertyData(cam, PropID.Evf_OutputDevice, 0, 0)  # 0 = None
        edsdk.SetPropertyData(cam, PropID.Evf_Mode, 0, 0)  # 0 = OFF
        print("Live view (EVF) stopped.")
    except Exception as e:
        print(f"Failed to stop live view: {e}")


def download_live_view_frame(cam, show=True, save_to=None):
    # Create EvfImageRef
    evf_image = edsdk.CreateEvfImageRef(cam)
    try:
        edsdk.DownloadEvfImage(cam, evf_image)
        # Get image data
        data = edsdk.GetImageData(evf_image)
        if save_to:
            # Save to file (as .jpg or .raw depending on camera)
            filename = os.path.join(save_to, str(uuid.uuid4()) + "_liveview.jpg")
            with open(filename, "wb") as f:
                f.write(data)
            print(f"Saved live view frame to {filename}")
        if show:
            # Decode JPEG and show using OpenCV
            arr = np.frombuffer(data, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is not None:
                cv2.imshow("Live View", img)
                cv2.waitKey(1)
            else:
                print("Failed to decode live view frame.")
    except Exception as e:
        print(f"Live view frame error: {e}")
    finally:
        edsdk.Release(evf_image)


if __name__ == "__main__":
    edsdk.InitializeSDK()
    cam_list = edsdk.GetCameraList()
    nr_cameras = edsdk.GetChildCount(cam_list)

    if nr_cameras == 0:
        print("No cameras connected")
        exit(1)

    cam = edsdk.GetChildAtIndex(cam_list, 0)
    edsdk.OpenSession(cam)
    edsdk.SetObjectEventHandler(cam, ObjectEvent.All, callback_object)
    edsdk.SetPropertyData(cam, PropID.SaveTo, 0, SaveTo.Host)
    print(edsdk.GetPropertyData(cam, PropID.SaveTo, 0))

    # Sets HD Capacity to an arbitrary big value
    edsdk.SetCapacity(
        cam, {"reset": True, "bytesPerSector": 512, "numberOfFreeClusters": 2147483647}
    )
    print(edsdk.GetDeviceInfo(cam))

    # Start live view
    start_live_view(cam)
    print("Live view started. Waiting for camera to enter EVF mode...")
    time.sleep(3)  # Give camera more time to enter live view
    print("Press 'q' in the window to quit live view.")
    max_retries = 20
    retries = 0
    while True:
        try:
            download_live_view_frame(cam, show=True)
            retries = 0  # Reset on success
        except edsdk.EdsError as e:
            if str(e) == "EDS_ERR_INVALID_HANDLE":
                retries += 1
                if retries > max_retries:
                    print("Camera not ready for live view frame after multiple attempts. Exiting live view.")
                    break
                print("Camera not ready for live view frame, retrying in 0.5s...")
                time.sleep(0.5)
                continue
            else:
                print(f"Live view error: {e}")
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    stop_live_view(cam)

    edsdk.SendCommand(cam, CameraCommand.TakePicture, 0)

    time.sleep(4)
    if os.name == "nt":
        pythoncom.PumpWaitingMessages()
    edsdk.TerminateSDK()
