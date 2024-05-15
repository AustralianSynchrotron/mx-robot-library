from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Any, TYPE_CHECKING, Union
from typing_extensions import Self
from pydantic import (
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    ValidationError,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError, Url
from pydantic_core.core_schema import (
    chain_schema,
    union_schema,
    str_schema,
    url_schema,
    no_info_wrap_validator_function,
    ValidatorFunctionWrapHandler,
    any_schema,
)

__all__ = ("HostAddress",)


if TYPE_CHECKING:
    HostAddress = Union[Url, IPv4Address, str]
else:
    @dataclass()
    class HostAddress:

        @classmethod
        def _validate(cls: type[Self], value: str, handler: ValidatorFunctionWrapHandler) -> str:
            try:
                handler(value)
            except ValidationError:
                try:
                    _url: Url = handler(f"http://{value}")
                    return _url.host
                except ValidationError as _ex:
                    raise PydanticCustomError(
                        "host_address_invalid",
                        "Host address passed is in an invalid format."
                    ) from _ex
            raise PydanticCustomError(
                "host_address_url",
                (
                    "Input value is a URL, "
                    f"which is an invalid input type for {cls.__name__}."
                ),
            )

        @classmethod
        def __get_pydantic_core_schema__(
            cls: type[Self],
            source: Any,
            handler: GetCoreSchemaHandler,
        ) -> CoreSchema:
            return chain_schema(
                steps=[
                    union_schema(
                        choices=[
                            str_schema(strip_whitespace=True, strict=True),
                            any_schema(),
                        ],
                        mode="left_to_right",
                        strict=False,
                    ),
                    union_schema(
                        choices=[
                            str_schema(pattern=r"^localhost$|^127\.0\.0\.1$"),
                            chain_schema(
                                steps=[
                                    handler.generate_schema(IPv4Address),
                                    str_schema(),
                                ],
                            ),
                            chain_schema(steps=[
                                str_schema(strip_whitespace=True),
                                no_info_wrap_validator_function(
                                    function=cls._validate,
                                    schema=url_schema(host_required=True, default_path="/"),
                                )
                            ])
                        ],
                        mode="left_to_right",
                    ),
                ],
            )

        @classmethod
        def __get_pydantic_json_schema__(
            cls: type[Self],
            schema: CoreSchema,
            handler: GetJsonSchemaHandler,
        ) -> JsonSchemaValue:
            return handler(schema)

        __hash__ = object.__hash__
