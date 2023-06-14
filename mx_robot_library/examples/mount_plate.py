from time import sleep

from mx_robot_library.client import Client
from mx_robot_library.schemas.common.path import RobotPaths
from mx_robot_library.schemas.common.sample import Plate

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

PLATE_TO_MOUNT = Plate(id=1)

# Mount plate from position "1"
robot.trajectory.plate.mount(plate=PLATE_TO_MOUNT)

# Wait for robot to start running the plate mount path
while robot.status.state.path != RobotPaths.PUT_PLATE:
    sleep(0.5)

assert robot.status.state.arm_plate == PLATE_TO_MOUNT

# Wait for robot to finish running the path
while robot.status.state.path != RobotPaths.UNDEFINED:
    sleep(0.5)

assert robot.status.state.goni_plate == PLATE_TO_MOUNT
