from typing import TYPE_CHECKING, Optional

from ..client.base import CmdChannel, SubClient
from ..schemas.responses.trajectory import TrajectoryResponse

if TYPE_CHECKING:
    from ..client.client import Client
    from ..schemas.commands.trajectory import BaseTrajectoryCmd
    from .trajectory import Trajectory


class SubTrajectory(SubClient, channel=CmdChannel.CMD):
    """Trajectory Sub-Client"""

    def __init__(self, parent: "Trajectory") -> None:
        self._client: "Client"
        self._parent = parent
        super().__init__(client=parent._client)

    def send_cmd(
        self, cmd: type["BaseTrajectoryCmd"], args: Optional[list] = None
    ) -> TrajectoryResponse:
        """Send a command to the robot, then receive it's response.

        Parameters
        ----------
        cmd : type[BaseTrajectoryCmd]
            Command to send to the robot.
        args : list, optional
            Command arguments, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """
        return self._parent.send_cmd(cmd=cmd, args=args)
