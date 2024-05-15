from typing import Annotated, Optional, Union

from pydantic import Field, validate_call, field_validator
from typing_extensions import Self

from ...exceptions.base import UnknownPLCError
from ...exceptions.commands.common import common_errors
from ..commands.general import RobotGeneralCmds
from .base import BaseResponse, compute_error


class CommonResponse(BaseResponse):
    """Common Response Model"""

    error: Optional[Annotated[Union[common_errors, UnknownPLCError], Field(union_mode="left_to_right")]] = Field(
        title="Raised Exception",
        description="Error returned by the PLC if raised.",
        validate_default=True,
        default=None,
    )

    _compute_error = field_validator("error", mode="before")(compute_error)

    @classmethod
    @validate_call
    def parse_cmd_output(
        cls,
        cmd: RobotGeneralCmds,
        obj: Annotated[Union[str, bytes], Field(union_mode="left_to_right")],
    ) -> Self:
        """Parse output from returned command to create a new object instance.

        Parameters
        ----------
        cmd : RobotGeneralCmds
            Command response to parse.
        obj : Union[str, bytes]
            Raw response string to be parsed.

        Returns
        -------
        Self
            New model instance.
        """

        return cls.model_validate(cls._parse_raw_values(cmd=cmd, raw=obj))
