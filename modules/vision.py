"""Frame acquisition and resizing helpers."""
import numpy as np
import cv2
import requests


def fetchFrame(cameraUrl):
    """Fetch a single frame from the camera URL."""
    response = requests.get(cameraUrl, timeout=5)
    response.raise_for_status()
    data = np.frombuffer(response.content, dtype=np.uint8)
    return cv2.imdecode(data, -1)


def resizeFrame(frame, scale):
    """Resize a frame by a uniform scale factor."""
    return cv2.resize(frame, None, fx=scale, fy=scale)




