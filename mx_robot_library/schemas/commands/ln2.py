from pydantic import Field

from .base import BaseCmdModel, CmdEnum, CmdField


class RobotLN2Cmds(CmdEnum):
    """Robot LN2 Commands"""

    LN2_REG_ON = CmdField(
        title="LN2 Level Regulation On",
        description="Start LN2 level regulation in Dewar.",
        value="regulon",
    )
    LN2_REG_OFF = CmdField(
        title="LN2 Level Regulation Off",
        description="Stop LN2 level regulation in Dewar.",
        value="reguloff",
    )
    PS_REG_ON = CmdField(
        title="Phase Separator Regulation On",
        description="Activate phase separator standalone regulation.",
        value="ps_regulon",
    )
    PS_REG_OFF = CmdField(
        title="Phase Separator Regulation Off",
        description="Deactivate phase separator standalone regulation.",
        value="ps_reguloff",
    )


class RobotLN2Cmd(BaseCmdModel):
    """Robot LN2 Command Model"""

    cmd: RobotLN2Cmds = Field(
        title="Command",
    )
