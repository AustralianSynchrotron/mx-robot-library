from types import MappingProxyType
from typing import Any, Union

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    chain_schema,
    int_schema,
    no_info_after_validator_function,
    str_schema,
    union_schema,
)
from typing_extensions import Self

from .base import BaseRobotItem, BaseRobotMeta


class Position(BaseRobotItem):
    """Position Model"""

    @classmethod
    def _validate(cls: type[Self], value: Union[str, int]) -> Self:
        return RobotPositions[value]

    @classmethod
    def __get_pydantic_core_schema__(
        cls: type[Self],
        source: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        _core_schema = handler(source)
        return union_schema(
            choices=[
                _core_schema,
                chain_schema(
                    steps=[
                        no_info_after_validator_function(
                            function=cls._validate,
                            schema=union_schema(
                                choices=[
                                    str_schema(),
                                    int_schema(),
                                ],
                                strict=True,
                            ),
                        ),
                        _core_schema,
                    ],
                ),
            ],
            mode="left_to_right",
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls: type[Self],
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(schema)


class RobotPositionsMeta(BaseRobotMeta, item_cls=Position):
    """Positions Meta"""

    __items__: tuple[Position, ...]

    def __getitem__(self: Self, item: Union[str, int]) -> Position:
        return super().__getitem__(item=item)

    def __contains__(self: Self, item: Union[Position, str, int]) -> bool:
        return super().__getitem__(item=item)

    @property
    def _item_by_name(self: Self) -> MappingProxyType[str, Position]:
        return super()._item_by_name

    @property
    def _item_by_id(self: Self) -> MappingProxyType[int, Position]:
        return super()._item_by_id


class RobotPositions(metaclass=RobotPositionsMeta):
    """Robot Positions"""

    UNDEFINED = Position(
        id=0,
        name="Undefined",
        description="Undefined",
    )
    HOME = Position(
        id=100,
        name="HOME",
        description="",
    )
    SOAK = Position(
        id=110,
        name="SOAK",
        description="",
    )
    DEWAR_CENTER = Position(
        id=120,
        name="DEWAR_CENTER",
        description="",
    )
    DGRIPPER_STORE = Position(
        id=130,
        name="DGRIPPER_STORE",
        description="",
    )
    DRY_ZONE = Position(
        id=140,
        name="DRY_ZONE",
        description="",
    )
    DRY_START = Position(
        id=150,
        name="DRY_START",
        description="",
    )
    DRY_END = Position(
        id=160,
        name="DRY_END",
        description="",
    )
    GONIO = Position(
        id=170,
        name="GONIO",
        description="",
    )
    PLATE_GONIO = Position(
        id=180,
        name="PLATE_GONIO",
        description="",
    )
    PLATEGRIPPER_STORE = Position(
        id=190,
        name="PLATEGRIPPER_STORE",
        description="",
    )
    PLATEGRIPPER_HOME = Position(
        id=200,
        name="PLATEGRIPPER_HOME",
        description="",
    )
    CALIBRATION_TOOL = Position(
        id=210,
        name="CALIBRATION_TOOL",
        description="",
    )
    LASER_STORE = Position(
        id=220,
        name="LASER_STORE",
        description="",
    )
    PATH_TOOL_STORE = Position(
        id=500,
        name="PATH_TOOL_STORE",
        description="",
    )
    TOOL_STORE = Position(
        id=510,
        name="TOOL_STORE",
        description="",
    )
    PATH_GONIO_0 = Position(
        id=520,
        name="PATH_GONIO_0",
        description="",
    )
    PATH_PLATEHOLDER = Position(
        id=530,
        name="PATH_PLATEHOLDER",
        description="",
    )
    PLATE_TOOLSTORE = Position(
        id=540,
        name="PLATE_TOOLSTORE",
        description="",
    )
    PATH_DRY = Position(
        id=550,
        name="PATH_DRY",
        description="",
    )
    PATH_GONIO_1 = Position(
        id=560,
        name="PATH_GONIO_1",
        description="",
    )
    PATH_GONIO_2 = Position(
        id=570,
        name="PATH_GONIO_2",
        description="",
    )
    DRY_ZONE_00 = Position(
        id=800,
        name="00_DRY_ZONE",
        description="",
    )
    HOME_ZONE = Position(
        id=810,
        name="01_HOME_ZONE",
        description="",
    )
    TOOLPLATEHOLDER_ZONE = Position(
        id=820,
        name="02_TOOLPLATEHOLDER_ZONE",
        description="",
    )
    LSRTOOLCAL_ZONE = Position(
        id=825,
        name="02_LSRTOOLCAL_ZONE",
        description="",
    )
    TOOLSTORE_ZONE = Position(
        id=830,
        name="03_TOOLSTORE_ZONE",
        description="",
    )
    GONIORECT_ZONE = Position(
        id=840,
        name="04_GONIORECT_ZONE",
        description="",
    )
    MOTION_ZONE = Position(
        id=850,
        name="05_MOTION_ZONE",
        description="",
    )
    Q1 = Position(
        id=860,
        name="06_Q1",
        description="",
    )
    Q2 = Position(
        id=870,
        name="07_Q2",
        description="",
    )
    Q3 = Position(
        id=880,
        name="08_Q3",
        description="",
    )
    Q4 = Position(
        id=890,
        name="09_Q4",
        description="",
    )
    GONIO_DEADZONE = Position(
        id=900,
        name="04_GONIO_DEADZONE",
        description="",
    )
    DEWARZONEN2 = Position(
        id=910,
        name="01_DEWARZONEN2",
        description="",
    )
    DEWAR_ZONE = Position(
        id=920,
        name="02_DEWAR_ZONE",
        description="",
    )
    DEWAR_LID_DEADZONE = Position(
        id=930,
        name="03_DEWAR_LID_DEADZONE",
        description="",
    )
    CALIB_ZONE = Position(
        id=940,
        name="00_CALIB_ZONE",
        description="",
    )
    SOAK_ZONE = Position(
        id=950,
        name="00_SOAK_ZONE",
        description="",
    )
    ARM_IS_PARKED = Position(
        id=1000,
        name="10_ARM_IS_PARKED",
        description="",
    )
    DEADZONE_1 = Position(
        id=1010,
        name="11_DEADZONE_1",
        description="",
    )
    DEADZONE_2 = Position(
        id=1020,
        name="12_DEADZONE_2",
        description="",
    )
    DEADZONE_3 = Position(
        id=1030,
        name="15_DEADZONE_3",
        description="",
    )
    DEADZONE_4 = Position(
        id=1040,
        name="16_DEADZONE_4",
        description="",
    )
