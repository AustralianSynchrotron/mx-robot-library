from mx_robot_library.client import Client

# Create a new client instance
robot = Client(
    host="192.168.0.0",  # Controller IP
    status_port=1000,  # Status query port [ENV: MX_ASC_STATUS_PORT"]
    cmd_port=10000,  # Trajectory command port [ENV: ASC_CMD_PORT"]
    readonly=False,  # Toggle to block trajectory calls (Local to client)
)

# Read robot state
state = robot.status.state

# Read PLC Inputs
plc_inputs = robot.status.plc_inputs

# Read PLC Outputs
plc_outputs = robot.status.plc_outputs

# Arm Power ON/OFF
robot.common.power = True
robot.common.power = False

# Reset Fault Alarm
robot.common.reset()

# Increase/Decrease Arm Speed
robot.common.speed_up()
robot.common.slow_down()
