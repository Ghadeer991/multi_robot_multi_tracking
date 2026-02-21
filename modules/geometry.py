"""Geometry helpers for angles, distances, and drawing."""
import math
import cv2


def drawLine(frame, point1, point2, color=(200, 0, 200)):
    """Draw a line if both points are available."""
    if point1 is None or point2 is None:
        return
    cv2.line(frame, point1, point2, color, 2)


def calculateDistance(point1, point2):
    """Return the pixel distance between two points."""
    if point1 is None or point2 is None:
        return None
    return int(math.sqrt((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2))


def calculateAngle(origin, target, front):
    """Return the angle between target and front vectors in degrees."""
    if origin is None or target is None or front is None:
        return None
    a = target[0] - origin[0]
    b = target[1] - origin[1]
    angleA = round(math.degrees(math.atan2(a, b)))
    c = front[0] - origin[0]
    d = front[1] - origin[1]
    angleB = round(math.degrees(math.atan2(c, d)))
    angle = angleA - angleB
    if angle < 0:
        angle += 360
    return angle




