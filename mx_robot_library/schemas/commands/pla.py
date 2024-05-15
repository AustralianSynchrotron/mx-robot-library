from typing import Annotated
from typing_extensions import Literal
from pydantic import Field, confloat, conint, conlist

from mx_robot_library.config import get_settings

from .base import BaseCmdModel, CmdEnum, CmdField

config = get_settings()


class RobotPLACmds(CmdEnum):
    """Robot PLA Commands

    Puck loading assistant (PLA), pan-tilt laser device.
    """

    RETURN_NEUTRAL = CmdField(
        title="Return to Neutral",
        description="""Bring back the pan-tilt laser device at its neutral position
        and switch off the laser power.""",
        value="pla_chill",
    )
    INCREASE_PAN = CmdField(
        title="Increase Panoramic Axis Angular Position",
        description="""Increase the angular position on the panoramic axis and
        automatically save it as the new position for the puck currently pointed.
        The angular step used is the one set by pla_setstep.""",
        value="pla_incpan",
    )
    DECREASE_PAN = CmdField(
        title="Decrease Panoramic Axis Angular Position",
        description="""Decrease the angular position on the panoramic axis and
        automatically save it as the new position for the puck currently pointed.
        The angular step used is the one set by pla_setstep.""",
        value="pla_decpan",
    )
    INCREASE_TILT = CmdField(
        title="Increase Tilt Axis Angular Position",
        description="""Increase the angular position on the tilt axis and automatically
        save it as the new position for the puck currently pointed.
        The angular step used is the one set by pla_setstep.""",
        value="pla_inctilt",
    )
    DECREASE_TILT = CmdField(
        title="Decrease Tilt Axis Angular Position",
        description="""Decrease the angular position on the tilt axis and automatically
        save it as the new position for the puck currently pointed.
        The angular step used is the one set by pla_setstep.""",
        value="pla_dectilt",
    )
    FACTORY_RESET = CmdField(
        title="Factory Reset",
        description="""Reset all puck positions for the pan-tilt laser device to
        factory set positions.""",
        value="pla_factoryreset",
    )
    REBOOT = CmdField(
        title="Factory Reset",
        description="Reboot the pan-tilt laser device controller.",
        value="pla_reboot",
    )
    SHUTDOWN = CmdField(
        title="Shutdown",
        description="""Cleanly turns off the pan-tilt laser controller
        (recommended before any power cycle of the electronics).
        The controller will boot up again after a power cycle of the electronics.""",
        value="pla_reboot",
    )
    STOP_SCANNING = CmdField(
        title="Stop Puck Scanning Sequence",
        description="""Stop the assisted puck scanning sequence.
        Pucks position-barcode mapping table is retained until next call of
        pla_cleanpuckmap or if values are overwritten by next call of
        pla_startscanning.""",
        value="pla_stopscanning",
    )


class RobotPLACmd(BaseCmdModel):
    """Robot PLA Command Model"""

    cmd: RobotPLACmds = Field(
        title="Command",
    )


class RobotPLAGotoPuckCmd(BaseCmdModel):
    """Robot PLA GotoPuck Command

    Point out the puck position given in argument in the Dewar with the laser device.

    Parameters
    ----------
    args : list[int]
        List containing a single integer to specify the desired puck position.
    """

    cmd: Literal["pla_gotopuck"] = Field(title="Command", default="pla_gotopuck")
    args: list[Annotated[int, Field(le=config.ASC_NUM_PUCKS, ge=1)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotPLASetStepCmd(BaseCmdModel):
    """Robot PLA SetStep Command

    Set the angular step used to adjust puck positions with pla_inc/decpan and
    pla_inc/dectilt functions.

    Parameters
    ----------
    args : list[float]
        List containing a single float to specify the desired angular step.
    """

    cmd: Literal["pla_setstep"] = Field(title="Command", default="pla_setstep")
    args: list[Annotated[float, Field(le=10, ge=0)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotPLAStartScanningCmd(BaseCmdModel):
    """Robot PLA Start Scanning Command

    Launch the assisted puck scanning sequence.

    Parameters
    ----------
    args : list[int]
        List containing two integers to specify the start and stop pucks.
    """

    cmd: Literal["pla_startscanning"] = Field(title="Command", default="pla_startscanning")
    args: list[Annotated[int, Field(le=config.ASC_NUM_PUCKS, ge=1)]] = Field(
        title="Arguments",
        min_length=2,
        max_length=2,
    )


class RobotPLACleanPuckMapCmd(BaseCmdModel):
    """Robot PLA Clean Puck Map Command

    Clean the pucks position-barcode mapping table from the memory between starting
    and last puck position number.

    Parameters
    ----------
    args : list[int]
        List containing two integers to specify the start and stop pucks.
    """

    cmd: Literal["pla_cleanpuckmap"] = Field(title="Command", default="pla_cleanpuckmap")
    args: list[Annotated[int, Field(le=config.ASC_NUM_PUCKS, ge=1)]] = Field(
        title="Arguments",
        min_length=2,
        max_length=2,
    )
