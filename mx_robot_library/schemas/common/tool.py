from types import MappingProxyType
from typing import Any, Optional, Union

from pydantic import Field
from typing_extensions import Self

from mx_robot_library.config import get_settings

from .base import BaseRobotItem, BaseRobotMeta

config = get_settings()


class Tool(BaseRobotItem):
    """Tool Model"""

    change_time: Optional[float] = Field(
        title="Max Change Time",
        description=(
            "Maximum time expected to finish the tool change operation when"
            " the robot speed is set to 100%."
        ),
        default=None,
    )

    @classmethod
    def validate(cls: type[Self], value: Any) -> Self:
        """ """
        if (isinstance(value, str) or isinstance(value, int)) and value in RobotTools:
            return RobotTools[value]
        return super(Tool, cls).validate(value)


class RobotToolsMeta(BaseRobotMeta, item_cls=Tool):
    """Tool Meta"""

    __items__: tuple[Tool, ...]

    def __getitem__(self: Self, item: Union[str, int]) -> Tool:
        return super().__getitem__(item=item)

    def __contains__(self: Self, item: Union[Tool, str, int]) -> bool:
        return super().__getitem__(item=item)

    @property
    def _item_by_name(self: Self) -> MappingProxyType[str, Tool]:
        return super()._item_by_name

    @property
    def _item_by_id(self: Self) -> MappingProxyType[int, Tool]:
        return super()._item_by_id

    @property
    def available_tools(self: Self) -> tuple[Tool, ...]:
        """Get a list of tools available to be mounted on the ASC arm.

        Returns
        -------
        tuple[Tool, ...]
            Available tools.
        """
        return tuple(
            [self.__items__[item] for item in config.ASC_TOOLS if item in self]
        )


class RobotTools(metaclass=RobotToolsMeta):
    """Robot Tools"""

    TOOL_CHANGER = Tool(
        id=0,
        name="ToolChanger",
        description="Tool Changer",
    )
    CRYOTONG = Tool(
        id=1,
        name="Cryotong",
        description="Cryotong gripper (Actor or Unipuck)",
    )
    SINGLE_GRIPPER = Tool(
        id=2,
        name="SingleGripper",
        description="Single magnetic gripper (Unipuck)",
    )
    DOUBLE_GRIPPER = Tool(
        id=3,
        name="DoubleGripper",
        description="Double magnetic gripper (Unipuck)",
    )
    MINISPINE_GRIPPER = Tool(
        id=4,
        name="MiniSpineGripper",
        description="MiniSpine gripper",
    )
    ROTATING_GRIPPER = Tool(
        id=5,
        name="RotatingGripper",
        description="Rotating gripper (SC3)",
    )
    PLATE_GRIPPER = Tool(
        id=6,
        name="PlateGripper",
        description="Plate gripper",
    )
    SPARE = Tool(
        id=7,
        name="Spare",
        description="Spare",
    )
    LASER_TOOL = Tool(
        id=8,
        name="LaserTool",
        description="Laser teaching tool",
    )
