from typing import Union
from typing_extensions import TypeAlias
from .common import common_errors
from .cv import cv_errors
from .pla import pla_errors
from .trajectory import trajectory_errors

command_errors: TypeAlias = Union[
    common_errors,
    cv_errors,
    pla_errors,
    trajectory_errors,
]
