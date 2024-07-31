from mx_robot_library.client import Client

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

# Read sample dewar level
robot.status.state.sample_dewar_level  # noqa: B018

# Read cryojet dewar level
robot.status.state.cryojet_dewar_level  # noqa: B018
