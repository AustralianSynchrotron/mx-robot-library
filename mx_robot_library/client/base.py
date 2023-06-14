from enum import Enum
from socket import AF_INET, SOCK_STREAM, socket
from typing import TYPE_CHECKING, Any

from pydantic import validate_arguments
from typing_extensions import Self

from ..config import get_settings
from ..logger import get_logger
from ..types import HostAddress

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator

logger = get_logger()
config = get_settings()


class CmdChannel(str, Enum):
    """Command Channel"""

    STATUS = "status"
    CMD = "cmd"


class BaseClient:
    """Abstract Base Client"""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Self:
        if isinstance(value, cls):
            return value


class RootClient(BaseClient):
    """Root Client"""

    @validate_arguments
    def __init__(
        self,
        host: HostAddress,
        status_port: int = config.ASC_STATUS_PORT,
        cmd_port: int = config.ASC_CMD_PORT,
        readonly: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        host : HostAddress
            Controller host address.
        status_port : int, optional
            Controller status command port, by default config.ASC_STATUS_PORT
        cmd_port : int, optional
            Controller command port, by default config.ASC_CMD_PORT
        readonly : bool, optional
            Is created client readonly, by default True
        """
        self.host: str = host
        self.status_port: int = status_port
        self.cmd_port: int = cmd_port
        self.readonly: bool = readonly

    @validate_arguments
    def send_cmd(
        self,
        cmd: bytes,
        port: int,
        timeout: float = config.ASC_CMD_TIMEOUT,
    ) -> bytes:
        """Send a command to the robot, then receive it's response.

        Parameters
        ----------
        cmd : bytes
            Structured command to send to the robot.
        port : int
            Port for socket to connect.
        timeout : float, optional
            Command timeout, by default config.ASC_CMD_TIMEOUT

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        data: bytes
        with socket(family=AF_INET, type=SOCK_STREAM) as sock:
            # Open socket connection
            try:
                logger.debug(
                    f"Attempting Connection: Host={self.host}, Port={port}",
                )
                sock.settimeout(timeout)
                sock.connect((self.host, port))
            except Exception as ex:
                logger.error(f"Connecting Failed: {ex}")
                raise ex

            # Send command packet
            try:
                logger.debug(f"Sending Command: {cmd}")
                sock.sendall(cmd)
            except Exception as ex:
                logger.error(f"Send Failed: {ex}")
                raise ex

            # Recieve PLC reply packet
            try:
                data = sock.recv(2048)
            except Exception as ex:
                logger.error(f"Receive Failed: {ex}")
                raise ex

            logger.debug(f"Response: {data}")
        return data


class SubClient(BaseClient):
    """Robot Sub-Client"""

    channel: CmdChannel = CmdChannel.STATUS

    def __init_subclass__(cls, channel: CmdChannel) -> None:
        """
        Parameters
        ----------
        channel : CmdChannel
            Sub-client command channel.
        """
        if channel == CmdChannel.CMD:
            cls.channel == CmdChannel.CMD
        else:
            cls.channel == CmdChannel.STATUS

    @validate_arguments
    def __init__(self, client: RootClient) -> None:
        """
        Parameters
        ----------
        client : RootClient
            Root client.
        """
        self._client = client

    @property
    def host(self) -> str:
        """Client host.

        Returns
        -------
        str
            Host.
        """
        return self._client.host

    @property
    def port(self) -> int:
        """Client port.

        Returns
        -------
        int
            Port.
        """
        if self.channel == CmdChannel.CMD:
            return self._client.cmd_port
        return self._client.status_port

    @validate_arguments
    def send_cmd(self, cmd: bytes, timeout: float = config.ASC_CMD_TIMEOUT) -> bytes:
        """Send a command to the robot, then receive it's response.

        Parameters
        ----------
        cmd : bytes
            Structured command to send to the robot.
        timeout : float, optional
            Command timeout, by default config.ASC_CMD_TIMEOUT

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """
        return self._client.send_cmd(cmd=cmd, port=self.port, timeout=timeout)
