from enum import Enum
from typing import Annotated, Any, Dict
from typing_extensions import Literal

from pydantic import Field, conint, conlist, validator, field_validator

from mx_robot_library.config import get_settings

from .base import BaseCmdModel, CmdEnum, CmdField

config = get_settings()


class RobotMaintCmds(CmdEnum):
    """Robot Maintenance Commands"""

    CAM_TRACKING_ON = CmdField(
        title="Camera Tracking On",
        description="Enable camera tracking feature.",
        value="cameratrackingon",
    )
    CAM_TRACKING_OFF = CmdField(
        title="Camera Tracking Off",
        description="Disable camera tracking feature.",
        value="cameratrackingoff",
    )
    SAVE_VIDEO_CLIP = CmdField(
        title="Save Video Clip",
        description="""Save the last 120s of video stream from the dome camera
        to configured FTP server.""",
        value="savevideoclip",
    )
    CLEAR_ROBOT_MSG = CmdField(
        title="Clear Robot Message",
        description="Clear last information message from robot controller.",
        value="clearrobotmsg",
    )
    CLEAR_MEMORY = CmdField(
        title="Clear Robot Memory",
        description="""Assume there are no sample nor plate in the tool
        or on the diffractometer.""",
        value="clearmemory",
    )
    PLC_SOFT_RESET = CmdField(
        title="Soft Reset PLC",
        description="""Initiate a warm reboot of the PLC and restart
        application on robot.""",
        value="resetprogram",
    )


class RobotMaintCmd(BaseCmdModel):
    """Robot Maintenance Command Model"""

    cmd: RobotMaintCmds = Field(
        title="Command",
    )


class BaseRobotMaintSetSample(BaseCmdModel):
    """Abstract Robot Maintenance Set Sample"""

    args: list[int] = Field(
        title="Arguments",
        min_length=3,
        max_length=3,
    )

    @field_validator("args", mode="after")
    def validate_args(self, value: list[int]) -> list[int]:
        puck_num, sample_num, sample_type = value
        if not puck_num >= 1:
            raise ValueError("Ensure puck number is greater than or equal to 1.")
        if not puck_num <= config.ASC_NUM_PUCKS:
            raise ValueError(
                f"Ensure puck number is less than or equal to {config.ASC_NUM_PUCKS}."
            )
        if not sample_num >= 1:
            raise ValueError("Ensure sample number is greater than or equal to 1.")
        if not sample_num <= config.ASC_NUM_PINS:
            raise ValueError(
                f"Ensure sample number is less than or equal to {config.ASC_NUM_PINS}."  # noqa: E501
            )
        if sample_type not in (1, 0):
            raise ValueError(
                f'Sample type "{sample_type}" not supported, valid options are (1 → Hampton / 0 → Other).'  # noqa: E501,B950,B907
            )
        return value


class RobotMaintSetDiffSampleCmd(BaseRobotMaintSetSample):
    """Robot Maintenance Set Diffractometer Sample Command

    Force robot to assume that the specified sample is mounted on diffractometer.

    Parameters
    ----------
    args : list[int]
        List of three integer arguments to set puck, sample and sample type.

        0: Puck Number
        1: Sample Number
        2: Sample Type (1 → Hampton / 0 → Other)
    """

    cmd: Literal["setdiffr"] = Field(title="Command", default="setdiffr")


class RobotMaintSetToolSampleCmd(BaseRobotMaintSetSample):
    """Robot Maintenance Set Tool Sample Command

    Force robot to assume that the specified sample is currently in the gripper jaw.

    Parameters
    ----------
    args : list[int]
        List of four integer arguments to set puck, sample, sample type and the jaw.

        0: Puck Number
        1: Sample Number
        2: Sample Type (1 → Hampton / 0 → Other)
        3: Jaw Number (Double grippers only) (0 → jaw A / 1 → jaw B)
    """

    cmd: Literal["settool"] = Field(title="Command", default="settool")
    args: list[int] = Field(
        title="Arguments",
        min_length=4,
        max_length=4,
    )

    @field_validator("args", mode="after")
    def validate_args(self, value: list[int]) -> list[int]:
        puck_num, sample_num, sample_type, jaw_num = value
        super().validate_args(
            v=[puck_num, sample_num, sample_type],
            values=value,
        )
        if jaw_num not in (0, 1):
            raise ValueError(
                f'Jaw number "{jaw_num}" not supported, valid options are (0 → jaw A / 1 → jaw B).'  # noqa: E501,B950,B907
            )
        return value


