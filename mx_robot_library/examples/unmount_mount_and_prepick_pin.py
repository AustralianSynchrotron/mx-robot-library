from time import sleep

from mx_robot_library.client import Client
from mx_robot_library.schemas.common.path import RobotPaths

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Try to mount a pin after unmounting the current pin, then pre-pick the next pin
pin = robot.utils.get_pin(id=5, puck=1)
prepick_pin = robot.utils.get_pin(id=5, puck=2)
msg = robot.trajectory.unmount_then_mount(pin=pin, prepick_pin=prepick_pin)

# Wait until operation is complete
while robot.status.state.path != RobotPaths.UNDEFINED:
    sleep(0.5)

# Check that the pin on the goni, matches expectations
assert robot.status.state.goni_pin == pin