import re
from typing import Union
from typing_extensions import Self
from pydantic import BaseModel, Field, validate_arguments
from ..commands.status import RobotStatusCmds


class BaseStatusResponse(BaseModel):
    """Abstract Status Command Response"""

    raw_values: tuple[str, ...] = Field(
        title="Raw Values",
        description="Raw values parsed from command output.",
        exclude=True,
    )

    class Config:
        allow_mutation: bool = False
        anystr_strip_whitespace: bool = True

    @staticmethod
    @validate_arguments
    def is_valid_id(id: Union[int, str]) -> bool:
        """Simple method to check if an ID is valid.

        Parameters
        ----------
        id : Union[int, str]
            ID to validate.

        Returns
        -------
        bool
            True if valid, else False.
        """

        if isinstance(id, str):
            return False
        
        return id >= 1

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

        _raw_values: tuple[str, ...] = tuple()
        match_str = re.compile(f"(?<={cmd.value}\().*(?=\))", re.S)
        if re.search(match_str, raw):
            _raw_inner: str = re.findall(match_str, raw)[0]
            _raw_values = _raw_inner.split(sep=",")

        return {
            "raw_values": _raw_values,
        }

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
