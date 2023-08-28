from typing import Any, Union

from typing_extensions import Self

from ..common import Common
from ..config import get_settings
from ..exceptions.client import ClientReadonly
from ..logger import get_logger
from ..status import Status
from ..trajectory import Trajectory
from ..types import HostAddress
from ..utils import Utils
from .base import RootClient

logger = get_logger()
config = get_settings()


class Client(RootClient):
    """Robot Client"""

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
        super().__init__(
            host=host,
            status_port=status_port,
            cmd_port=cmd_port,
            readonly=readonly,
        )
        self._status: Union[Status, None] = None
        self._trajectory: Union[Trajectory, None] = None
        self._common: Union[Common, None] = None
        self._utils: Union[Utils, None] = None

    @classmethod
    def validate(cls, value: Any) -> Self:
        if isinstance(value, str):
            try:
                return cls(host=value)
            except Exception:
                pass
        elif isinstance(value, dict):
            try:
                return cls(**value)
            except Exception:
                pass
        elif isinstance(value, tuple):
            try:
                return cls(*value)
            except Exception:
                pass
        return super(Client, cls).validate(value=value)

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
        Trajectory
            Instance of the trajectory sub-client.
        """

        if self.readonly:
            raise ClientReadonly("Client is in readonly mode.")

        if not self._trajectory:
            self._trajectory = Trajectory(client=self)
        return self._trajectory

    @property
    def common(self) -> Common:
        """Sub-client to handle calls to robot common commands.

        Returns
        -------
        Common
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
