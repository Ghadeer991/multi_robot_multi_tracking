"""Main tracking loop and orchestration."""
import cv2

from .assignment import AssignmentState, assignFirstTarget, assignSecondTarget, computeDistances
from .aruco_tracking import detectRobots
from .config import loadDefaultConfig
from .geometry import calculateAngle, drawLine
from .robot_control import connectRobot, decideCommand, sendCommand
from .target_tracking import TargetTracker
from .vision import fetchFrame, resizeFrame


def handleTarget(
    frame,
    label,
    targetCenter,
    attachKey,
    distances,
    robotCenters,
    robotFronts,
    robotSockets,
    distanceThreshold,
):
    """Send commands for a target assigned to a robot."""
    if attachKey is None or distances is None:
        return
    robotIndex = 0 if attachKey == "first" else 1
    robotCenter = robotCenters[robotIndex]
    robotFront = robotFronts[robotIndex]
    drawLine(frame, robotCenter, targetCenter, (0, 0, 200))
    distance = distances[robotIndex]
    angle = calculateAngle(robotCenter, targetCenter, robotFront)
    command = decideCommand(angle, distance, distanceThreshold)
    sendCommand(robotSockets[robotIndex], command)
    print(label, attachKey, "d = ", distance, "a = ", angle)


def runApp():
    """Run the multi-robot multi-target tracking loop."""
    config = loadDefaultConfig()
    font = cv2.FONT_HERSHEY_PLAIN
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    parameters = cv2.aruco.DetectorParameters()
    tracker = TargetTracker(config.tracking.trackerType)
    state = AssignmentState()

    robot1Socket = connectRobot(config.network.robot1Ip, config.network.port)
    robot2Socket = connectRobot(config.network.robot2Ip, config.network.port)
    robotSockets = [robot1Socket, robot2Socket]

    try:
        while True:
            timer = cv2.getTickCount()
            frame = fetchFrame(config.network.cameraUrl)
            frame = resizeFrame(frame, config.tracking.frameScale)

            targetCenters = tracker.update(frame, font, config.tracking.maxTargets)
            robots = detectRobots(frame, arucoDict, parameters, config.camera, font)
            robotCenters = [robots[1][0], robots[2][0]]
            robotFronts = [robots[1][1], robots[2][1]]

            for robotCenter in robotCenters:
                for targetCenter in targetCenters:
                    drawLine(frame, robotCenter, targetCenter)

            firstDistances = computeDistances(targetCenters[0], robotCenters)
            secondDistances = computeDistances(targetCenters[1], robotCenters)

            assignFirstTarget(state, firstDistances)
            assignSecondTarget(state, secondDistances)

            handleTarget(
                frame,
                "1",
                targetCenters[0],
                state.firstTargetAttach,
                firstDistances,
                robotCenters,
                robotFronts,
                robotSockets,
                config.tracking.distanceThreshold,
            )
            handleTarget(
                frame,
                "2",
                targetCenters[1],
                state.secondTargetAttach,
                secondDistances,
                robotCenters,
                robotFronts,
                robotSockets,
                config.tracking.distanceThreshold,
            )

            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            cv2.putText(frame, "FPS : " + str(int(fps)), (10, 20), font, 1, (0, 50, 255), 2)
            cv2.imshow("Frame", frame)

            key = cv2.waitKey(30) & 0xFF
            if key == ord("t"):
                roi = cv2.selectROI("Frame", frame)
                tracker.addTarget(frame, roi)
            if key == 27:
                break
    finally:
        sendCommand(robot1Socket, "stop")
        sendCommand(robot2Socket, "stop")
        cv2.destroyAllWindows()



