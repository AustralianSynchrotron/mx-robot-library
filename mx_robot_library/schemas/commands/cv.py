from pydantic import Field, conint, conlist

from .base import BaseCmdModel, CmdEnum, CmdField


class RobotCVCmds(CmdEnum):
    """Robot CV Commands

    Cryo-vision package (CV).
    """

    REFRESH = CmdField(
        title="Refresh Camera",
        desciption="""Force refresh the cryo-vision module results (automatically bring
        back the dome camera to the Dewar filming position and turn on the ring light).
        Computations can take a few seconds; results are available within the 'state'
        request answer.""",
        value="cv_refresh",
    )
    AUTO_REFRESH_ON = CmdField(
        title="Turn On Automatic Camera Refresh",
        desciption="""Turns on the automatic refresh of cryo-vision module results.
        When this option is used, the cryo-vision controller will try to refresh
        the pucks & samples detection results each time the robot is at SOAK position,
        with the dome camera filming the Dewar, with its lid open.""",
        value="cv_autorefreshon",
    )
    AUTO_REFRESH_OFF = CmdField(
        title="Turn Off Automatic Camera Refresh",
        desciption="Stops the automatic refresh of cryo-vision based results.",
        value="cv_autorefreshoff",
    )
    REBOOT = CmdField(
        title="Reboot CV Controller",
        desciption="""Reboot the cryo-vision controller.
        Same effect as pla_reboot command.""",
        value="cv_reboot",
    )
    SHUTDOWN = CmdField(
        title="Shutdown CV Controller",
        desciption="""Cleanly turns off the cry-vision controller
        (recommended before any power cycle of the electronics).
        The controller will boot up again after a power cycle of the electronics.
        Same effect as pla_shutdown command (same controller for Puck Loading Assistant
        and Cryo-Vision options).""",
        value="cv_shutdown",
    )


class RobotCVCmd(BaseCmdModel):
    """Robot CV Command Model"""

    cmd: RobotCVCmds = Field(
        title="Command",
    )


class RobotCVLightModeCmd(BaseCmdModel):
    """Robot CV Light Mode Command

    Depending on the input value of 'cmd', the external light used by the cryo-vision
    algorithm can be forced OFF for light-sensitive experiments.

    Parameters
    ----------
    args : list[int]
        List containing a single integer to set automatic or manual off modes.
        (0 = External lighting is managed by the PLC,
        1 = External lighting is forced to OFF by the user)
    """

    cmd: str = Field(title="Command", default="cv_forcelightoff", const=True)
    args: conlist(item_type=conint(ge=0, le=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )
