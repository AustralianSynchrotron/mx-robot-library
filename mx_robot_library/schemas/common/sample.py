from enum import Enum
from typing import Any, Type, Union, Optional

from pydantic import BaseModel, Field, validate_arguments
from typing_extensions import Self

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
    def validate(cls: Type[Self], value: Any) -> Self:
        if value == "-1":
            return None
        return super().validate(value=value)


class Puck(BaseSample):
    """Puck Model"""

    id: int = Field(
        title="ID",
        le=config.ASC_NUM_PUCKS,
        ge=1,
    )
    name: Optional[str] = Field(title="Name", default=None)

    def __str__(self: Self) -> str:
        return self.name or f"puck_{self.id}"

    @classmethod
    def validate(cls: Type[Self], value: Any) -> Self:
        if (isinstance(value, str) or isinstance(value, int)) and cls.is_valid_id(
            value
        ):
            value = {"id": value}
        return super().validate(value=value)


class HotPuck(Puck):
    """Puck Model"""

    id: int = Field(
        title="ID",
        le=101,
        ge=101,
        default=101,
    )


class Pin(BaseSample):
    """Pin Model"""

    id: int = Field(
        title="ID",
        le=config.ASC_NUM_PINS,
        ge=1,
    )
    puck: Union[Puck, HotPuck] = Field(
        title="Puck",
    )
    type: PinType = Field(
        title="Type",
        default=PinType.OTHER,
    )
    name: Optional[str] = Field(title="Name", default=None)

    def __iter__(self):
        for _id in (self.puck.id, self.id):
            yield _id

    def __str__(self: Self) -> str:
        return self.name or f"{str(self.puck)}[{self.id}]"

    @classmethod
    def validate(cls: Type[Self], value: Any) -> Self:
        if isinstance(value, (tuple, list)) and len(value) >= 2:
            _puck_id, _id = value[:2]
            if cls.is_valid_id(_puck_id) or cls.is_valid_id(_id):
                value = {"id": _id, "puck": {"id": _puck_id}}
            else:
                return None
        return super().validate(value=value)


class Plate(BaseSample):
    """Plate Model"""

    id: int = Field(
        title="ID",
        le=config.ASC_NUM_PLATES,
        ge=1,
    )
    # datamatrix: ? TBD

    @classmethod
    def validate(cls: Type[Self], value: Any) -> Self:
        if (isinstance(value, str) or isinstance(value, int)) and cls.is_valid_id(
            value
        ):
            value = {"id": value}
        return super().validate(value=value)
