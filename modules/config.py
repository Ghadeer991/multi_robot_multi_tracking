"""Configuration models and defaults for camera, network, and tracking."""
import numpy as np
from dataclasses import dataclass


@dataclass
class CameraConfig:
    matrix: np.ndarray
    distCoeffs: np.ndarray
    markerSize: int


@dataclass
class NetworkConfig:
    robot1Ip: str
    robot2Ip: str
    port: int
    cameraUrl: str


@dataclass
class TrackingConfig:
    distanceThreshold: int
    frameScale: float
    trackerType: str
    maxTargets: int = 2


@dataclass
class AppConfig:
    camera: CameraConfig
    network: NetworkConfig
    tracking: TrackingConfig


def loadDefaultConfig():
    """Load default configuration values."""
    camera = CameraConfig(
        matrix=np.array(
            [[1056.288, 2.4753, 286.309], [0.0, 1064.736, 297.475], [0.0, 0.0, 1.0]],
            dtype=float,
        ),
        distCoeffs=np.array([[0.0, 0.0, 0.0, 0.0, 0.0]]),
        markerSize=8,
    )
    network = NetworkConfig(
        robot1Ip="192.168.43.185",
        robot2Ip="192.168.43.22",
        port=8080,
        cameraUrl="http://192.168.43.1:8080/shot.jpg",
    )
    tracking = TrackingConfig(
        distanceThreshold=150,
        frameScale=0.5,
        trackerType="tld",
    )
    return AppConfig(camera=camera, network=network, tracking=tracking)



