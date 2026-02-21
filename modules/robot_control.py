"""Robot socket control and motion decision logic."""
import socket


def connectRobot(ip, port):
    """Create and connect a robot socket."""
    sock = socket.socket()
    sock.connect((ip, port))
    return sock


def sendCommand(sock, command):
    """Send a single command to a robot."""
    message = f"{command}\n"
    sock.send(message.encode())


def decideCommand(angle, distance, distanceThreshold):
    """Decide a motion command based on angle and distance."""
    if angle is None or distance is None or distance >= 100000:
        return "stop"
    if angle <= 20 or angle >= 340:
        if distance < distanceThreshold:
            return "stop"
        return "forward"
    if 20 < angle < 180:
        return "left"
    if 180 <= angle < 340:
        return "right"
    return "stop"




