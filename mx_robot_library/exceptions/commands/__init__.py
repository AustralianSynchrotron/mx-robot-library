from typing import Union, Annotated
from typing_extensions import TypeAlias
from pydantic import Field
from .common import common_errors
from .cv import cv_errors
from .pla import pla_errors
from .trajectory import trajectory_errors

__all__ = ("command_errors",)

command_errors: TypeAlias = Annotated[
    Union[
        common_errors,
        cv_errors,
        pla_errors,
        trajectory_errors,
    ],
    Field(union_mode="left_to_right"),
]
