from types import MappingProxyType
from typing import Any, Optional, Union

from pydantic import (
    Field,
    validate_call,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    field_validator,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    no_info_after_validator_function,
    plain_serializer_function_ser_schema,
)
from typing_extensions import Self

from ..commands.status import RobotStatusCmds
from ..common.path import Path, RobotPaths
from ..common.position import Position, RobotPositions
from ..common.sample import Pin, Plate
from ..common.tool import Tool
from .base import BaseStatusResponse, compute_error


class StateResponse(BaseStatusResponse):
    """State Response Model"""

    power: bool = Field(
        title="Power Status",
        description="Whether the PLC is currently sending power to the robot arm.",
    )
    remote_mode: bool = Field(
        title="Remote Mode",
        description="Whether the robot is currently in remote mode.",
    )
    fault_or_stopped: bool = Field(
        title="Fault or Stopped",
        description="Fault status or stop mode.",
    )
    tool: Optional[Tool] = Field(
        title="Tool",
        description="Current tool mounted.",
    )
    position: Position = Field(
        title="Position",
        description="Current position of the robot arm.",
        default=RobotPositions.UNDEFINED,
    )
    path: Path = Field(
        title="Command Path",
        description="The function the robot is currently running.",
        default=RobotPaths.UNDEFINED,
    )
    jaw_a_is_open: bool = Field(
        title="Jaw (A) Is Open",
        description="Jaw (A) is open.",
    )
    jaw_b_is_open: bool = Field(
        title="Jaw (B) Is Open",
        description="Jaw (B) is open.",
    )
    jaw_a_pin: Optional[Pin] = Field(
        title="Jaw (A) Pin",
        description="Pin mounted in Jaw (A).",
        default=None,
    )
    jaw_b_pin: Optional[Pin] = Field(
        title="Jaw (B) Pin",
        description="Pin mounted in Jaw (B).",
        default=None,
    )
    goni_pin: Optional[Pin] = Field(
        title="Goni Pin",
        description="Pin mounted on the goniometer.",
        default=None,
    )
    arm_plate: Optional[Plate] = Field(
        title="Arm Plate",
        description="Plate mounted on the arm.",
        default=None,
    )
    goni_plate: Optional[Plate] = Field(
        title="Goni Plate",
        description="Plate mounted on the goniometer.",
        default=None,
    )
    seq_running: bool = Field(
        title="Sequence Running",
        description="Sequence is running.",
    )
    seq_paused: bool = Field(
        title="Sequence Paused",
        description="Sequence is paused.",
    )
    speed_ratio: float = Field(
        title="Speed Ratio",
        description="Robot speed ratio (%).",
        le=100.0,
        ge=0.0,
    )
    plc_last_msg: str = Field(
        title="PLC Last Message",
        description="Last information message from PLC.",
    )

    _compute_error = field_validator("error", mode="before")(compute_error)

    @classmethod
    def _get_position_map(
        cls: type[Self],
    ) -> MappingProxyType[str, Union[int, tuple[int, ...]]]:
        """Get position mapping proxy from field definitions.

        Returns
        -------
        MappingProxyType[str, Union[int, tuple[int, ...]]]
            Field to position mapping.
        """
        _position_map: dict[str, Union[int, tuple[int, ...]]] = {
            "power": 0,
            "remote_mode": 1,
            "fault_or_stopped": 2,
            "tool": 3,
            "position": 4,
            "path": 5,
            "jaw_a_is_open": 6,
            "jaw_b_is_open": 7,
            "jaw_a_pin": (8, 9),
            "jaw_b_pin": (10, 11),
            "goni_pin": (12, 13),
            "arm_plate": 14,
            "goni_plate": 15,
            "seq_running": 17,
            "seq_paused": 18,
            "speed_ratio": 19,
            "plc_last_msg": 28,
        }
        return MappingProxyType(_position_map)

    @classmethod
    @validate_call
    def _parse_raw_values(
        cls,
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
        res = super(StateResponse, cls)._parse_raw_values(cmd=cmd, raw=raw)
        _raw_values = res["raw_values"]

        # Use position map to map raw values to model
        _position_map = cls._get_position_map()
        for _key, _position in _position_map.items():
            if isinstance(_position, list) or isinstance(_position, tuple):
                res[_key] = [_raw_values[pos] for pos in _position]
            elif isinstance(_position, int):
                res[_key] = _raw_values[_position]

        for _key in ("jaw_a_pin", "jaw_b_pin", "goni_pin"):
            if _key in res:
                res[_key] = Pin._validate(res[_key])

        for _key in ("arm_plate", "goni_plate"):
            if _key in res:
                res[_key] = Plate._validate(res[_key])
                if res[_key] == "-1":
                    res[_key] = None

        return res
