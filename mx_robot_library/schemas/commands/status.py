from pydantic import Field

from .base import BaseCmdModel, CmdEnum, CmdField


class RobotStatusCmds(CmdEnum):
    """Robot Status Commands"""

    GET_ASC_STATE = CmdField(
        title="Get ASC State",
        description="Ask for the sample changer status.",
        value="state",
    )
    GET_PLC_INPUTS = CmdField(
        title="Get PLC Inputs",
        description="Ask for the status of the PLC inputs.",
        value="di",
    )
    GET_PLC_OUTPUTS = CmdField(
        title="Get PLC Outputs",
        description="Ask for the status of the PLC outputs.",
        value="do",
    )
    GET_SAMPLE_DATA = CmdField(
        title="Get Sample Data",
        description="""Ask for sample data (time statistics given in s.,
        pucks position-DataMatrix mapping table, etc…).""",
        value="sampledata",
    )


class RobotStatusCmd(BaseCmdModel):
    """Robot Status Command Model"""

    cmd: RobotStatusCmds = Field(
        title="Command",
    )
