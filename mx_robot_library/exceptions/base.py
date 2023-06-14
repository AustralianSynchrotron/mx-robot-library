from typing import Any, Optional
from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class RobotException(Exception):
    """General Robot Exception"""

    msg: str = Field(title="Message")

    def __str__(self) -> str:
        return self.msg

    @property
    def args(self) -> tuple[Any, ...]:
        """ """
        return (self.msg,)


@dataclass(frozen=True)
class PLCError(RobotException):
    """Robot PLC Error"""

    cmd: Optional[str] = Field(
        title="Command",
        description="Command call sent to the PLC.",
        default=None,
    )
    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        default=None,
    )
    msg: str = Field(
        title="Message",
        description="Shortend error message.",
        default="PLC error occured.",
    )
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default=None,
    )


@dataclass(frozen=True)
class UnknownPLCError(PLCError):
    """Unknown PLC Error"""

    response: str = Field(
        title="Response",
        description="Response received from the command call.",
    )
    msg: str = Field(
        title="Message",
        description="Short error message.",
        default="An unknown PLC error was received.",
    )
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="Command call resulted in the PLC returning an unknown error.",
    )
