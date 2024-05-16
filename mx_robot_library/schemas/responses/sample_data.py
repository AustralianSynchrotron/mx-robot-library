from pydantic import Field, field_validator, validate_call

from ...config import get_settings
from ..commands.status import RobotStatusCmds
from .base import BaseStatusResponse, compute_error

config = get_settings()


class SampleDataResponse(BaseStatusResponse):
    """Sample Data Response"""

    puck_matrix: list[str] = Field(
        title="Puck Presense",
        description="Puck presense mapping.",
        min_length=config.ASC_NUM_PUCKS,
        max_length=config.ASC_NUM_PUCKS,
    )

    _compute_error = field_validator("error", mode="before")(compute_error)

    @classmethod
    @validate_call
    def _parse_raw_values(
        cls,
        cmd: RobotStatusCmds,
        raw: str,
    ) -> dict[str, tuple[str, ...]]:
        res = super(SampleDataResponse, cls)._parse_raw_values(cmd=cmd, raw=raw)
        _raw_values = res["raw_values"]

        # Set values for keys where value does not need pre-parsing
        res.update(
            {
                "puck_matrix": _raw_values[21:50],
            }
        )

        return res
