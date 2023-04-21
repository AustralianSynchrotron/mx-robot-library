from time import sleep

from mx_robot_library.client import Client
from mx_robot_library.schemas.common.path import RobotPaths

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Try to mount a pin after unmounting the current pin on the goni
pin = robot.utils.get_pin(id=5, puck=1)
msg = robot.trajectory.hot_puck.unmount_then_mount(pin=pin)

# Wait until operation starts
while robot.status.state.path != RobotPaths.HOTPUCK_GET_PUT:
    sleep(0.5)

# Wait until operation ends
while robot.status.state.path != RobotPaths.UNDEFINED:
    sleep(0.5)

# Check that the pin on the goni, matches expectations
assert robot.status.state.goni_pin == pin
