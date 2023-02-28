from typing import TYPE_CHECKING, Union

from cachetools import TTLCache, cached

from mx_robot_library.schemas.commands.status import RobotStatusCmd, RobotStatusCmds
from mx_robot_library.schemas.responses.plc import PLCInputsResponse, PLCOutputsResponse
from mx_robot_library.schemas.responses.sample_data import SampleDataResponse
from mx_robot_library.schemas.responses.state import StateResponse

if TYPE_CHECKING:
    from .client import Client


class Status:
    """Robot Status"""

    def __init__(self, client: "Client") -> None:
        self._client = client
        self._port = self._client._status_port
        self._raw_state: Union[bytes, None] = None
        self._raw_plc_inputs: Union[bytes, None] = None
        self._raw_plc_outputs: Union[bytes, None] = None
        self._raw_sample_data: Union[bytes, None] = None

    def _send_cmd(self, cmd: RobotStatusCmds) -> bytes:
        """Send a status command to the robot and receive reply.

        Parameters
        ----------
        cmd : RobotStatusCmds
            Command to send to the robot.

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """

        return self._client._send_cmd(
            cmd=RobotStatusCmd(cmd=cmd).cmd_fmt,
            port=self._port,
        )

    @property
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def state(self) -> StateResponse:
        """Read robot state.

        NOTE: State object is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        StateResponse
            Parsed robot state model instance.
        """

        self._raw_state = self._send_cmd(cmd=RobotStatusCmds.GET_ASC_STATE)
        return StateResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_ASC_STATE,
            obj=self._raw_state,
        )

    @property
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def plc_inputs(self) -> PLCInputsResponse:
        """Read PLC inputs.

        NOTE: Output is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        PLCInputsResponse
            Parsed robot PLC Inputs model instance.
        """

        self._raw_plc_inputs = self._send_cmd(cmd=RobotStatusCmds.GET_PLC_INPUTS)
        return PLCInputsResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_PLC_INPUTS,
            obj=self._raw_plc_inputs,
        )

    @property
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def plc_outputs(self) -> PLCOutputsResponse:
        """Read PLC outputs.

        NOTE: Output is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        PLCOutputsResponse
            Parsed robot PLC Outputs model instance.
        """

        self._raw_plc_outputs = self._send_cmd(cmd=RobotStatusCmds.GET_PLC_OUTPUTS)
        return PLCOutputsResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_PLC_OUTPUTS,
            obj=self._raw_plc_outputs,
        )

    @property
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def sample_data(self) -> SampleDataResponse:
        """Read sample data.

        NOTE: Output is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        SampleDataResponse
            Parsed robot Sample Data model instance.
        """

        self._raw_sample_data = self._send_cmd(cmd=RobotStatusCmds.GET_SAMPLE_DATA)
        return SampleDataResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_SAMPLE_DATA,
            obj=self._raw_sample_data,
        )

    def get_loaded_pucks(self):
        """ """

        # Read populated puck positions from PLC outputs 56(1)->84(29)
        # _puck_positions = self.plc_outputs[56:85]
        # self.sample_data

        raise NotImplementedError
