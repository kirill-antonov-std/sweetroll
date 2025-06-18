from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from threading import Thread
from typing import Optional
from enum import Enum
import logging
import time
import cv2
import sys
import os

from camera_capture_config import CameraCaptureConfig, CaptureTrigger

logger = logging.getLogger(__name__)

class CameraAdapter():

    FRAME_RATE = 1 / 60

    def __init__(self, config: CameraCaptureConfig):
        self.camera_capture: cv2.VideoCapture = self._create_camera_capture(
            camera_handle=config.camera_handle, 
            capture_trigger=config.capture_trigger
        )
        self.CAMERA_HANDLE: str = config.camera_handle
        self.CAPTURE_TRIGGER: CaptureTrigger = config.capture_trigger
        self.CAPTURE_INTERVAL_MS: int = None
        self.CAPTURE_TRIGGER_DI: int = None
        self._capturing_tread: Thread = Thread(target=self._capture_loop)

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
    
    def start_continuous_capturing(self) -> bool:
        self._capturing_tread.start()

    def stop_continuous_capturing(self) -> bool:
        self._release_camera_capture()

def run_module() -> None:        
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    config = CameraCaptureConfig.from_env()
    if not os.path.exists(config.images_dir):
        os.makedirs(name=config.images_dir)
        logger.info(f"The directory for images is created by path {config.images_dir}")

    camera = CameraAdapter(config=config)
    camera.start_continuous_capturing()

    while True:
        time.sleep(0.5)

if __name__ == "__main__":
    run_module()