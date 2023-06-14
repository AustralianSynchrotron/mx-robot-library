from typing import Optional, Union
from typing_extensions import TypeAlias
from pydantic import Field
from pydantic.dataclasses import dataclass
from ..base import PLCError


@dataclass(frozen=True)
class DewarClosedError(PLCError):
    """Dewar Closed Error"""
    # Open dewar first

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bopen\b.*\bdewar\b.*\bfirst\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="The dewar is closed.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The dewar needs to be open before calling this command.",
    )


@dataclass(frozen=True)
class CVPositionError(PLCError):
    """Cryo-Vision Position Error"""
    # Robot must be at SOAK or HOME

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bmust\b.*\bat\b.*\bsoak\b.*\bhome\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Robot must be at SOAK or HOME.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The robot arm is in an invalid position to execute this command.",
    )


@dataclass(frozen=True)
class ExternalLightingDisabled(PLCError):
    """External Lighting Disabled"""
    # Enable external lighting first

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\benable\b.*\bexternal\b.*\blighting\b.*\bfirst\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="External lighting must be enabled.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="External lighting is currently disabled.",
    )


cv_errors: TypeAlias = Union[DewarClosedError, CVPositionError, ExternalLightingDisabled]