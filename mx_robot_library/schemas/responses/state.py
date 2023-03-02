from typing import Optional

from pydantic import Field, validate_arguments
from typing_extensions import Self

from ..commands.status import RobotStatusCmds
from ..common.path import Path, RobotPaths
from ..common.position import Position, RobotPositions
from ..common.sample import Pin
from ..common.tool import Tool
from .base import BaseStatusResponse


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

    @classmethod
    @validate_arguments
    def _parse_raw_values(
        cls: type[Self],
        cmd: RobotStatusCmds,
        raw: str,
    ) -> dict[str, tuple[str, ...]]:
        res = super(StateResponse, cls)._parse_raw_values(cmd=cmd, raw=raw)
        _raw_values = res["raw_values"]

        # Set values for keys where value does not need pre-parsing
        res.update(
            {
                "power": _raw_values[0],
                "remote_mode": _raw_values[1],
                "fault_or_stopped": _raw_values[2],
                "tool": _raw_values[3],
                "position": _raw_values[4],
                "path": _raw_values[5],
                "jaw_a_is_open": _raw_values[6],
                "jaw_b_is_open": _raw_values[7],
                "seq_running": _raw_values[17],
                "seq_paused": _raw_values[18],
                "speed_ratio": _raw_values[19],
                "plc_last_msg": _raw_values[28],
            },
        )

        # Process pin status for jaws ("A"/"B") and goni
        _pin_keys = iter(["jaw_a_pin", "jaw_b_pin", "goni_pin"])
        _pin_values = iter(_raw_values[8:14])
        for puck_id in _pin_values:
            pin_id = next(_pin_values)
            key = next(_pin_keys)
            if cls.is_valid_id(puck_id) and cls.is_valid_id(pin_id):
                res[key] = Pin.parse_obj(
                    obj={
                        "id": pin_id,
                        "puck": {"id": puck_id},
                    }
                )
        return res
