from typing import TYPE_CHECKING, Literal, Optional, Union

from pydantic import validate_arguments
from typing_extensions import Annotated

from ..client.base import CmdChannel
from ..decorators import check_tool, raise_ex, wait_for_path
from ..schemas.commands.trajectory import (
    RobotTrajHotPuckMountSampleCmd,
    RobotTrajHotPuckReturnSampleCmd,
    RobotTrajHotPuckUnmountAndMountSampleCmd,
    RobotTrajHotPuckUnmountSampleCmd,
)
from ..schemas.common.path import RobotPaths
from ..schemas.common.sample import Pin, Puck
from ..schemas.common.tool import RobotTools, Tool
from ..schemas.responses.trajectory import TrajectoryResponse
from .base import SubTrajectory

if TYPE_CHECKING:
    from .trajectory import Trajectory


class HotPuckTraj(SubTrajectory, channel=CmdChannel.CMD):
    """Robot Hot Puck Trajectory"""

    def __init__(self, parent: "Trajectory") -> None:
        super().__init__(parent=parent)

        # Hard coding these for now, seems to work.
        self._gonio_x_shift: int = 0
        self._gonio_y_shift: int = 0
        self._gonio_z_shift: int = 0

    @raise_ex
    @wait_for_path(path=RobotPaths.HOTPUCK_PUT)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def mount(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
        prepick_pin: Optional[Pin] = None,
        prepick_pin_detect: bool = True,
        data_matrix_scan: bool = False,
    ) -> TrajectoryResponse:
        """Take a sample from the hot puck, optionally read its datamatrix
        and mount it on the goniometer.
        The sample needed for the next exchange can then be pre-picked.

        Parameters
        ----------
        pin : Pin
            Target pin.
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None
        pin_detect : bool, optional
            Pin detection, by default True
        prepick_pin : Optional[Pin], optional
            Pre-pick pin, by default None
        prepick_pin_detect : bool, optional
            Pre-pick pin detection, by default True
        data_matrix_scan : bool, optional
            Datamatrix scan, by default False

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        _prepick_pin: Union[Pin, Literal[0]] = 0
        _prepick_puck: Union[Puck, Literal[0]] = 0
        _prepick_pin_type: Union[Puck, Literal[0]] = 0
        if prepick_pin is not None:
            _prepick_pin = prepick_pin
            _prepick_puck = prepick_pin.puck
            _prepick_pin_type = prepick_pin.type

        return self.send_cmd(
            cmd=RobotTrajHotPuckMountSampleCmd,
            args=[
                tool,
                pin.puck,
                pin,
                data_matrix_scan,
                _prepick_puck,
                _prepick_pin,
                pin.type,
                _prepick_pin_type,
                (not pin_detect),
                (not prepick_pin_detect),
                self._gonio_x_shift,
                self._gonio_y_shift,
                self._gonio_z_shift,
            ],
        )

    @raise_ex
    @wait_for_path(path=RobotPaths.HOTPUCK_GET)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def unmount(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        data_matrix_scan: bool = False,
    ) -> TrajectoryResponse:
        """Get the sample from the diffractometer, optionally read its datamatrix
        and put it back into the hot puck, in its memorized position.

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None
        data_matrix_scan : bool, optional
            Datamatrix scan, by default False

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(
            RobotTrajHotPuckUnmountSampleCmd,
            args=[
                tool,
                data_matrix_scan,
                self._gonio_x_shift,
                self._gonio_y_shift,
                self._gonio_z_shift,
            ],
        )

    @raise_ex
    @wait_for_path(path=RobotPaths.HOTPUCK_GET_PUT)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def unmount_then_mount(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
        prepick_pin: Optional[Pin] = None,
        prepick_pin_detect: bool = True,
        data_matrix_scan: bool = False,
    ) -> TrajectoryResponse:
        """Get the sample currently mounted on the goniometer,
        put it back into the hot puck and mount the specified sample
        on the goniometer optionally reading its datamatrix
        (no heating of the gripper between both operations).

        The sample needed for the next exchange can be then pre-picked
        (only available for double grippers with process requiring soaking phases).

        Parameters
        ----------
        pin : Pin
            Target pin.
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None
        pin_detect : bool, optional
            Pin detection, by default True
        prepick_pin : Optional[Pin], optional
            Pre-pick pin, by default None
        prepick_pin_detect : bool, optional
            Pre-pick pin detection, by default True
        data_matrix_scan : bool, optional
            Datamatrix scan, by default False

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        _prepick_pin: Union[Pin, Literal[0]] = 0
        _prepick_puck: Union[Puck, Literal[0]] = 0
        _prepick_pin_type: Union[Puck, Literal[0]] = 0
        if prepick_pin is not None:
            _prepick_pin = prepick_pin
            _prepick_puck = prepick_pin.puck
            _prepick_pin_type = prepick_pin.type

        return self.send_cmd(
            cmd=RobotTrajHotPuckUnmountAndMountSampleCmd,
            args=[
                tool,
                pin.puck,
                pin,
                data_matrix_scan,
                _prepick_puck,
                _prepick_pin,
                pin.type,
                _prepick_pin_type,
                (not pin_detect),
                (not prepick_pin_detect),
                self._gonio_x_shift,
                self._gonio_y_shift,
                self._gonio_z_shift,
            ],
        )

    @raise_ex
    @wait_for_path(path=RobotPaths.HOTPUCK_BACK)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def return_pin(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Put the sample in the gripper back in the hot puck to its memorized position
        (generally used after a “recover” path).

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(cmd=RobotTrajHotPuckReturnSampleCmd, args=[tool])
