from pydantic import Field, conlist, validate_arguments, validator
from typing_extensions import Self

from ...config import get_settings
from ..commands.status import RobotStatusCmds
from .base import BaseStatusResponse, compute_error

config = get_settings()


class BasePLCResponse(BaseStatusResponse):
    """Abstract PLC Response"""

    raw_values: tuple[bool, ...] = Field(
        title="Raw Values",
        description="Raw values parsed from command output.",
    )


class PLCInputsResponse(BasePLCResponse):
    """PLC Inputs Response Model"""

    door_closed: bool = Field(title="Door Closed")

    _compute_error = validator(
        "error",
        pre=True,
        always=True,
        allow_reuse=True,
    )(compute_error)

    @classmethod
    @validate_arguments
    def _parse_raw_values(
        cls: type[Self],
        cmd: RobotStatusCmds,
        raw: str,
    ) -> dict[str, tuple[str, ...]]:
        res = super(PLCInputsResponse, cls)._parse_raw_values(cmd=cmd, raw=raw)
        _raw_values = res["raw_values"]

        # Set values for keys where value does not need pre-parsing
        res.update(
            {
                "door_closed": _raw_values[11],  # Could also be (4)?
            }
        )

        return res


class PLCOutputsResponse(BasePLCResponse):
    """PLC Outputs Response Model"""

    puck_presense: conlist(
        item_type=bool,
        min_items=config.ASC_NUM_PUCKS,
        max_items=config.ASC_NUM_PUCKS,
    ) = Field(
        title="Puck Presense",
        description="Puck presense mapping.",
    )

    _compute_error = validator(
        "error",
        pre=True,
        always=True,
        allow_reuse=True,
    )(compute_error)

    @classmethod
    @validate_arguments
    def _parse_raw_values(
        cls: type[Self],
        cmd: RobotStatusCmds,
        raw: str,
    ) -> dict[str, tuple[str, ...]]:
        res = super(PLCOutputsResponse, cls)._parse_raw_values(cmd=cmd, raw=raw)
        _raw_values = res["raw_values"]

        # Set values for keys where value does not need pre-parsing
        res.update(
            {
                "puck_presense": _raw_values[56:85],
            }
        )

        return res
