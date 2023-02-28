from typing_extensions import Self
from enum import Enum
from pydantic import BaseModel, Field
from mx_robot_library.config import get_settings

config = get_settings()


class PinType(int, Enum):
    """Pin Type"""

    CRYSTAL_CAP = 1
    OTHER = 0


class BaseSample(BaseModel):
    """Abstract Sample Model"""

    id: int = Field(title="ID", ge=1)

    def __int__(self: Self) -> int:
        return self.id


class Puck(BaseSample):
    """Puck Model"""

    id: int = Field(
        title="ID",
        le=config.ASC_NUM_PUCKS,
        ge=1,
    )
    # datamatrix: ? TBD


class Pin(BaseSample):
    """Pin Model"""

    id: int = Field(
        title="ID",
        le=config.ASC_NUM_PINS,
        ge=1,
    )
    puck: Puck = Field(
        title="Puck",
        description="",
    )
    type: PinType = Field(
        title="Type",
        description="",
        default=PinType.OTHER,
    )
    # datamatrix: ? TBD


class Plate(BaseSample):
    """Plate Model"""

    id: int = Field(
        title="ID",
        # le=config.ASC_NUM_PLATES,
        ge=1,
    )
    # datamatrix: ? TBD
