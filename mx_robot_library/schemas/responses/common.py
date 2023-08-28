from typing import Optional, Union

from pydantic import Field, validate_arguments, validator
from typing_extensions import Self

from ...exceptions.base import UnknownPLCError
from ...exceptions.commands.common import common_errors
from ..commands.general import RobotGeneralCmds
from .base import BaseResponse, compute_error


class CommonResponse(BaseResponse):
    """Common Response Model"""

    error: Optional[Union[common_errors, UnknownPLCError]] = Field(
        title="Raised Exception",
        description="Error returned by the PLC if raised.",
        default=None,
    )

    _compute_error = validator(
        "error",
        pre=True,
        always=True,
        allow_reuse=True,
    )(compute_error)

    @classmethod
    @validate_arguments
    def parse_cmd_output(
        cls: type[Self],
        cmd: RobotGeneralCmds,
        obj: Union[str, bytes],
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

        return cls.parse_obj(cls._parse_raw_values(cmd=cmd, raw=obj))
