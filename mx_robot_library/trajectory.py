from typing import TYPE_CHECKING, Union, Optional, Literal
from typing_extensions import Annotated
from pydantic import validate_arguments
from mx_robot_library.schemas.commands.trajectory import (
    BaseTrajectoryCmd, RobotTrajMoveHomeDirectCmd, RobotTrajMoveHomeSafeCmd,
    RobotTrajMountSampleCmd, RobotTrajUnmountSampleCmd, RobotTrajPrepickSampleCmd,
    RobotTrajUnmountAndMountSampleCmd, RobotTrajReadSampleCmd, RobotTrajMountPlateCmd,
    RobotTrajReturnSampleCmd, RobotTrajPickAndMoveSampleCmd, RobotTrajUnmountPlateCmd,
    RobotTrajPickAndMovePlateCmd, RobotTrajTeachGonioCmd, RobotTrajTeachPuckCmd,
    RobotTrajTeachDewarCmd, RobotTrajTeachPlateHolderCmd, RobotTrajSoakToolCmd,
    RobotTrajDryToolCmd, RobotTrajChangeToolCmd, RobotTrajCalibrateToolCmd,
)
from mx_robot_library.schemas.common.tool import RobotTools, Tool
from mx_robot_library.schemas.common.sample import Pin, Puck

if TYPE_CHECKING:
    from .client import Client


