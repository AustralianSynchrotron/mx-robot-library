from typing import Optional, Union

from pydantic import Field
from pydantic.dataclasses import dataclass
from typing_extensions import TypeAlias

from ..base import PLCError


@dataclass(frozen=True)
class LidMovingError(PLCError):
    """Lid Moving Error"""

    # Disabled when lid is moving

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bdisabled\b.*\blid\b.*\bmoving\b.*",
        default=None,
    )
    msg: str = Field(
        title="Message",
        description="Short error message.",
        default="The dewar lid is moving.",
    )
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="Command disabled when the dewar lid is moving.",
    )


@dataclass(frozen=True)
class PowerDisabled(PLCError):
    """Power Disabled"""

    # Robot power disabled

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bpower\b.*\bdisabled\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Robot power disabled.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The robot arm needs to be energised first.",
    )


@dataclass(frozen=True)
class NotReadyError(PLCError):
    """Not Ready Error"""

    # Robot not ready

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bnot\b.*\bready\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Robot not ready.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The robot is not ready to perform the operation requested.",
    )


@dataclass(frozen=True)
class ChangeToolError(PLCError):
    """Change Tool Error"""

    # Change tool first

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bchange\b.*\btool\b.*\bfirst\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Change tool first.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The required tool is not currently mounted on the arm.",
    )


@dataclass(frozen=True)
class PositionRejected(PLCError):
    """Position Rejected"""

    # Rejected - Trajectory must start at position: HOME
    # Rejected - Trajectory must start at position: SOAK

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\btrajectory\b.*\bmust\b.*\bstart\b.*\bposition\b:.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Robot at wrong start position.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The arm is in the wrong position to start the requested operation.",
    )


@dataclass(frozen=True)
class ToolAlreadyEquiped(PLCError):
    """Tool Already Equiped"""

    # Tool already equipped

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\btool\b.*\balready\b.*\bequipped\b:.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Tool already equipped.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The tool you requested the robot mount is already mounted.",
    )


trajectory_errors: TypeAlias = Union[
    LidMovingError,
    PowerDisabled,
    NotReadyError,
    ChangeToolError,
    PositionRejected,
    ToolAlreadyEquiped,
]
