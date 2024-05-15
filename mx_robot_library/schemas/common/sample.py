from enum import Enum
from typing import Annotated, Any, Type, Union
from typing_extensions import Self
from pydantic import BaseModel, Field, validate_call
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core.core_schema import no_info_before_validator_function
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

    def __eq__(self: Self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return self.id == __value.id
        return super().__eq__(__value)

    @staticmethod
    @validate_call
    def is_valid_id(
        id: Annotated[
            Union[int, str],
            Field(union_mode="left_to_right"),
        ],
    ) -> bool:
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
    def _validate(cls: Type[Self], value: Any) -> Self:
        if value == "-1":
            return None
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls: type[Self],
        source: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return no_info_before_validator_function(
            function=cls._validate,
            schema=handler(source),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls: type[Self],
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(schema)


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
    def _validate(cls: Type[Self], value: Any) -> Self:
        if (isinstance(value, str) or isinstance(value, int)) and cls.is_valid_id(
            value
        ):
            value = {"id": value}
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls: type[Self],
        source: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return no_info_before_validator_function(
            function=cls._validate,
            schema=handler(source),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls: type[Self],
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(schema)


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
    puck: Annotated[Union[Puck, HotPuck], Field(union_mode="left_to_right")] = Field(
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

    def __eq__(self: Self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return self.puck.id == __value.puck.id and self.id == __value.id
        return super().__eq__(__value)

    @classmethod
    def _validate(cls: Type[Self], value: Any) -> Self:
        if isinstance(value, tuple) or isinstance(value, list) and len(value) >= 2:
            _puck_id, _id = value[:2]
            if cls.is_valid_id(_puck_id) or cls.is_valid_id(_id):
                value = {"id": _id, "puck": {"id": _puck_id}}
            else:
                return None
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls: Type[Self],
        source: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return no_info_before_validator_function(
            function=cls._validate,
            schema=handler(source),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls: Type[Self],
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(schema)


class Plate(BaseSample):
    """Plate Model"""

    id: int = Field(
        title="ID",
        le=config.ASC_NUM_PLATES,
        ge=1,
    )
    # datamatrix: ? TBD

    @classmethod
    def _validate(cls: Type[Self], value: Any) -> Self:
        if (isinstance(value, str) or isinstance(value, int)) and cls.is_valid_id(
            value
        ):
            value = {"id": value}
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls: Type[Self],
        source: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return no_info_before_validator_function(
            function=cls._validate,
            schema=handler(source),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls: Type[Self],
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(schema)
