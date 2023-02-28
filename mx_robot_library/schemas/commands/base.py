from enum import Enum
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, validator


class CmdField(BaseModel):
    """Command Field Model"""

    title: str
    description: Optional[str]
    value: str


class BaseCmdModel(BaseModel):
    """Abstract Command Model"""

    cmd: str = Field(
        title="Command",
        regex=r"^[^\(\)\s]*$",
    )
    args: Optional[list] = Field(title="Arguments")
    cmd_fmt: Optional[str] = Field(
        title="Formatted Command",
        description="Formatted command to be passed via socket connection.",
        regex=r"^[^\(\)\s]*\r|^\S*\(.*\)\r",
    )

    class Config:
        validate_assignment: bool = True

    def __setattr__(self, name: str, value: Any) -> Any:
        res = super().__setattr__(name, value)

        # When "cmd" or "args" fields are updated we'll trigger "cmd_fmt" to recompute.
        if name in ["cmd", "args"]:
            self.cmd_fmt = self.__class__.compute_cmd_fmt(
                v=self.cmd_fmt,
                values=self.dict(),
            )
        return res

    @validator("cmd_fmt", pre=True, always=True)
    def compute_cmd_fmt(
        cls, v: Optional[str], values: Dict[str, Any]  # noqa: B902
    ) -> str:
        if values.get("cmd") and values.get("args"):
            v = f"{values['cmd']}({','.join([str(arg) for arg in values['args']])})\r"
        elif values.get("cmd"):
            v = f"{values['cmd']}\r"
        return v


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
