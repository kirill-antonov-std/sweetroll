from datetime import datetime
from typing import Optional
from enum import Enum
import time
import cv2
import os

class CameraAdapter():

    FRAME_RATE = 1 / 60

    class CaptureTrigger(Enum):
        TIMER_TRIGGER = 0
        DI_TRIGGER = 1

    def __init__(self, camera_handle: str, capture_trigger: CaptureTrigger):
        self.camera_capture: cv2.VideoCapture = self._create_camera_capture(camera_handle=camera_handle, 
                                                                            capture_trigger=capture_trigger)
        self.CAMERA_HANDLE: str = camera_handle
        self.CAPTURE_TRIGGER: CameraAdapter.CaptureTrigger = capture_trigger
        self.CAPTURE_INTERVAL_MS: int = None
        self.CAPTURE_TRIGGER_DI: int = None

    def _create_camera_capture(self, camera_handle: str, 
                               capture_trigger: CaptureTrigger) -> Optional[cv2.VideoCapture]:
        cap: Optional[cv2.VideoCapture] = None
        try:
            cap = cv2.VideoCapture(camera_handle)
        except:
            pass
        if not cap.isOpened():
            cap = None
        return cap
    
    def _release_camera_capture(self) -> bool:
        ret_val = False
        self.camera_capture.release()
        if not self.camera_capture.isOpened():
            ret_val = True
        return ret_val
    
    def _check_trigger(self) -> bool:
        return True
    
    def _capture_loop(self) -> None:
        while True:
            if self._check_trigger():
                self.get_image()
            time.sleep(self.FRAME_RATE)
    
    def get_image(self) -> Optional[cv2.typing.MatLike]:
        ret_val: Optional[cv2.typing.MatLike] = None
        status, frame = self.camera_capture.read()
        if status is True:
            ret_val = frame
        return ret_val
    
    def close(self) -> bool:
        self._release_camera_capture()

if __name__ == "__main__":

    CAMERA_DEVICE = os.getenv("CAMERA_DEVICE")
    CAPTURE_INTERVAL = int(os.getenv("CAPTURE_INTERVAL", 60))
    SAVE_DIR = os.getenv("SAVE_DIR")
    os.makedirs(SAVE_DIR, exist_ok=True)