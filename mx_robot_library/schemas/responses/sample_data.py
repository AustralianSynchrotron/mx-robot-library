from pydantic import Field, conlist, validate_arguments
from typing_extensions import Self

from mx_robot_library.config import get_settings

from ..commands.status import RobotStatusCmds
from .base import BaseStatusResponse

config = get_settings()


class SampleDataResponse(BaseStatusResponse):
    """Sample Data Response"""

    puck_matrix: conlist(
        item_type=str,
        min_items=config.ASC_NUM_PUCKS,
        max_items=config.ASC_NUM_PUCKS,
    ) = Field(
        title="Puck Presense",
        description="Puck presense mapping.",
    )

    @classmethod
    @validate_arguments
    def _parse_raw_values(
        cls: type[Self],
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
