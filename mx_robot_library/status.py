from typing import Union

from cachetools import TTLCache, cached

from .client.base import CmdChannel, RootClient, SubClient
from .decorators import raise_ex
from .schemas.commands.status import RobotStatusCmd, RobotStatusCmds
from .schemas.responses.plc import PLCInputsResponse, PLCOutputsResponse
from .schemas.responses.sample_data import SampleDataResponse
from .schemas.responses.state import StateResponse
from .schemas.common.sample import Puck


class Status(SubClient, channel=CmdChannel.STATUS):
    """Robot Status"""

    def __init__(self, client: RootClient) -> None:
        """
        Parameters
        ----------
        client : RootClient
            Root client.
        """
        super().__init__(client=client)
        self._raw_state: Union[bytes, None] = None
        self._raw_plc_inputs: Union[bytes, None] = None
        self._raw_plc_outputs: Union[bytes, None] = None
        self._raw_sample_data: Union[bytes, None] = None

    def send_cmd(self, cmd: RobotStatusCmds) -> bytes:
        """Send a command to the robot, then receive it's response.

        Parameters
        ----------
        cmd : RobotStatusCmds
            Command to send to the robot.

        Returns
        -------
        bytes
            Reply to be decoded from robot.
        """
        return super().send_cmd(cmd=RobotStatusCmd(cmd=cmd).cmd_fmt)

    @property
    @raise_ex
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def state(self, *args, **kwargs) -> StateResponse:
        """Read robot state.

        NOTE: State object is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        StateResponse
            Parsed robot state model instance.
        """

        self._raw_state = self.send_cmd(cmd=RobotStatusCmds.GET_ASC_STATE)
        return StateResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_ASC_STATE,
            obj=self._raw_state,
        )

    @property
    @raise_ex
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def plc_inputs(self, *args, **kwargs) -> PLCInputsResponse:
        """Read PLC inputs.

        NOTE: Output is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        PLCInputsResponse
            Parsed robot PLC Inputs model instance.
        """

        self._raw_plc_inputs = self.send_cmd(cmd=RobotStatusCmds.GET_PLC_INPUTS)
        return PLCInputsResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_PLC_INPUTS,
            obj=self._raw_plc_inputs,
        )

    @property
    @raise_ex
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def plc_outputs(self, *args, **kwargs) -> PLCOutputsResponse:
        """Read PLC outputs.

        NOTE: Output is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        PLCOutputsResponse
            Parsed robot PLC Outputs model instance.
        """

        self._raw_plc_outputs = self.send_cmd(cmd=RobotStatusCmds.GET_PLC_OUTPUTS)
        return PLCOutputsResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_PLC_OUTPUTS,
            obj=self._raw_plc_outputs,
        )

    @property
    @raise_ex
    @cached(cache=TTLCache(maxsize=1, ttl=0.05))
    def sample_data(self, *args, **kwargs) -> SampleDataResponse:
        """Read sample data.

        NOTE: Output is cached for 50ms to avoid spamming the robot controller.

        Returns
        -------
        SampleDataResponse
            Parsed robot Sample Data model instance.
        """

        self._raw_sample_data = self.send_cmd(cmd=RobotStatusCmds.GET_SAMPLE_DATA)
        return SampleDataResponse.parse_cmd_output(
            cmd=RobotStatusCmds.GET_SAMPLE_DATA,
            obj=self._raw_sample_data,
        )

    def get_loaded_pucks(self, *args, **kwargs) -> tuple[Puck, ...]:
        """Get pucks currently loaded in the dewar.

        Pucks are detected using presence information pulled from the robot PLC.

        If datamatrix (barcode) information is present in the sample data,
        this will be passed to the output puck instance `name` property,
        otherwise the puck name will be generated based on the pucks positon
        in the dewar, e.g. from the `id` attribute.

        Returns
        -------
        tuple[Puck, ...]
            Currently loaded pucks.
        """
        return tuple(
            Puck(id=str(_idx), name=_name)
            for _idx, (_populated, _name) in enumerate(
                zip(
                    self.plc_outputs.puck_presense,
                    self.sample_data.puck_matrix,
                ),
                start=1,
            )
            if _populated
        )
