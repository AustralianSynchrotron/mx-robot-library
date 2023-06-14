from typing import Optional, Union
from typing_extensions import TypeAlias
from pydantic import Field
from pydantic.dataclasses import dataclass
from ..base import PLCError


@dataclass(frozen=True)
class CmdNotFound(PLCError):
    """Command Not Found"""
    # Command not found

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bcommand\b.*\bnot\b.*\bfound\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Command not found.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="Command referenced in the command call does not exist.",
    )


@dataclass(frozen=True)
class ManualModeError(PLCError):
    """Manual Mode Error"""
    # Remote mode requested

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bremote\b.*\bmode\b.*\brequested\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Remote mode requested.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="Requested operation requires remote mode to be engaged.",
    )


@dataclass(frozen=True)
class DoorOpenError(PLCError):
    """Door Open Error"""
    # Doors must be closed

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bdoors\b.*\bmust\b.*\bclosed\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Door(s) is(are) opened.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="One or more door interlocks are not engaged.",
    )


@dataclass(frozen=True)
class EmergencyStop(PLCError):
    """Emergency Stop"""
    # Emergency stop triggered

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bemergency\b.*\bstop\b.*\btriggered\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Emergency stop has been triggered.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="One or several emergency-stop button(s) is (are) triggered.",
    )


@dataclass(frozen=True)
class SystemFault(PLCError):
    """System Fault"""
    # System fault active

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bsystem\b.*\bfault\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="System fault active.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="One or several emergency-stop button(s) is (are) triggered.",
    )


@dataclass(frozen=True)
class InconsistentParams(PLCError):
    """Inconsistent Parameters"""
    # Inconsistent parameters

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\binconsistent\b.*\bparameters\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Invalid parameters specified.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="Parameters specified in command call are invalid.",
    )


@dataclass(frozen=True)
class OrderRejected(PLCError):
    """Order Rejected"""
    # Order rejected

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\border\b.*\brejected\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Order rejected.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="Command call was rejected.",
    )


@dataclass(frozen=True)
class PathRunningError(PLCError):
    """Path Running Error"""
    # Disabled when path is running
    # Path already running

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bpath\b.*(?:\bis\b|\balready\b).*\brunning\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Path already running.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The robot is already busy running another path.",
    )


@dataclass(frozen=True)
class SafetyRestartRequired(PLCError):
    """Safety Restart Required"""
    # Safety restart needed
    # A safety restart is required ("Restart" button on WMS)

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bsafety\b.*\brestart\b.*(?:\bneeded\b|\brequired\b).*",
        default=None,
    )
    msg: str = Field(title="Message", default="Safety restart required.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The robot PLC is locked and needs to be power-cycled.",
    )


@dataclass(frozen=True)
class DeviceNotResponding(PLCError):
    """Device Not Responding"""
    # Device not responding

    response: Optional[str] = Field(
        title="Response",
        description="Response received from the command call.",
        regex=r"(?i).*\bdevice\b.*\bnot\b.*\bresponding\b.*",
        default=None,
    )
    msg: str = Field(title="Message", default="Device not responding.")
    detail: Optional[str] = Field(
        title="Detail",
        description="Detailed error message.",
        default="The PLC cannot communicate with the requested module.",
    )


common_errors: TypeAlias = Union[
    CmdNotFound,
    ManualModeError,
    DoorOpenError,
    EmergencyStop,
    SystemFault,
    InconsistentParams,
    OrderRejected,
    PathRunningError,
    SafetyRestartRequired,
    DeviceNotResponding,
]
