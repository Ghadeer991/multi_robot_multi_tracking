"""Target tracking via OpenCV MultiTracker."""
import cv2
import numpy as np


trackerFactories = {
    "csrt": cv2.legacy.TrackerCSRT_create,
    "kcf": cv2.legacy.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.legacy.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create,
}


class TargetTracker:
    """OpenCV MultiTracker wrapper for interactive target selection."""

    def __init__(self, trackerType):
        if trackerType not in trackerFactories:
            raise ValueError(f"Unsupported tracker type: {trackerType}")
        self.trackerType = trackerType
        self.multiTracker = cv2.legacy.MultiTracker_create()

    def addTarget(self, frame, roi):
        """Add a new ROI target to the tracker."""
        tracker = trackerFactories[self.trackerType]()
        self.multiTracker.add(tracker, frame, roi)

    def update(self, frame, font, maxTargets=2):
        """Update trackers, draw labels, and return target centers."""
        success, boxes = self.multiTracker.update(frame)
        targetCenters = [None] * maxTargets
        if not success:
            return targetCenters

        for i, box in enumerate(boxes):
            if i >= maxTargets:
                break
            x, y, w, h = [int(v) for v in box]
            center = (x + w // 2, y + h // 2)
            targetCenters[i] = center
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 100, 255), 2)
            point1 = (x + w // 2, y - 10)
            point2 = (x + w // 2 - 10, y - 20)
            point3 = (x + w // 2 + 10, y - 20)
            trianglePoints = np.array([point1, point2, point3])
            cv2.drawContours(frame, [trianglePoints], 0, (0, 0, 255), -1)
            cv2.putText(frame, str(i + 1), (x, y - 3), font, 1, (50, 50, 255), 2)
            cv2.circle(frame, center, 3, (255, 0, 0), -1)

        return targetCenters




