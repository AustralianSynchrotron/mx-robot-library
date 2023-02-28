from typing import Union
from socket import socket, AF_INET, SOCK_STREAM
from .logger import get_logger
from .config import get_settings
from .exceptions import ClientReadonly
from .status import Status
from .trajectory import Trajectory
from .common import Common
from .utils import Utils

logger = get_logger()
config = get_settings()


class Client:
    """Robot Client"""

    def __init__(
        self,
        host: str,
        status_port: int = config.ASC_STATUS_PORT,
        cmd_port: int = config.ASC_CMD_PORT,
        readonly=True,
    ) -> None:
        """
        Parameters
        ----------
        host : str
            Controller host address.
        status_port : int, optional
            Controller status command port, by default config.ASC_STATUS_PORT
        cmd_port : int, optional
            Controller command port, by default config.ASC_CMD_PORT
        readonly : bool, optional
            Is created client readonly, by default True
        """

        self._host: str = host
        self._status_port: int = status_port
        self._cmd_port: int = cmd_port
        self._readonly: bool = readonly
        self._status: Union[Status, None] = None
        self._trajectory: Union[Trajectory, None] = None
        self._common: Union[Common, None] = None
        self._utils: Union[Utils, None] = None

    @property
    def status(self) -> Status:
        """Sub-client to handle calls to robot status commands.

        Returns
        -------
        Status
            Instance of the status sub-client.
        """

        if not self._status:
            self._status = Status(client=self)
        return self._status

    @property
    def trajectory(self) -> Trajectory:
        """Sub-client to handle calls to robot trajectory commands.

        Returns
        -------
        Status
            Instance of the trajectory sub-client.
        """

        if self._readonly:
            raise ClientReadonly("Client is in readonly mode.")

        if not self._trajectory:
            self._trajectory = Trajectory(client=self)
        return self._trajectory

    @property
    def common(self) -> Common:
        """Sub-client to handle calls to robot common commands.

        Returns
        -------
        Status
            Instance of the common sub-client.
        """

        if not self._common:
            self._common = Common(client=self)
        return self._common

    @property
    def utils(self) -> Utils:
        """Common utilities.

        Returns
        -------
        Utils
            Instance of utils.
        """

        if not self._utils:
            self._utils = Utils(client=self)
        return self._utils

    def _send_cmd(
        self,
        cmd: Union[str, bytes],
        port: int,
        timeout: float = config.ASC_CMD_TIMEOUT,
    ) -> bytes:
        """Send a command to the robot, then receive it's response.

        Parameters
        ----------
        cmd : Union[bytes, str]
            Structured command to send to the robot.
        sock : socket
            Socket to send the command over.
        port : int
            Port for socket to connect.
        timeout : float, optional
            Command timeout, by default config.ASC_CMD_TIMEOUT

        Returns
        -------
        bytes
            Reply to be decoded from robot.

        Raises
        ------
        error
            _description_
        error
            _description_
        error
            _description_
        """

        if isinstance(cmd, str):
            cmd = cmd.encode("utf-8")

        data: bytes
        with socket(family=AF_INET, type=SOCK_STREAM) as sock:
            # TODO: Implement retry logic and improve targeting of the error handling.
            try:
                logger.debug(
                    f"Attempting Connection: Host={self._host}, Port={port}",
                )
                sock.settimeout(timeout)
                sock.connect((self._host, port))
            except Exception as error:
                logger.error(f"Connecting Failed: {error}")
                raise error

            try:
                logger.debug(f"Sending Command: {cmd}")
                sock.sendall(cmd)
            except Exception as error:
                logger.error(f"Send Failed: {error}")
                raise error

            try:
                data = sock.recv(2048)
            except Exception as error:
                logger.error(f"Receive Failed: {error}")
                raise error

            data_str = data.decode("utf-8")
            logger.debug(f"Response: {data_str}")
        return data
