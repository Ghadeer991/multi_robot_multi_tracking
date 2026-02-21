"""ArUco marker detection and robot pose extraction."""
import cv2
import numpy as np


def detectRobots(frame, arucoDict, parameters, cameraConfig, font):
    """Detect ArUco markers and return robot centers/fronts by ID."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    markerCorners, markerIds, _ = cv2.aruco.detectMarkers(
        gray, arucoDict, parameters=parameters
    )
    robots = {1: (None, None), 2: (None, None)}

    if markerCorners:
        cv2.aruco.estimatePoseSingleMarkers(
            markerCorners,
            cameraConfig.markerSize,
            cameraConfig.matrix,
            cameraConfig.distCoeffs,
        )
        for markerId, markerCorner in zip(markerIds, markerCorners):
            cv2.polylines(frame, np.int32([markerCorner]), True, (0, 255, 0), 2)
            markerCorner = markerCorner.reshape(4, 2).astype(int)
            topRight = markerCorner[0].ravel()
            topLeft = markerCorner[1].ravel()
            bottomRight = markerCorner[2].ravel()
            front = (topRight + topLeft) // 2
            center = (topRight + bottomRight) // 2
            markerIndex = int(markerId[0])
            cv2.putText(frame, f"id: {markerIndex}", tuple(topRight), font, 1, (200, 100, 50), 2)
            cv2.arrowedLine(frame, tuple(center), tuple(front), (0, 255, 255), 2)
            if markerIndex in robots:
                robots[markerIndex] = (tuple(center), tuple(front))

    return robots



