from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CmdField(BaseModel):
    """Command Field Model"""

    title: str
    description: Optional[str]
    value: str


class BaseCmdModel(BaseModel):
    """Abstract Command Model"""

    cmd: str = Field(
        title="Command",
        pattern=r"^[^\(\)\s]*$",
    )
    args: Optional[list] = Field(title="Arguments", default=None)
    cmd_fmt: str = Field(
        title="Formatted Command",
        description="Formatted command to be passed via socket connection.",
        pattern=r"^[^\(\)\s]*\r|^\S*\(.*\)\r",
    )

    model_config = ConfigDict(validate_assignment=True)

    def __setattr__(self, name: str, value: Any) -> Any:
        res = super().__setattr__(name, value)

        # When "cmd" or "args" fields are updated we'll trigger "cmd_fmt" to recompute.
        if name in ["cmd", "args"]:
            self.cmd_fmt = self.__class__.compute_cmd_fmt(
                v=self.cmd_fmt,
                values=self.model_dump(warnings=False),
            )
        return res

    @classmethod
    @model_validator(mode="before")
    def compute_cmd_fmt(cls, value: Any) -> Any:
        if isinstance(value, dict):
            if value.get("cmd") and value.get("args"):
                _args = ",".join([str(arg) for arg in value["args"]])
                value["cmd_fmt"] = f"{value['cmd']}({_args})\r"
            elif value.get("cmd"):
                value["cmd_fmt"] = f"{value['cmd']}\r"
        return value


class CmdEnum(Enum):
    """Abstract Command Enum"""

    _value_: CmdField

    @property
    def title(self) -> str:
        return self._value_.title

    @property
    def description(self) -> Union[str, None]:
        return self._value_.description

    @property
    def value(self) -> str:
        return self._value_.value

    def __str__(self) -> str:
        return self.value
