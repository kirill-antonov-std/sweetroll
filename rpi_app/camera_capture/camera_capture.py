from __future__ import annotations
from datetime import datetime
from typing import Optional
import threading
import logging
import signal
import time
import cv2
import sys
import os

from camera_capture_config import CameraCaptureConfig, CaptureTrigger, TRIGGER_CHECKERS

logger = logging.getLogger(__name__)

class CameraAdapter():

    FRAME_RATE_S = 1 / 60

    def __init__(self, config: CameraCaptureConfig):
        self.camera_capture: cv2.VideoCapture = self._create_camera_capture(
            camera_handle=config.camera_handle
        )
        self.CONFIG = config
        self.CAMERA_HANDLE: str = config.camera_handle
        self.CAPTURE_TRIGGER: CaptureTrigger = config.capture_trigger
        if config.capture_interval_s is not None:
            self.CAPTURE_INTERVAL_S: int = config.capture_interval_s
        if config.capture_trigger_di is not None:
            self.CAPTURE_TRIGGER_DI: int = config.capture_trigger_di
        self.IMAGES_DIR = config.images_dir
        self._trigger_checker = TRIGGER_CHECKERS[self.CAPTURE_TRIGGER]
        self._capturing_thread: threading.Thread = threading.Thread(target=self._capture_loop)
        self._stop_event = threading.Event()

    def _create_camera_capture(self, camera_handle: str) -> Optional[cv2.VideoCapture]:
        cap: Optional[cv2.VideoCapture] = None
        try:
            cap = cv2.VideoCapture(camera_handle)
        except Exception as e:
            raise RuntimeError(f"Failed to create the video capture ({camera_handle})") from e
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open the video capture ({camera_handle})")
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
        while not self._stop_event.is_set():
            if self._trigger_checker(self.CONFIG):
                image = self.get_image()
                ts = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                image_name = f"{self.IMAGES_DIR}/cap_{ts}.jpg"
                status = cv2.imwrite(image_name, image)
                if status:
                    logging.info(f"The image {image_name} has successfully captured")
                else:
                    logging.warning(f"Failed to save the image into the {self.IMAGES_DIR} folder")

            time.sleep(self.FRAME_RATE_S)
    
    def get_image(self) -> Optional[cv2.typing.MatLike]:
        ret_val: Optional[cv2.typing.MatLike] = None
        status, frame = self.camera_capture.read()
        if status is True:
            ret_val = frame
        else:
            if self.CAMERA_HANDLE.endswith((".mp4", ".avi")):
                self.camera_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return ret_val
    
    def start_continuous_capturing(self) -> bool:
        self._capturing_thread.start()
        return self._capturing_thread.is_alive()

    def stop_continuous_capturing(self) -> bool:
        self._stop_event.set()
        self._capturing_thread.join()
        return self._release_camera_capture()

def run_module() -> None:        
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    shutdown_event = threading.Event()
    def handle_shutdown(signum, frame):
        logger.info(f"Received signal {signum}. Shutting down...")
        shutdown_event.set()
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    config = CameraCaptureConfig.from_env()
    if not os.path.exists(config.images_dir):
        os.makedirs(name=config.images_dir)
        logger.info(f"The directory for images is created by path {config.images_dir}")

    camera = CameraAdapter(config=config)
    camera.start_continuous_capturing()

    while not shutdown_event.is_set():
        time.sleep(0.5)
    camera.stop_continuous_capturing()

if __name__ == "__main__":
    run_module()