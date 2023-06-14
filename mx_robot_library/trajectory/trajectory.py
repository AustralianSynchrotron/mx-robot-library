from typing import TYPE_CHECKING, Optional, Union

from pydantic import validate_arguments
from typing_extensions import Annotated

from ..schemas.commands.trajectory import (
    BaseTrajectoryCmd,
    RobotTrajCalibrateToolCmd,
    RobotTrajChangeToolCmd,
    RobotTrajDryToolCmd,
    RobotTrajMoveHomeDirectCmd,
    RobotTrajMoveHomeSafeCmd,
    RobotTrajSoakToolCmd,
)
from ..schemas.responses.trajectory import TrajectoryResponse
from ..schemas.common.tool import RobotTools, Tool
from ..schemas.common.path import RobotPaths
from ..client.base import SubClient, CmdChannel
from ..decorators import check_tool, raise_ex, wait_for_path
from .hotpuck import HotPuckTraj
from .plate import PlateTraj
from .puck import PuckTraj

if TYPE_CHECKING:
    from ..client import Client


class Trajectory(SubClient, channel=CmdChannel.CMD):
    """Robot Trajectory"""

    def __init__(self, client: "Client") -> None:
        """
        Parameters
        ----------
        client : Client
            Client.
        """
        self._client: "Client"
        super().__init__(client=client)
        self._hot_puck: Union[HotPuckTraj, None] = None
        self._plate: Union[PlateTraj, None] = None
        self._puck: Union[PuckTraj, None] = None

    @property
    def hot_puck(self) -> HotPuckTraj:
        """Sub-client to handle calls to robot hot puck trajectory commands.

        Returns
        -------
        HotPuckTraj
            Instance of the hot puck trajectory sub-client.
        """

        if not self._hot_puck:
            self._hot_puck = HotPuckTraj(parent=self)
        return self._hot_puck

    @property
    def plate(self) -> PlateTraj:
        """Sub-client to handle calls to robot plate trajectory commands.

        Returns
        -------
        PlateTraj
            Instance of the plate trajectory sub-client.
        """

        if not self._plate:
            self._plate = PlateTraj(parent=self)
        return self._plate

    @property
    def puck(self) -> PuckTraj:
        """Sub-client to handle calls to robot puck trajectory commands.

        Returns
        -------
        PuckTraj
            Instance of the puck trajectory sub-client.
        """

        if not self._puck:
            self._puck = PuckTraj(parent=self)
        return self._puck

    def send_cmd(
        self, cmd: type[BaseTrajectoryCmd], args: Optional[list] = None
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

        # Generate command instance from command arguments
        _cmd = cmd(args=(args if args is not None else []))

        # Send formatted command to robot
        _msg = super().send_cmd(cmd=_cmd.cmd_fmt)

        return TrajectoryResponse.parse_cmd_output(cmd=_cmd, obj=_msg)

    @raise_ex
    @wait_for_path(path=RobotPaths.HOME)
    @validate_arguments
    def home(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Move the robot arm back to home position.

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self.send_cmd(cmd=RobotTrajMoveHomeDirectCmd, args=[tool])

    @raise_ex
    @wait_for_path(path=RobotPaths.RECOVER)
    @validate_arguments
    def recover(self, tool: Optional[Annotated[Tool, RobotTools]] = None) -> TrajectoryResponse:
        """Recover the robot arm back to home position.

        This command works different to the "home" trajectory, as the robot will move
        very slowly back to the home position in a safety mode.

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self.send_cmd(cmd=RobotTrajMoveHomeSafeCmd, args=[tool])

    @raise_ex
    @wait_for_path(path=RobotPaths.TEACH_GONI)
    @check_tool(tool=RobotTools.LASER_TOOL)
    @validate_arguments
    def teach_goni(self) -> TrajectoryResponse:
        """ """

        # RobotTrajTeachGonioCmd
        raise NotImplementedError

    @raise_ex
    @wait_for_path(path=RobotPaths.TEACH_PUCK)
    @check_tool(tool=RobotTools.LASER_TOOL)
    @validate_arguments
    def teach_puck(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """ """

        # RobotTrajTeachPuckCmd
        raise NotImplementedError

    @raise_ex
    @wait_for_path(path=RobotPaths.TEACH_DEWAR)
    @check_tool(tool=RobotTools.LASER_TOOL)
    @validate_arguments
    def teach_dewar(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """ """

        # RobotTrajTeachDewarCmd
        raise NotImplementedError

    @raise_ex
    @wait_for_path(path=RobotPaths.TEACH_PLATE_HOLDER)
    @check_tool(tool=RobotTools.LASER_TOOL)
    @validate_arguments
    def teach_plate_holder(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """ """

        # RobotTrajTeachPlateHolderCmd
        raise NotImplementedError

    @raise_ex
    @check_tool(tool=RobotTools.LASER_TOOL)
    @validate_arguments
    def teach_hotpuck(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """ """

        # RobotTrajTeachHotPuckCmd
        raise NotImplementedError

    @raise_ex
    @wait_for_path(path=RobotPaths.SOAK)
    @validate_arguments
    def soak(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Chilling of the gripper (only for grippers with process
        requiring drying and soaking phases).

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self.send_cmd(cmd=RobotTrajSoakToolCmd, args=[tool])

    @raise_ex
    @wait_for_path(path=RobotPaths.DRY)
    @validate_arguments
    def dry(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Dry the gripper.

        /!\\ Do not dry a gripper already in warm conditions /!\\

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self.send_cmd(cmd=RobotTrajDryToolCmd, args=[tool])

    @raise_ex
    @wait_for_path(path=RobotPaths.CHANGE_TOOL)
    @validate_arguments
    def change_tool(self, tool: Annotated[Tool, RobotTools]) -> TrajectoryResponse:
        """Launch automatic tool change, the robot will put its current tool
        on the parking and pick the one given in argument.

        Parameters
        ----------
        tool : Tool
            Tool to be changed to.

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(cmd=RobotTrajChangeToolCmd, args=[tool])

    @raise_ex
    @wait_for_path(path=RobotPaths.TOOL_CAL)
    @validate_arguments
    def calibrate_tool(self, tool: Annotated[Tool, RobotTools]) -> TrajectoryResponse:
        """Start gripper or laser tool calibration until the precision
        criterion is reached.

        Parameters
        ----------
        tool : Tool
            Tool to be calibrated.

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(cmd=RobotTrajCalibrateToolCmd, args=[tool])
