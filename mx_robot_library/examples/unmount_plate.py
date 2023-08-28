from mx_robot_library.client import Client

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Unmount plate from goni, wait to complete
robot.trajectory.plate.unmount(wait=True)

assert robot.status.state.goni_plate is None
