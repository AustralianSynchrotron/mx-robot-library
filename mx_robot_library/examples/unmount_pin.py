from time import sleep

from mx_robot_library.client import Client
from mx_robot_library.schemas.common.path import RobotPaths

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Try to unmount a pin
msg = robot.trajectory.unmount()

# Wait until operation is complete
while robot.status.state.path != RobotPaths.UNDEFINED:
    sleep(0.5)

# Check there is no pin on the goniometer
assert robot.status.state.goni_pin is None
