from mx_robot_library.client import Client

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Try to pre-pick a pin, loading it into the gripper
pin = robot.utils.get_pin(id=5, puck=1)
msg = robot.trajectory.prepick(pin=pin)

# # Wait until operation is complete
# while robot.status.state.path != RobotPaths.UNDEFINED:
#     sleep(0.5)

# # Check that the pin on the goni, matches expectations
# assert robot.status.state.goni_pin == pin
