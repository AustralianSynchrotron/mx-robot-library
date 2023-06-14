from mx_robot_library.client import Client

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Try to unmount a pin, wait to complete
msg = robot.trajectory.hot_puck.unmount(wait=True)

# Check there is no pin on the goniometer
assert robot.status.state.goni_pin is None
