from typing import TYPE_CHECKING, Optional

from pydantic import validate_arguments

from .client.base import CmdChannel, SubClient
from .decorators import raise_ex
from .schemas.commands.general import RobotGeneralCmd, RobotGeneralCmds

if TYPE_CHECKING:
    from .client import Client


class Common(SubClient, channel=CmdChannel.CMD):
    """Robot Common"""

    def __init__(self, client: "Client") -> None:
        """
        Parameters
        ----------
        client : Client
            Client.
        """
        self._client: "Client"
        super().__init__(client=client)

    def send_cmd(self, cmd: RobotGeneralCmds, args: Optional[list] = None) -> bytes:
        """Send a command to the robot and receive echo reply.

        Parameters
        ----------
        cmd : RobotGeneralCmds
            Command to send to the robot.
        args : list, optional
            Command arguments, by default None

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """
        return super().send_cmd(cmd=RobotGeneralCmd(cmd=cmd, args=args).cmd_fmt)

    @property
    def power(self) -> bool:
        """Get power status of the robot arm.

        Returns
        -------
        bool
            True if power enabled, otherwise False.
        """
        return self._client.status.state.power

    @power.setter
    @raise_ex
    @validate_arguments
    def power(self, value: bool) -> None:
        """Set power status of the robot arm.

        Parameters
        ----------
        value : bool
            Value to set power property.

        Returns
        -------
        None
        """
        self.send_cmd(cmd=RobotGeneralCmds.ON if value else RobotGeneralCmds.OFF)

    @raise_ex
    @validate_arguments
    def reset(self) -> bytes:
        """Acknowledge and reset security fault and allow user to bring power back.

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.RESET)

    @raise_ex
    @validate_arguments
    def speed_up(self) -> bytes:
        """Increase robot speed (range from 0.01% to 100%).

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.SPEED_UP)

    @raise_ex
    @validate_arguments
    def slow_down(self) -> bytes:
        """Decrease robot speed (range from 0.01% to 100%).

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.SLOW_DOWN)
