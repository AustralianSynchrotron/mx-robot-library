from typing import TYPE_CHECKING, Optional

from pydantic import validate_call

from .client.base import CmdChannel, SubClient
from .decorators import raise_ex
from .schemas.commands.general import RobotGeneralCmd, RobotGeneralCmds
from .schemas.responses.common import CommonResponse

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

    def send_cmd(
        self, cmd: RobotGeneralCmds, args: Optional[list] = None
    ) -> CommonResponse:
        """Send a command to the robot and receive echo reply.

        Parameters
        ----------
        cmd : RobotGeneralCmds
            Command to send to the robot.
        args : list, optional
            Command arguments, by default None

        Returns
        -------
        CommonResponse
            Decoded response from the robot.
        """
        return CommonResponse.parse_cmd_output(
            cmd=cmd,
            obj=super().send_cmd(cmd=RobotGeneralCmd(cmd=cmd, args=args).cmd_fmt),
        )

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
    @validate_call
    def power(self, value: bool, *args, **kwargs) -> CommonResponse:
        """Set power status of the robot arm.

        Parameters
        ----------
        value : bool
            Value to set power property.

        Returns
        -------
        CommonResponse
            Decoded response from the robot.
        """
        return self.send_cmd(
            cmd=RobotGeneralCmds.ON if value else RobotGeneralCmds.OFF,
        )

    @raise_ex
    @validate_call
    def reset(self, *args, **kwargs) -> bytes:
        """Acknowledge and reset security fault and allow user to bring power back.

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.RESET)

    @raise_ex
    @validate_call
    def speed_up(self, *args, **kwargs) -> CommonResponse:
        """Increase robot speed (range from 0.01% to 100%).

        Returns
        -------
        CommonResponse
            Decoded response from the robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.SPEED_UP)

    @raise_ex
    @validate_call
    def slow_down(self, *args, **kwargs) -> CommonResponse:
        """Decrease robot speed (range from 0.01% to 100%).

        Returns
        -------
        CommonResponse
            Decoded response from the robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.SLOW_DOWN)

    @raise_ex
    @validate_call
    def close_lid(self, *args, **kwargs) -> CommonResponse:
        """Close lid

        Returns
        -------
        CommonResponse
            Decoded response from the robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.CLOSE_LID)

    @raise_ex
    @validate_call
    def open_lid(self, *args, **kwargs) -> CommonResponse:
        """Open lid

        Returns
        -------
        CommonResponse
            Decoded response from the robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.OPEN_LID)

    @raise_ex
    @validate_call
    def abort(self, *args, **kwargs) -> CommonResponse:
        """Abort

        Returns
        -------
        CommonResponse
            Decoded response from the robot.
        """
        return self.send_cmd(cmd=RobotGeneralCmds.ABORT)
