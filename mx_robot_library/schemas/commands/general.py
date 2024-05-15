from typing import Optional

from pydantic import Field

from .base import BaseCmdModel, CmdEnum, CmdField


class RobotGeneralCmds(CmdEnum):
    """Robot General Commands"""

    # Power Commands
    ON = CmdField(
        title="Power On",
        description="Switch the robot power on.",
        value="on",
    )
    OFF = CmdField(
        title="Power Off",
        description="Switch the robot power off.",
        value="off",
    )
    PANIC = CmdField(
        title="Emergency Stop",
        description="""Stop the robot immediately,
        abort the trajectory and shut arm power off.""",
        value="panic",
    )
    RESET = CmdField(
        title="Fault Reset",
        description="Acknowledge security fault and allow user to bring power back.",
        value="reset",
    )

    # Open/Close Tool Commands
    OPEN_TOOL_A = CmdField(
        title="Open Tool (A)",
        description="Open the current gripper (jaw A in case of double gripper).",
        value="opentool",
    )
    CLOSE_TOOL_A = CmdField(
        title="Close Tool (A)",
        description="Close the current gripper (jaw A in case of double gripper).",
        value="closetool",
    )
    OPEN_TOOL_B = CmdField(
        title="Open Tool (B)",
        description="Open the current gripper (jaw B in case of double gripper).",
        value="opentoolb",
    )
    CLOSE_TOOL_B = CmdField(
        title="Close Tool (B)",
        description="Close the current gripper (jaw B in case of double gripper).",
        value="closetoolb",
    )

    # Speed Commands
    # Notes:
    #     The documentation states that the speed can range from 0.01% to 100%,
    #     but the two commands that control this value don't allow arguments.

    #     There must be more to this, as I don't think we'd be expected to call
    #     the command nine thousand, nine hundred and ninety nine times, just to
    #     get from 0.01% to 100%.
    SPEED_UP = CmdField(
        title="Increase Speed",
        description="Increase robot speed (range from 0.01% to 100%).",
        value="speedup",
    )
    SLOW_DOWN = CmdField(
        title="Decrease Speed",
        description="Decrease robot speed (range from 0.01% to 100%).",
        value="speeddown",
    )

    # Trajectory Commands
    ABORT = CmdField(
        title="Abort Trajectory",
        description="Abort running trajectory.",
        value="abort",
    )
    PAUSE = CmdField(
        title="Pause Trajectory",
        description="Pause running trajectory, stopping the robot in position.",
        value="pause",
    )
    RESTART = CmdField(
        title="Restart Trajectory",
        description="Resume the trajectory after pause or default.",
        value="restart",
    )

    # Dewar Commands
    OPEN_LID = CmdField(
        title="Open Lid",
        description="Open Dewar Lid.",
        value="openlid",
    )
    CLOSE_LID = CmdField(
        title="Close Lid",
        description="Close Dewar Lid.",
        value="closelid",
    )

    # Goniometer Commands
    MAGNET_ON = CmdField(
        title="Magnet On",
        description="Switch on the magnetization of the goniometer electro-magnet.",
        value="magneton",
    )
    MAGNET_OFF = CmdField(
        title="Magnet Off",
        description="Switch off the magnetization of the goniometer electro-magnet.",
        value="magnetoff",
    )

    # Miscellaneous Commands
    CLEAR_BCRD = CmdField(
        title="Clear Barcode",
        description="Clear the barcode/datamatrix return message.",
        value="clearbcrd",
    )
    HEATER_ON = CmdField(
        # I think this heater is to prevent condensation accumulating on the robot?
        title="Heater On",
        description="Switch on the heater.",
        value="heateron",
    )
    HEATER_OFF = CmdField(
        title="Heater Off",
        description="Switch off the heater.",
        value="heateroff",
    )


class RobotGeneralCmd(BaseCmdModel):
    """Robot General Command Model"""

    cmd: RobotGeneralCmds = Field(
        title="Command",
    )
    args: Optional[list] = Field(
        title="Arguments",
        default=None,
    )
