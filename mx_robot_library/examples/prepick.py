from mx_robot_library.client import Client
from mx_robot_library.schemas.common.sample import Pin

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

PREPICK_PIN = Pin(id=5, puck=1)

# Try to pre-pick a pin, loading it into the gripper, wait to complete
msg = robot.trajectory.puck.prepick(pin=PREPICK_PIN, wait=True)

# Check that the pre-picked pin, matches expectations
assert robot.status.state.jaw_b_pin == PREPICK_PIN
