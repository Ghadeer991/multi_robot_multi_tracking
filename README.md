# Multi-Robot Multi-Target Tracking

This folder contains the modularized version of the original multi-robot tracking project.

## Contents
- `RobotCode.ino`: ESP8266 robot firmware.
- `main.py`: Entry point for the Python tracking system.
- `modules/`: Modular Python implementation.

## Setup
1. Install dependencies:
   - Python packages: `opencv-python`, `opencv-contrib-python`, `numpy`, `requests`
2. Update IPs and ports in `modules/config.py` to match your robots and camera.
3. Run the tracker:
   - `python main.py`

## Controls
- `t`: Select and add a target ROI.
- `Esc`: Exit the loop and stop both robots.

## Notes
- ArUco IDs `1` and `2` are mapped to robot 1 and robot 2.
- Distance threshold defaults to 150 pixels.