class Trajectory:
    """Robot Trajectory"""

    def __init__(self, client: "Client") -> None:
        self._client = client
        self._port = self._client._cmd_port

        # Hard coding these for now, seems to work.
        self._gonio_x_shift: int = 0
        self._gonio_y_shift: int = 0
        self._gonio_z_shift: int = 0

    def _send_cmd(self, cmd: type[BaseTrajectoryCmd], args: list = []) -> bytes:
        """Send a command to the robot and receive echo reply.

        Parameters
        ----------
        cmd : type[BaseTrajectoryCmd]
            Command to send to the robot.
        args : list, optional
            Command arguments, by default []

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        return self._client._send_cmd(
            cmd=cmd(args=args).cmd_fmt,
            port=self._port,
        )

    @validate_arguments
    def home(self, tool: Optional[Annotated[Tool, RobotTools]] = None) -> bytes:
        """Move the robot arm back to home position.

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(cmd=RobotTrajMoveHomeDirectCmd, args=[tool])

    @validate_arguments
    def recover(self, tool: Optional[Annotated[Tool, RobotTools]] = None) -> bytes:
        """Recover the robot arm back to home position.

        This command works different to the "home" trajectory, as the robot will move
        very slowly back to the home position in a safety mode.

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(cmd=RobotTrajMoveHomeSafeCmd, args=[tool])

    @validate_arguments
    def mount(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
        prepick_pin: Optional[Pin] = None,
        prepick_pin_detect: bool = True,
        data_matrix_scan: bool = False,
    ) -> bytes:
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
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        _prepick_pin: Union[Pin, Literal[0]] = 0
        _prepick_puck: Union[Puck, Literal[0]] = 0
        _prepick_pin_type: Union[Puck, Literal[0]] = 0
        if prepick_pin is not None:
            _prepick_pin = prepick_pin
            _prepick_puck = prepick_pin.puck
            _prepick_pin_type = prepick_pin.type

        return self._send_cmd(
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

    @validate_arguments
    def unmount(
        self,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        data_matrix_scan: bool = False,
    ) -> bytes:
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
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(RobotTrajUnmountSampleCmd, args=[
            tool,
            data_matrix_scan,
            self._gonio_x_shift,
            self._gonio_y_shift,
            self._gonio_z_shift,
        ])

    @validate_arguments
    def unmount_then_mount(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
        prepick_pin: Optional[Pin] = None,
        prepick_pin_detect: bool = True,
        data_matrix_scan: bool = False,
    ) -> bytes:
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
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        _prepick_pin: Union[Pin, Literal[0]] = 0
        _prepick_puck: Union[Puck, Literal[0]] = 0
        _prepick_pin_type: Union[Puck, Literal[0]] = 0
        if prepick_pin is not None:
            _prepick_pin = prepick_pin
            _prepick_puck = prepick_pin.puck
            _prepick_pin_type = prepick_pin.type

        return self._send_cmd(
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

    @validate_arguments
    def prepick(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
        data_matrix_scan: bool = False,
    ) -> bytes:
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
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(
            cmd=RobotTrajPrepickSampleCmd,
            args=[tool, pin.puck, pin, data_matrix_scan, pin.type, pin_detect],
        )

    @validate_arguments
    def read_datamatrix(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
    ) -> bytes:
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
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(
            cmd=RobotTrajReadSampleCmd,
            args=[tool, pin.puck, pin, pin.type, (not pin_detect)],
        )

    @validate_arguments
    def return_pin(self, tool: Optional[Annotated[Tool, RobotTools]] = None) -> bytes:
        """Put the sample in the gripper back in the Dewar to its memorized position
        (generally used after a “recover” path).

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(cmd=RobotTrajReturnSampleCmd, args=[tool])

    @validate_arguments
    def pick_and_move(
        self,
        pin: Pin,
        tool: Optional[Annotated[Tool, RobotTools]] = None,
        pin_detect: bool = True,
    ) -> bytes:
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
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(
            cmd=RobotTrajPickAndMoveSampleCmd,
            args=[tool, pin.puck, pin, pin.type, (not pin_detect)],
        )

    @validate_arguments
    def mount_plate(self) -> bytes:
        """ """

        # RobotTrajMountPlateCmd
        raise NotImplementedError

    @validate_arguments
    def unmount_plate(self) -> bytes:
        """ """

        # RobotTrajUnmountPlateCmd
        raise NotImplementedError

    @validate_arguments
    def pick_and_move_plate(self) -> bytes:
        """ """

        # RobotTrajPickAndMovePlateCmd
        raise NotImplementedError

    @validate_arguments
    def teach_goni(self) -> bytes:
        """ """

        # RobotTrajTeachGonioCmd
        raise NotImplementedError

    @validate_arguments
    def teach_puck(self) -> bytes:
        """ """

        # RobotTrajTeachPuckCmd
        raise NotImplementedError

    @validate_arguments
    def teach_dewar(self) -> bytes:
        """ """

        # RobotTrajTeachDewarCmd
        raise NotImplementedError

    @validate_arguments
    def teach_plate_holder(self) -> bytes:
        """ """

        # RobotTrajTeachPlateHolderCmd
        raise NotImplementedError

    @validate_arguments
    def soak(self, tool: Optional[Annotated[Tool, RobotTools]] = None) -> bytes:
        """Chilling of the gripper (only for grippers with process
        requiring drying and soaking phases).

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(cmd=RobotTrajSoakToolCmd, args=[tool])

    @validate_arguments
    def dry(self, tool: Optional[Annotated[Tool, RobotTools]] = None) -> bytes:
        """Dry the gripper.

        /!\\ Do not dry a gripper already in warm conditions /!\\

        Parameters
        ----------
        tool : Optional[Tool], optional
            Tool to call the operation with, by default None

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        if tool is None:
            tool = self._client.status.state.tool

        return self._send_cmd(cmd=RobotTrajDryToolCmd, args=[tool])

    @validate_arguments
    def change_tool(self, tool: Annotated[Tool, RobotTools]) -> bytes:
        """Launch automatic tool change, the robot will put its current tool
        on the parking and pick the one given in argument.

        Parameters
        ----------
        tool : Tool
            Tool to be changed to.

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        return self._send_cmd(cmd=RobotTrajChangeToolCmd, args=[tool])

    @validate_arguments
    def calibrate_tool(self, tool: Annotated[Tool, RobotTools]) -> bytes:
        """Start gripper or laser tool calibration until the precision
        criterion is reached.

        Parameters
        ----------
        tool : Tool
            Tool to be calibrated.

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        return self._send_cmd(cmd=RobotTrajCalibrateToolCmd, args=[tool])
