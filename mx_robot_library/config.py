import logging
from functools import lru_cache
from typing import Annotated, Optional, Tuple, Union

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ASCSettings(BaseSettings):
    """Automatic Sample Changer Settings"""

    ASC_NUM_PUCKS: int = Field(
        title="Number of Pucks",
        description="Total number of pucks supported.",
        default=29,
    )
    ASC_NUM_PINS: int = Field(
        title="Number of Pins",
        description="Total number of pins per puck supported.",
        default=16,
    )
    ASC_NUM_PLATES: int = Field(
        title="Number of Trays",
        description="Total number of trays supported.",
        default=20,
    )
    ASC_TOOLS: Tuple[
        Annotated[Union[str, int], Field(union_mode="left_to_right")], ...
    ] = Field(
        title="Supported Tools",
        description="List of tools supported by this ASC.",
        default=("ToolChanger", "DoubleGripper", "PlateGripper", "LaserTool"),
    )
    ASC_CMD_TIMEOUT: float = Field(
        title="Command Timeout",
        description="Seconds for connection to timeout, when sending a command.",
        default=5.0,
    )
    ASC_STATUS_PORT: int = Field(
        title="Status Port",
        description="Port the client will send status commands over.",
        default=1000,
    )
    ASC_CMD_PORT: int = Field(
        title="Command Port",
        description="Port the client will send all actionable commands over.",
        default=10000,
    )
    ASC_LOG_NAME: str = Field(
        title="Logger Name",
        default="MX_ROBOT",
    )
    ASC_LOG_LEVEL: int = Field(
        title="Logger Level",
        default=logging.INFO,
    )
    ASC_LOG_FORMAT: str = Field(
        title="Logger Format",
        default="%(asctime)s %(name)s :: %(levelname)-8s :: %(message)s",
    )
    ASC_LOG_PATH: Optional[str] = Field(
        title="Logger File Path",
        default=None,
    )


class Settings(ASCSettings):
    """Settings"""

    model_config = SettingsConfigDict(
        str_strip_whitespace=True,
        env_prefix="MX_",
        validate_assignment=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """Cache the settings, this allows the settings to be used in dependencies and
    for overwriting in tests
    """
    return Settings()
