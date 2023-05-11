from types import MappingProxyType
from typing import Optional, Union

from pydantic import Field, validate_arguments
from typing_extensions import Self

from ..commands.status import RobotStatusCmds
from ..common.path import Path, RobotPaths
from ..common.position import Position, RobotPositions
from ..common.sample import Pin, Plate
from ..common.tool import Tool
from .base import BaseStatusResponse


class StateResponse(BaseStatusResponse):
    """State Response Model"""

    power: bool = Field(
        title="Power Status",
        description="Whether the PLC is currently sending power to the robot arm.",
        position=0,
    )
    remote_mode: bool = Field(
        title="Remote Mode",
        description="Whether the robot is currently in remote mode.",
        position=1,
    )
    fault_or_stopped: bool = Field(
        title="Fault or Stopped",
        description="Fault status or stop mode.",
        position=2,
    )
    tool: Optional[Tool] = Field(
        title="Tool",
        description="Current tool mounted.",
        position=3,
    )
    position: Position = Field(
        title="Position",
        description="Current position of the robot arm.",
        default=RobotPositions.UNDEFINED,
        position=4,
    )
    path: Path = Field(
        title="Command Path",
        description="The function the robot is currently running.",
        default=RobotPaths.UNDEFINED,
        position=5,
    )
    jaw_a_is_open: bool = Field(
        title="Jaw (A) Is Open",
        description="Jaw (A) is open.",
        position=6,
    )
    jaw_b_is_open: bool = Field(
        title="Jaw (B) Is Open",
        description="Jaw (B) is open.",
        position=7,
    )
    jaw_a_pin: Optional[Pin] = Field(
        title="Jaw (A) Pin",
        description="Pin mounted in Jaw (A).",
        default=None,
        position=(8, 9),
    )
    jaw_b_pin: Optional[Pin] = Field(
        title="Jaw (B) Pin",
        description="Pin mounted in Jaw (B).",
        default=None,
        position=(10, 11),
    )
    goni_pin: Optional[Pin] = Field(
        title="Goni Pin",
        description="Pin mounted on the goniometer.",
        default=None,
        position=(12, 13),
    )
    arm_plate: Optional[Plate] = Field(
        title="Arm Plate",
        description="Plate mounted on the arm.",
        default=None,
        position=14,
    )
    goni_plate: Optional[Plate] = Field(
        title="Goni Plate",
        description="Plate mounted on the goniometer.",
        default=None,
        position=15,
    )
    seq_running: bool = Field(
        title="Sequence Running",
        description="Sequence is running.",
        position=17,
    )
    seq_paused: bool = Field(
        title="Sequence Paused",
        description="Sequence is paused.",
        position=18,
    )
    speed_ratio: float = Field(
        title="Speed Ratio",
        description="Robot speed ratio (%).",
        le=100.0,
        ge=0.0,
        position=19,
    )
    plc_last_msg: str = Field(
        title="PLC Last Message",
        description="Last information message from PLC.",
        position=28,
    )

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
        _position_map: dict[str, Union[int, tuple[int, ...]]] = {}
        for _name, _model in cls.__fields__.items():
            _field_info = _model.field_info
            if _field_info.extra.get("position") is not None:
                _position_map[_name] = _field_info.extra["position"]
        return MappingProxyType(_position_map)

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
        res = super(StateResponse, cls)._parse_raw_values(cmd=cmd, raw=raw)
        _raw_values = res["raw_values"]

        # Use position map to map raw values to model
        _position_map = cls._get_position_map()
        for _key, _position in _position_map.items():
            if isinstance(_position, list) or isinstance(_position, tuple):
                res[_key] = [_raw_values[pos] for pos in _position]
            elif isinstance(_position, int):
                res[_key] = _raw_values[_position]
        return res
