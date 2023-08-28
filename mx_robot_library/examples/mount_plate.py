from mx_robot_library.client import Client
from mx_robot_library.schemas.common.sample import Plate

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

PLATE_TO_MOUNT = Plate(id=1)

# Mount plate from position "1", wait to complete
robot.trajectory.plate.mount(plate=PLATE_TO_MOUNT, wait=True)

assert robot.status.state.goni_plate == PLATE_TO_MOUNT
