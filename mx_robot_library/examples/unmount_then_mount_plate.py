from mx_robot_library.client import Client
from mx_robot_library.schemas.common.sample import Plate

# Create a new client instance
robot = Client(host="192.168.0.0", readonly=False)

PLATE_TO_MOUNT = Plate(id=2)

# Unmount plate from goni, then mount plate from position "2"
robot.trajectory.plate.unmount_then_mount(plate=PLATE_TO_MOUNT)

assert robot.status.state.goni_plate == PLATE_TO_MOUNT
