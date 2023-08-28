import re
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field, validate_arguments
from typing_extensions import Self

from ...exceptions.base import PLCError
from ..commands.status import RobotStatusCmds

ROBOT_STATUS_CMD_STRS: tuple[str, ...] = tuple([str(_val) for _val in RobotStatusCmds])


def compute_error(v: Any, values: Dict[str, Any]) -> Union[Dict[str, Any], Any, None]:
    """Compute error from parsed "cmd" and "msg".

    Parameters
    ----------
    v : Any
        Current value.
    values : Dict[str, Any]
        Model values.

    Returns
    -------
    Union[Dict[str, Any], Any, None]
        Computed value or default.
    """

    if v is None:
        _cmd: Any = values.get("cmd")
        _resp: Any = values.get("msg")

        if _cmd in ROBOT_STATUS_CMD_STRS and isinstance(_resp, str):
            # Response is for a status command
            _cmd: str
            match_str = re.compile(f"(?<={_cmd}\().*(?=\))", re.S)  # noqa: W605
            _matches: list[str] = re.findall(match_str, _resp)
            if len(_matches) != 1:
                # Response doesn't match expected format
                return {"cmd": _cmd, "response": _resp}
            try:
                # If we can split on "," without hitting an exception, no error exists
                _matches[0].split(sep=",")
                return None
            except Exception:
                return {"cmd": _cmd, "response": _resp}
        elif isinstance(_resp, str) and _resp == _cmd:
            # Response echos command, so no error
            return None
        elif isinstance(_cmd, str) and isinstance(_resp, str):
            # Error exists, let Pydantic try to match an exception by response
            return {"cmd": _cmd, "response": _resp}
    return v


class BaseResponse(BaseModel):
    """Abstract Command Response"""

    cmd: str = Field(
        title="Command",
        description="Command that triggered this response.",
        exclude=True,
    )
    msg: str = Field(
        title="Message",
        description="Message returned from command call.",
        exclude=True,
    )
    error: Optional[PLCError] = Field(
        title="Raised Exception",
        description="Error returned by the PLC if raised.",
        default=None,
    )

    class Config:
        allow_mutation: bool = False
        anystr_strip_whitespace: bool = True

    @classmethod
    @validate_arguments
    def _parse_raw_values(
        cls: type[Self],
        cmd: Union[str, Any],
        raw: str,
    ) -> dict[str, Any]:
        """Parse raw command output from the robot.

        Parameters
        ----------
        cmd : Union[str, Any]
            Command response to parse.
        raw : str
            Raw response string to be parsed.

        Returns
        -------
        dict[str, Any]
            Dictionary containing parsed values.
        """

        return {"cmd": str(cmd), "msg": raw}

    @classmethod
    @validate_arguments
    def parse_cmd_output(
        cls: type[Self],
        cmd: Union[str, Any],
        obj: Union[str, bytes],
    ) -> Self:
        """Parse output from returned command to create a new object instance.

        Parameters
        ----------
        cmd : Union[str, Any]
            Command response to parse.
        obj : Union[str, bytes]
            Raw response string to be parsed.

        Returns
        -------
        Self
            New model instance.
        """

        return cls.parse_obj(cls._parse_raw_values(cmd=cmd, raw=obj))


class BaseStatusResponse(BaseResponse):
    """Abstract Status Command Response"""

    raw_values: tuple[str, ...] = Field(
        title="Raw Values",
        description="Raw values parsed from command output.",
        exclude=True,
    )

    @classmethod
    @validate_arguments
    def _parse_raw_values(
        cls: type[Self],
        cmd: RobotStatusCmds,
        raw: str,
    ) -> dict[str, tuple[str, ...]]:
        """Parse raw command output from the robot.

        Parameters
        ----------
        cmd : RobotStatusCmds
            Command response to parse.
        raw : str
            Raw response string to be parsed.

        Returns
        -------
        dict[str, tuple[str, ...]]
            Dictionary containing parsed values.
        """

        res = super(BaseStatusResponse, cls)._parse_raw_values(cmd=cmd, raw=raw)

        _raw_values: tuple[str, ...] = tuple()
        match_str = re.compile(f"(?<={cmd.value}\().*(?=\))", re.S)  # noqa: W605
        if re.search(match_str, raw):
            _raw_inner: str = re.findall(match_str, raw)[0]
            _raw_values = _raw_inner.split(sep=",")

        res.update(
            {
                "raw_values": _raw_values,
            }
        )

        return res

    @classmethod
    @validate_arguments
    def parse_cmd_output(
        cls: type[Self],
        cmd: RobotStatusCmds,
        obj: Union[str, bytes],
    ) -> Self:
        """Parse output from returned command to create a new object instance.

        Parameters
        ----------
        cmd : RobotStatusCmds
            Command response to parse.
        obj : Union[str, bytes]
            Raw response string to be parsed.

        Returns
        -------
        Self
            New model instance.
        """

        return cls.parse_obj(cls._parse_raw_values(cmd=cmd, raw=obj))
