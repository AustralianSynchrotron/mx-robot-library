from types import MappingProxyType
from typing import Any, Union

from typing_extensions import Self

from .base import BaseRobotItem, BaseRobotMeta


class Path(BaseRobotItem):
    """Path Model"""

    @classmethod
    def validate(cls: type[Self], value: Any) -> Self:
        """ """
        if (isinstance(value, str) or isinstance(value, int)) and value in RobotPaths:
            return RobotPaths[value]
        return super(Path, cls).validate(value)


class RobotPathsMeta(BaseRobotMeta, item_cls=Path):
    """Paths Meta"""

    __items__: tuple[Path, ...]

    def __getitem__(self: Self, item: Union[str, int]) -> Path:
        return super().__getitem__(item=item)

    def __contains__(self: Self, item: Union[Path, str, int]) -> bool:
        return super().__getitem__(item=item)

    @property
    def _item_by_name(self: Self) -> MappingProxyType[str, Path]:
        return super()._item_by_name

    @property
    def _item_by_id(self: Self) -> MappingProxyType[int, Path]:
        return super()._item_by_id


class RobotPaths(metaclass=RobotPathsMeta):
    """Robot Paths"""

    UNDEFINED = Path(
        id=0,
        name="",
        description="Undefined",
    )
    HOME = Path(
        id=1000,
        name="home",
        description="",
    )
    PUT = Path(
        id=2000,
        name="put",
        description="",
    )
    GET = Path(
        id=3000,
        name="get",
        description="",
    )
    GET_PUT = Path(
        id=4000,
        name="getput",
        description="",
    )
    PICK = Path(
        id=5000,
        name="pick",
        description="",
    )
    SOAK = Path(
        id=6000,
        name="soak",
        description="",
    )
    DRY = Path(
        id=7000,
        name="dry",
        description="",
    )
    DATAMATRIX = Path(
        id=8000,
        name="datamatrix",
        description="",
    )
    PUT_PLATE = Path(
        id=9000,
        name="putplate",
        description="",
    )
    GET_PLATE = Path(
        id=10000,
        name="getplate",
        description="",
    )
    CHANGE_TOOL = Path(
        id=20000,
        name="changetool",
        description="",
    )
    TOOL_CAL = Path(
        id=21000,
        name="toolcal",
        description="",
    )
    TEACH_PUCK = Path(
        id=22000,
        name="teachpuck",
        description="",
    )
    TEACH_DEWAR = Path(
        id=23000,
        name="teachdewar",
        description="",
    )
    TEACH_GONI = Path(
        id=24000,
        name="teachgonio",
        description="",
    )
    TEACH_PLATE_HOLDER = Path(
        id=25000,
        name="teachplateholder",
        description="",
    )
    RECOVER = Path(
        id=30000,
        name="recover",
        description="",
    )
    BACK = Path(
        id=31000,
        name="back",
        description="",
    )
    GOTO_DIF = Path(
        id=32000,
        name="gotodif",
        description="",
    )
    PLATE_TO_DIF = Path(
        id=33000,
        name="platetodif",
        description="",
    )
