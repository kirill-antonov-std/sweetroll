from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from enum import Enum
import logging
import os

logger = logging.getLogger(__name__)

class CaptureTrigger(Enum):
    UNKNOWN = None
    TIMER_TRIGGER = "timer"
    DI_TRIGGER = "di"

@dataclass
class CameraCaptureConfig:
    camera_handle: Optional[str] = None
    capture_trigger: CaptureTrigger = CaptureTrigger.UNKNOWN
    capture_interval_s: Optional[int] = 60
    capture_trigger_di: Optional[int] = None
    images_dir: str = "/data"

    @staticmethod
    def from_env() -> CameraCaptureConfig:
        camera_handle = CameraCaptureConfig._get_camera_handle()
        capture_trigger = CameraCaptureConfig._get_capture_trigger()
        capture_interval_s = None
        capture_trigger_di = None
        if capture_trigger is CaptureTrigger.TIMER_TRIGGER:
            capture_interval_s = CameraCaptureConfig._get_capture_interval_s()
        elif capture_trigger is CaptureTrigger.DI_TRIGGER:
            capture_trigger_di = CameraCaptureConfig._get_capture_trigger_di()
        images_dir = CameraCaptureConfig._get_images_dir()
        
        return CameraCaptureConfig(
            camera_handle=camera_handle, 
            capture_trigger=capture_trigger,
            capture_interval_s=capture_interval_s,
            capture_trigger_di=capture_trigger_di,
            images_dir=images_dir
        )
    
    @staticmethod
    def _get_camera_handle() -> str:
        env_var = os.getenv("CAMERA_HANDLE")
        if env_var is None or env_var == "":
            msg = "Missing required env variable: CAMERA_HANDLE"
            logger.error(msg)
            raise ValueError(msg)
        return env_var
    
    @staticmethod
    def _get_capture_trigger() -> CaptureTrigger:
        env_var = os.getenv("CAPTURE_TRIGGER")
        if env_var is None:
            msg = "Missing required env variable: CAPTURE_TRIGGER"
            logger.error(msg)
            raise ValueError(msg)
        if env_var not in [trigger.value for trigger in CaptureTrigger]:
            msg = f"Provided env variable CAPTURE_TRIGGER value ({env_var}) is not supported"
            logger.error(msg)
            raise ValueError(msg)
        return CaptureTrigger(env_var)
    
    @staticmethod
    def _get_capture_interval_s() -> int:
        env_var = os.getenv("CAPTURE_INTERVAL_S")
        if env_var is None:
            msg = ("Missing optional env variable: CAPTURE_INTERVAL_S; " + \
                   f"default value is used ({CameraCaptureConfig.capture_interval_s})")
            logger.warning(msg)
            env_var = CameraCaptureConfig.capture_interval_s
        else:
            try:
                env_var = int(env_var)
            except:
                msg = (f"Provided env variable CAPTURE_INTERVAL_S value ({env_var}) is not valid; " +  \
                       "must be integer")
                logger.error(msg)
                raise TypeError(msg)
            max_value = 24 * 60 * 60
            if not (env_var > 0 and env_var <= max_value):
                msg = (f"Provided env variable CAPTURE_INTERVAL_S value ({env_var}) is not valid; " +  \
                       f"must be within the range from 1 to {max_value} (24 hours)")
                logger.error(msg)
                raise ValueError(msg)
        return env_var
    
    @staticmethod
    def _get_capture_trigger_di() -> int:
        env_var = os.getenv("CAPTURE_TRIGGER_DI")
        if env_var is None:
            msg = "Missing required env variable: CAPTURE_TRIGGER_DI"
            logger.error(msg)
            raise ValueError(msg)
        else:
            try:
                env_var = int(env_var)
            except:
                msg = (f"Provided env variable CAPTURE_TRIGGER_DI value ({env_var}) is not valid; " +  \
                    "must be integer")
                logger.error(msg)
                raise TypeError(msg)
            max_value = 26
            if not (env_var >= 0 and env_var <= max_value):
                msg = (f"Provided env variable CAPTURE_TRIGGER_DI value ({env_var}) is not valid; " +  \
                    f"must be within the range from 0 to {max_value}")
                logger.error(msg)
                raise ValueError(msg)
        return env_var
    
    @staticmethod
    def _get_images_dir() -> str:
        env_var = os.getenv("IMAGES_DIR")
        if env_var is None:
            msg = "Missing required env variable: IMAGES_DIR"
            logger.error(msg)
            raise ValueError(msg)
        return env_var