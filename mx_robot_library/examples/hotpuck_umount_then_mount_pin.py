from mx_robot_library.client import Client
from mx_robot_library.schemas.common.sample import Pin

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

PIN_TO_MOUNT = Pin(id=5, puck=101)

# Try to mount a pin after unmounting the current pin on the goni, wait to complete
msg = robot.trajectory.hot_puck.unmount_then_mount(pin=PIN_TO_MOUNT, wait=True)

# Check that the pin on the goni, matches expectations
assert robot.status.state.goni_pin == PIN_TO_MOUNT
