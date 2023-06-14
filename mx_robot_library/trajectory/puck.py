from typing import TYPE_CHECKING, Literal, Optional, Union

from pydantic import validate_arguments
from typing_extensions import Annotated

from ..client.base import CmdChannel
from ..decorators import check_tool, raise_ex, wait_for_path
from ..schemas.commands.trajectory import (
    RobotTrajMountSampleCmd,
    RobotTrajPickAndMoveSampleCmd,
    RobotTrajPrepickSampleCmd,
    RobotTrajReadSampleCmd,
    RobotTrajReturnSampleCmd,
    RobotTrajUnmountAndMountSampleCmd,
    RobotTrajUnmountSampleCmd,
)
from ..schemas.common.path import RobotPaths
from ..schemas.common.sample import Pin, Puck
from ..schemas.common.tool import RobotTools, Tool
from ..schemas.responses.trajectory import TrajectoryResponse
from .base import SubTrajectory

if TYPE_CHECKING:
    from .trajectory import Trajectory


class PuckTraj(SubTrajectory, channel=CmdChannel.CMD):
    """Robot Puck Trajectory"""

    def __init__(self, parent: "Trajectory") -> None:
        super().__init__(parent=parent)

        # Hard coding these for now, seems to work.
        self._gonio_x_shift: int = 0
        self._gonio_y_shift: int = 0
        self._gonio_z_shift: int = 0

    @raise_ex
    @wait_for_path(path=RobotPaths.PUT)
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
        """Take a sample from the Dewar, optionally read its datamatrix
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
            cmd=RobotTrajMountSampleCmd,
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
    @wait_for_path(path=RobotPaths.GET)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def unmount(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        data_matrix_scan: bool = False,
    ) -> TrajectoryResponse:
        """Get the sample from the diffractometer, optionally read its datamatrix
        and put it back into the Dewar, in its memorized position.

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
            RobotTrajUnmountSampleCmd,
            args=[
                tool,
                data_matrix_scan,
                self._gonio_x_shift,
                self._gonio_y_shift,
                self._gonio_z_shift,
            ],
        )

    @raise_ex
    @wait_for_path(path=RobotPaths.GET_PUT)
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
        put it back into the Dewar and mount the specified sample
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
            cmd=RobotTrajUnmountAndMountSampleCmd,
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
    @wait_for_path(path=RobotPaths.PICK)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def prepick(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
        data_matrix_scan: bool = False,
    ) -> TrajectoryResponse:
        """Pick a sample for the next mounting, optionally read its
        datamatrix and go back to soaking position (only
        available for double grippers with process requiring
        soaking phases).

        Parameters
        ----------
        pin : Pin
            Target pin.
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None
        pin_detect : bool, optional
            Pin detection, by default True
        data_matrix_scan : bool, optional
            Datamatrix scan, by default False

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(
            cmd=RobotTrajPrepickSampleCmd,
            args=[tool, pin.puck, pin, data_matrix_scan, pin.type, pin_detect],
        )

    @raise_ex
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def read_datamatrix(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
    ) -> TrajectoryResponse:
        """Take a sample from the Dewar, read the datamatrix
        and put the sample back into the Dewar.

        Parameters
        ----------
        pin : Pin
            Target pin.
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None
        pin_detect : bool, optional
            Pin detection, by default True

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(
            cmd=RobotTrajReadSampleCmd,
            args=[tool, pin.puck, pin, pin.type, (not pin_detect)],
        )

    @raise_ex
    @wait_for_path(path=RobotPaths.BACK)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def return_pin(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
    ) -> TrajectoryResponse:
        """Put the sample in the gripper back in the Dewar to its memorized position
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

        return self.send_cmd(cmd=RobotTrajReturnSampleCmd, args=[tool])

    @raise_ex
    @wait_for_path(path=RobotPaths.GOTO_DIF)
    @check_tool(tool=RobotTools.DOUBLE_GRIPPER)
    @validate_arguments
    def pick_and_move(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
    ) -> TrajectoryResponse:
        """Take a sample from the Dewar and move to the goniometer mounting position
        without releasing it (path to test goniometer position).

        Parameters
        ----------
        pin : Pin
            Target pin.
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None
        pin_detect : bool, optional
            Pin detection, by default True

        Returns
        -------
        TrajectoryResponse
            Decoded response from the robot.
        """

        return self.send_cmd(
            cmd=RobotTrajPickAndMoveSampleCmd,
            args=[tool, pin.puck, pin, pin.type, (not pin_detect)],
        )
