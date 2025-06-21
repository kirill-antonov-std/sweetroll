import pytest

from camera_capture_config import CameraCaptureConfig, CaptureTrigger

from helpers import set_env
from conftest import *

default_env_vars_timer = {
    "CAMERA_HANDLE": "usb_camera",
    "CAPTURE_TRIGGER": "timer",
    "CAPTURE_INTERVAL_S": "120",
    "CAPTURE_TRIGGER_DI": "12",
    "IMAGES_DIR": "/tmp/images"
}

default_env_vars_di = {
    "CAMERA_HANDLE": "usb_camera",
    "CAPTURE_TRIGGER": "di",
    "CAPTURE_INTERVAL_S": "120",
    "CAPTURE_TRIGGER_DI": "12",
    "IMAGES_DIR": "/tmp/images"
}

def test_valid_env_vars_timer():
    set_env(default_env_vars_timer)
    config = CameraCaptureConfig.from_env()
    assert config.camera_handle == default_env_vars_timer["CAMERA_HANDLE"]
    assert config.capture_trigger is CaptureTrigger(default_env_vars_timer["CAPTURE_TRIGGER"])
    assert config.capture_interval_s == int(default_env_vars_timer["CAPTURE_INTERVAL_S"])
    assert config.capture_trigger_di is None
    assert config.images_dir == default_env_vars_timer["IMAGES_DIR"]

def test_valid_env_vars_di():
    set_env(default_env_vars_di)
    config = CameraCaptureConfig.from_env()
    assert config.camera_handle == default_env_vars_di["CAMERA_HANDLE"]
    assert config.capture_trigger is CaptureTrigger(default_env_vars_di["CAPTURE_TRIGGER"])
    assert config.capture_interval_s is None
    assert config.capture_trigger_di == int(default_env_vars_di["CAPTURE_TRIGGER_DI"])
    assert config.images_dir == default_env_vars_di["IMAGES_DIR"]

def test_missing_camera_handle():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAMERA_HANDLE"}
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAMERA_HANDLE"):
        CameraCaptureConfig.from_env()

def test_empty_camera_handle():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAMERA_HANDLE"}
    env_vars["CAMERA_HANDLE"] = ""
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAMERA_HANDLE"):
        CameraCaptureConfig.from_env()

def test_random_camera_handle():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAMERA_HANDLE"}
    env_vars["CAMERA_HANDLE"] = "abcd1234"
    set_env(env_vars)
    config = CameraCaptureConfig.from_env()
    assert config.camera_handle == env_vars["CAMERA_HANDLE"]

def test_missing_capture_trigger():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_TRIGGER"}
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_TRIGGER"):
        CameraCaptureConfig.from_env()

def test_empty_capture_trigger():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_TRIGGER"}
    env_vars["CAPTURE_TRIGGER"] = ""
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_TRIGGER"):
        CameraCaptureConfig.from_env()

def test_none_capture_trigger():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_TRIGGER"}
    env_vars["CAPTURE_TRIGGER"] = "None"
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_TRIGGER"):
        CameraCaptureConfig.from_env()

def test_missing_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    set_env(env_vars)
    config = CameraCaptureConfig.from_env()
    assert config.capture_interval_s == 60

def test_empty_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    env_vars["CAPTURE_INTERVAL_S"] = ""
    set_env(env_vars)
    with pytest.raises(TypeError, match="CAPTURE_INTERVAL_S"):
        CameraCaptureConfig.from_env()

def test_string_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    env_vars["CAPTURE_INTERVAL_S"] = "abcd1234"
    set_env(env_vars)
    with pytest.raises(TypeError, match="CAPTURE_INTERVAL_S"):
        CameraCaptureConfig.from_env()

def test_negative_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    env_vars["CAPTURE_INTERVAL_S"] = str(-45)
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_INTERVAL_S"):
        CameraCaptureConfig.from_env()

def test_zero_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    env_vars["CAPTURE_INTERVAL_S"] = str(0)
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_INTERVAL_S"):
        CameraCaptureConfig.from_env()

def test_one_second_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    env_vars["CAPTURE_INTERVAL_S"] = str(1)
    set_env(env_vars)
    config = CameraCaptureConfig.from_env()
    assert config.capture_interval_s == int(env_vars["CAPTURE_INTERVAL_S"])

def test_one_day_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    env_vars["CAPTURE_INTERVAL_S"] = str(24 * 60 * 60)
    set_env(env_vars)
    config = CameraCaptureConfig.from_env()
    assert config.capture_interval_s == int(env_vars["CAPTURE_INTERVAL_S"])

def test_one_day_plus_second_capture_interval_s():
    env_vars = {key: value for key, value in default_env_vars_timer.items() if key != "CAPTURE_INTERVAL_S"}
    env_vars["CAPTURE_INTERVAL_S"] = str(24 * 60 * 60 + 1)
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_INTERVAL_S"):
        CameraCaptureConfig.from_env()

def test_missing_capture_trigger_di():
    env_vars = {key: value for key, value in default_env_vars_di.items() if key != "CAPTURE_TRIGGER_DI"}
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_TRIGGER_DI"):
        CameraCaptureConfig.from_env()

def test_empty_capture_trigger_di():
    env_vars = {key: value for key, value in default_env_vars_di.items() if key != "CAPTURE_TRIGGER_DI"}
    env_vars["CAPTURE_TRIGGER_DI"] = ""
    set_env(env_vars)
    with pytest.raises(TypeError, match="CAPTURE_TRIGGER_DI"):
        CameraCaptureConfig.from_env()

def test_string_capture_trigger_di():
    env_vars = {key: value for key, value in default_env_vars_di.items() if key != "CAPTURE_TRIGGER_DI"}
    env_vars["CAPTURE_TRIGGER_DI"] = "abcd1234"
    set_env(env_vars)
    with pytest.raises(TypeError, match="CAPTURE_TRIGGER_DI"):
        CameraCaptureConfig.from_env()

def test_negative_capture_trigger_di():
    env_vars = {key: value for key, value in default_env_vars_di.items() if key != "CAPTURE_TRIGGER_DI"}
    env_vars["CAPTURE_TRIGGER_DI"] = str(-1)
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_TRIGGER_DI"):
        CameraCaptureConfig.from_env()

def test_zero_capture_trigger_di():
    env_vars = {key: value for key, value in default_env_vars_di.items() if key != "CAPTURE_TRIGGER_DI"}
    env_vars["CAPTURE_TRIGGER_DI"] = str(0)
    set_env(env_vars)
    config = CameraCaptureConfig.from_env()
    assert config.capture_trigger_di == int(env_vars["CAPTURE_TRIGGER_DI"])

def test_26_capture_trigger_di():
    env_vars = {key: value for key, value in default_env_vars_di.items() if key != "CAPTURE_TRIGGER_DI"}
    env_vars["CAPTURE_TRIGGER_DI"] = str(26)
    set_env(env_vars)
    config = CameraCaptureConfig.from_env()
    assert config.capture_trigger_di == int(env_vars["CAPTURE_TRIGGER_DI"])

def test_27_capture_trigger_di():
    env_vars = {key: value for key, value in default_env_vars_di.items() if key != "CAPTURE_TRIGGER_DI"}
    env_vars["CAPTURE_TRIGGER_DI"] = str(27)
    set_env(env_vars)
    with pytest.raises(ValueError, match="CAPTURE_TRIGGER_DI"):
        CameraCaptureConfig.from_env()

if __name__ == "__main__":
    pytest.main()