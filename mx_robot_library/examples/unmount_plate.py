from time import sleep

from mx_robot_library.client import Client
from mx_robot_library.schemas.common.path import RobotPaths
from mx_robot_library.schemas.common.sample import Plate


# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Unmount plate from goni
robot.trajectory.plate.unmount()

# Wait for robot to start running the plate unmount path
while robot.status.state.path != RobotPaths.GET_PLATE:
    sleep(0.5)

# Wait for robot to finish running the path
while robot.status.state.path != RobotPaths.UNDEFINED:
    sleep(0.5)

assert robot.status.state.goni_plate is None