class RobotMaintSetMaxSoakCmd(BaseCmdModel):
    """Robot Maintenance Set Max Soak Time Command

    Set the soaking timeout after which a gripper drying will be automatically
    scheduled (after next sample exchange).

    Value must be between 1-10800 seconds.

    args : list[int]
        List containing a single integer to set soaking timeout.
    """

    cmd: Literal["setmaxsoaktime"] = Field(title="Command", default="setmaxsoaktime")
    args: list[Annotated[int, Field(ge=1, le=10800)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotMaintSetMaxSoakNumCmd(BaseCmdModel):
    """Robot Maintenance Set Max Soak Number Command

    Set the soaking cycle number after which a gripper drying will be automatically
    scheduled (after next sample exchange).

    Value must be between 1-48 cycles.

    args : list[int]
        List containing a single integer to set soaking cycle number.
    """

    cmd: Literal["setmaxsoaknb"] = Field(title="Command", default="setmaxsoaknb")
    args: list[Annotated[int, Field(ge=1, le=48)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotMaintSetAutoCloseLidCmd(BaseCmdModel):
    """Robot Maintenance Set Auto Close Lid Timer Command

    Set the timeout after which the lid will be automatically closed
    (Robot will go out of soaking port first).

    Value must be between 1-34560 minutes.

    Set value to zero to disable the function.

    args : list[int]
        List containing a single integer to set auto close lid timer.
    """

    cmd: Literal["setautocloselidtimer"] = Field(title="Command", default="setautocloselidtimer")
    args: list[Annotated[int, Field(ge=1, le=34560)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotMaintSetAutoDryCmd(BaseCmdModel):
    """Robot Maintenance Set Auto Dry Timer Command

    Set the timeout after which the gripper will be automatically dryed and brought
    back to home position (Robot will go out of soaking port first).

    Value must be between 1-34560 minutes.

    Set value to zero to disable the function.

    args : list[int]
        List containing a single integer to set auto dry timeout.
    """

    cmd: Literal["setautodrytimer"] = Field(title="Command", default="setautodrytimer")
    args: list[Annotated[int, Field(ge=1, le=34560)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotMaintSetCoolTimeCmd(BaseCmdModel):
    """Robot Maintenance Set Gripper Cooling Time Command

    Set the time spent by the robot in the soaking port to cool down
    its gripper after a drying phase.

    Value must be between 0-60 seconds.

    args : list[int]
        List containing a single integer to set gripper cooling time.
    """

    cmd: Literal["setgrippercoolingtimer"] = Field(title="Command", default="setgrippercoolingtimer")
    args: list[Annotated[int, Field(ge=0, le=60)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotMaintSetHighLN2Cmd(BaseCmdModel):
    """Robot Maintenance Set High LN2 Threshold Command

    Set the high threshold for LN2 regulation.

    Value is expresed as a percentage and must be between 0-100.

    args : list[int]
        List containing a single integer to set high LN2 threshold.
    """

    cmd: Literal["sethighln2"] = Field(title="Command", default="sethighln2")
    args: list[Annotated[int, Field(ge=0, le=100)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class RobotMaintSetLowLN2Cmd(BaseCmdModel):
    """Robot Maintenance Set Low LN2 Threshold Command

    Set the low threshold for LN2 regulation.

    Value is expresed as a percentage and must be between 0-100.

    args : list[int]
        List containing a single integer to set low LN2 threshold.
    """

    cmd: Literal["setlowln2"] = Field(title="Command", default="setlowln2")
    args: list[Annotated[int, Field(ge=0, le=100)]] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )


class CameraPositions(str, Enum):
    """Named Robot Camera Positions"""

    GONIOMETER = "gonio"
    DEWAR = "dewar"
    DRY_HOME = "dryhome"

    def __str__(self) -> str:
        return self.value


class RobotMaintGotoCamPosCmd(BaseCmdModel):
    """Robot Maintenance Goto Camera Position Command

    Move the camera to the position given in argument.
    """

    cmd: Literal["gotocameraposition"] = Field(title="Command", default="gotocameraposition")
    args: list[CameraPositions] = Field(
        title="Arguments",
        min_length=1,
        max_length=1,
    )
