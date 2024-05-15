from typing import Optional, Type

from pydantic import Field
from pydantic.dataclasses import dataclass
from typing_extensions import TypeAlias

from ..base import PLCError


@dataclass(frozen=True)
class NotPointingError(PLCError):
    """Not Pointing Error"""

    # Point a puck first

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        pattern=r"(?i).*\bpoint\b.*\bpuck\b.*\bfirst\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Point a puck first.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="A call needs to be made to point the laser at a puck first.",
    )


pla_errors: TypeAlias = Type[NotPointingError]
