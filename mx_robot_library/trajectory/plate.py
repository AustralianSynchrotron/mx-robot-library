from typing import Optional

from pydantic import validate_arguments
from typing_extensions import Annotated

from mx_robot_library.schemas.commands.trajectory import (
    RobotTrajMountPlateCmd,
    RobotTrajPickAndMovePlateCmd,
    RobotTrajUnmountPlateCmd,
)
from ..schemas.responses.trajectory import TrajectoryResponse
from ..schemas.common.sample import Plate
from ..schemas.common.tool import RobotTools, Tool
from ..schemas.common.path import RobotPaths
from ..client.base import CmdChannel
from ..decorators import check_tool, raise_ex, wait_for_path
from .base import SubTrajectory


class PlateTraj(SubTrajectory, channel=CmdChannel.CMD):
    """Robot Plate Trajectory"""

    @raise_ex
    @wait_for_path(path=RobotPaths.PUT_PLATE)
    @check_tool(tool=RobotTools.PLATE_GRIPPER)
    @validate_arguments
    def mount(
        self,
        plate: Plate,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Take a plate from the hotel and put in onto the goniometer.

        Parameters
        ----------
        plate : Plate
            Target plate.
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(
            cmd=RobotTrajMountPlateCmd,
            args=[tool, plate],
        )

    @raise_ex
    @wait_for_path(path=RobotPaths.GET_PLATE)
    @check_tool(tool=RobotTools.PLATE_GRIPPER)
    @validate_arguments
    def unmount(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Take the plate from the goniometer and put it back in the hotel.

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(
            cmd=RobotTrajUnmountPlateCmd,
            args=[tool],
        )

    @raise_ex
    @check_tool(tool=RobotTools.PLATE_GRIPPER, on_error=True)
    @validate_arguments
    def unmount_then_mount(
        self,
        plate: Plate,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Get the plate currently mounted on the goniometer,
        put it back in the hotel and mount the specified plate
        on the goniometer.

        Parameters
        ----------
        plate : Plate
            Target plate.
        tool : Optional[Annotated[Tool, RobotTools]], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        # Unmount plate
        self.unmount(tool=tool, wait=True)

        # Mount plate
        return self.mount(plate=plate, tool=tool, wait=True)

    @raise_ex
    @wait_for_path(path=RobotPaths.PLATE_TO_DIF)
    @check_tool(tool=RobotTools.PLATE_GRIPPER)
    @validate_arguments
    def pick_and_move(
        self,
        plate: Plate,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Take a plate from the hotel and move to the goniometer mounting position
        without releasing it (path to test goniometer position).

        Parameters
        ----------
        plate : Plate
            Target plate.
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(
            cmd=RobotTrajPickAndMovePlateCmd,
            args=[tool, plate],
        )
