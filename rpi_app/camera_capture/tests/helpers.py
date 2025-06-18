from camera_capture import CameraAdapter
import os

def set_env(base_env):
    os.environ.update(base_env)

class CameraFake(CameraAdapter):
    def __init__(self):
        pass