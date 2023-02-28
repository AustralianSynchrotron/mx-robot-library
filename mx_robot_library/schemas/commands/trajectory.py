from collections import OrderedDict
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import (
    BaseModel, Field, conint, conlist, root_validator, validate_arguments, validator,
)
from mx_robot_library.config import get_settings

config = get_settings()


class TrajectorySubCmds(str, Enum):
    """Trajectory Sub Commands"""

    # Arm Return Commands
    MOVE_HOME_DIRECT = "home"
    MOVE_HOME_SAFE = "recover"

    # Sample Mount/Unmount/Move Commands
    MOUNT_AND_PREPICK_SAMPLE = "put"
    UNMOUNT_SAMPLE = "get"
    UNMOUNT_MOUNT_AND_PREPICK_SAMPLE = "getput"
    PREPICK_SAMPLE = "pick"
    READ_SAMPLE = "datamatrix"
    RETURN_SAMPLE = "back"
    PICK_AND_MOVE_SAMPLE = "gotodif"

    # Plate / Tray Commands
    MOUNT_PLATE = "putplate"
    UNMOUNT_PLATE = "getplate"
    PICK_AND_MOVE_PLATE = "platetodif"

    # Auto-Learn / Teaching Commands
    TEACH_GONIOMETER = "teachgonio"
    TEACH_PUCK = "teachpuck"
    TEACH_DEWAR = "teachdewar"
    TEACH_PLATE_HOLDER = "teachplateholder"

    # Tool Commands
    SOAK_TOOL = "soak"
    DRY_TOOL = "dry"
    CHANGE_TOOL = "changetool"
    CALIBRATE_TOOL = "toolcal"

    def __str__(self) -> str:
        return self.value


class BaseTrajectoryCmd(BaseModel):
    """Abstract Trajectory Command Model"""

    cmd: str = Field(title="Command", default="traj", const=True)
    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
    )
    full_args: Optional[
        conlist(
            item_type=int,
            min_items=1,
        )
    ] = Field(title="Full Arguments")
    args: conlist(
        item_type=int,
        min_items=1,
    ) = Field(title="Sub Arguments")
    cmd_fmt: Optional[str] = Field(
        title="Formatted Command",
        description="Formatted command to be passed via socket connection.",
        regex=r"^[^\(\)\s]*\r|^\S*\(.*\)\r",
    )

    class Config:
        validate_assignment: bool = True

    def __setattr__(self, name: str, value: Any) -> Any:
        res = super().__setattr__(name, value)

        # For "sub_cmd", "args", "full_args" fields
        # we'll trigger "cmd_fmt" to recompute.
        if name in ["sub_cmd", "args", "full_args"]:
            self.cmd_fmt = self.__class__.compute_cmd_fmt(
                v=self.cmd_fmt,
                values=self.dict(),
            )
        return res

    @root_validator(pre=True)
    def compute_full_args(cls, values: Dict[str, Any]):  # noqa: B902
        arg_vals = cls.get_named_args(values.get("args", []))
        args = list(arg_vals.values())
        if values.get("args") and any(args):
            values["full_args"] = cls.trim_args(args)
        else:
            values["full_args"] = args
        return values

    @validator("cmd_fmt", always=True)
    def compute_cmd_fmt(
        cls, v: Optional[str], values: Dict[str, Any]  # noqa: B902
    ) -> str:
        if values.get("cmd") and values.get("sub_cmd") and values.get("full_args"):
            cmd_args = [values["sub_cmd"], *values["full_args"]]
            v = f"{values['cmd']}({','.join([str(arg) for arg in cmd_args])})\r"
        return v

    @validator("full_args", always=True)
    def validate_full_args(
        cls, v: list[int], values: Dict[str, Any]  # noqa: B902
    ) -> list[int]:
        arg_vals = cls.get_named_args(v)
        if not arg_vals["tool_num"] >= 1:
            raise ValueError("Ensure tool number is greater than/equal to 1.")
        if arg_vals["puck_num"] and not (
            arg_vals["puck_num"] >= 1 and arg_vals["puck_num"] <= config.ASC_NUM_PUCKS
        ):
            raise ValueError(
                f"Ensure puck number is greater than/equal to 1 and less than/equal to {config.ASC_NUM_PUCKS}."  # noqa: E501,B950
            )
        smpl_num = arg_vals["sample_num"]
        if smpl_num and not (smpl_num >= 1 and smpl_num <= config.ASC_NUM_PINS):
            raise ValueError(
                f"Ensure sample number is greater than/equal to 1 and less than/equal to {config.ASC_NUM_PINS}."  # noqa: E501,B950
            )
        if not arg_vals["datamatrix_scan"] in (1, 0):
            raise ValueError(
                f"Datamatrix scan \"{arg_vals['datamatrix_scan']}\" not supported, valid options are (1 → On / 0 → Off)."  # noqa: E501,B950
            )
        n_puck_num = arg_vals["next_puck_num"]
        if n_puck_num and not (n_puck_num >= 0 and n_puck_num <= config.ASC_NUM_PUCKS):
            raise ValueError(
                f"Ensure next puck number is greater than/equal to 0 and less than/equal to {config.ASC_NUM_PUCKS}."  # noqa: E501,B950
            )
        n_smpl_nm = arg_vals["next_sample_num"]
        if n_smpl_nm and not (n_smpl_nm >= 0 and n_smpl_nm <= config.ASC_NUM_PINS):
            raise ValueError(
                f"Ensure next sample number is greater than/equal to 0 and less than/equal to {config.ASC_NUM_PINS}."  # noqa: E501,B950
            )
        if not arg_vals["sample_type"] in (1, 0):
            raise ValueError(
                f"Sample type \"{arg_vals['sample_type']}\" not supported, valid options are (1 → Hampton / 0 → Other)."  # noqa: E501,B950
            )
        if not arg_vals["next_sample_type"] in (1, 0):
            raise ValueError(
                f"Next sample type \"{arg_vals['next_sample_type']}\" not supported, valid options are (1 → Hampton / 0 → Other)."  # noqa: E501,B950
            )
        if not arg_vals["sample_detect_inhibit"] in (1, 0):
            raise ValueError(
                f"Sample detection inhibition \"{arg_vals['sample_detect_inhibit']}\" not supported, valid options are (1 → Detection disabled / 0 → Detection enabled)."  # noqa: E501,B950
            )
        if not arg_vals["next_sample_detect_inhibit"] in (1, 0):
            raise ValueError(
                f"Next sample detection inhibition \"{arg_vals['next_sample_detect_inhibit']}\" not supported, valid options are (1 → Detection disabled / 0 → Detection enabled)."  # noqa: E501,B950
            )
        return v

    @staticmethod
    @validate_arguments
    def get_named_args(args: list[int]) -> OrderedDict:
        """Generate an named dict of arguments from passed list.

        Parameters
        ----------
        args : list[int]
            List of unnamed arguments.

        Returns
        -------
        OrderedDict
            Dictionary of named arguments.
        """
        keys = (
            "tool_num",
            "puck_num",
            "sample_num",
            "datamatrix_scan",
            "next_puck_num",
            "next_sample_num",
            "sample_type",
            "next_sample_type",
            "sample_detect_inhibit",
            "next_sample_detect_inhibit",
            "goni_x",
            "goni_y",
            "goni_z",
        )
        arg_vals = OrderedDict.fromkeys(keys, 0)
        for index, val in enumerate(args):
            arg_vals[keys[index]] = val
        return arg_vals

    @staticmethod
    @validate_arguments
    def trim_args(args: list[int]) -> list[int]:
        """Chop any trailing "0" values off the end of the returned list,
        as they will default automatically.

        Parameters
        ----------
        args : list[int]
            List of argument values.

        Returns
        -------
        list[int]
            List of argument values with trailing "0" values removed.
        """
        last_arg_index = [i for i, val in enumerate(args) if val][-1]
        return args[: last_arg_index + 1]


class RobotTrajMoveHomeDirectCmd(BaseTrajectoryCmd):
    """Robot Trajectory Move Home Direct Command

    Move the robot arm back to home position.

    args : list[int]
        List containing a single integer to set tool to move home.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.MOVE_HOME_DIRECT,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajMoveHomeSafeCmd(BaseTrajectoryCmd):
    """Robot Trajectory Move Home Safe Command

    Move the robot arm back to home position.

    args : list[int]
        List containing a single integer to set tool to move home.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.MOVE_HOME_SAFE,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajMountSampleCmd(BaseTrajectoryCmd):
    """Robot Trajectory Mount And Prepick Sample Command

    Take a sample from the Dewar, eventually read its datamatrix
    and mount it on the goniometer.
    The sample needed for the next exchange can be then pre-picked.

    args : list[int]
        List containing thirteen integers to select sample to mounted
        and the sample to be prepicked.

        0: Tool Number
        1: Puck Number
        2: Sample Number
        3: DataMatrix Scan (1: Enabled, 0: Disabled)
        4: Next Puck Number (Set to "0" to skip prepick)
        5: Next Sample Number (Set to "0" to skip prepick)
        6: Sample Type (1: Hampton; 0: other caps)
        7: Next Sample Type (1: Hampton; 0: other caps)
        8: Sample Detection Inhibition (0: Detection enable, 1: detection disabled)
        9: Next Sample Detection Inhibition (0: Detection enable, 1: detection disabled)
        10: Gonio X Shift (µm)
        11: Gonio Y Shift (µm)
        12: Gonio Z Shift (µm)
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.MOUNT_AND_PREPICK_SAMPLE,
        const=True,
    )
    args: conlist(item_type=int, min_items=13, max_items=13,) = Field(
        title="Arguments",
    )


class RobotTrajUnmountSampleCmd(BaseTrajectoryCmd):
    """Robot Trajectory Unmount Sample Command

    Get the sample from the diffractometer, eventually read its datamatrix
    and put it back into the Dewar, in its memorized position.

    args : list[int]
        List containing five integers to select tool used to get the sample,
        whether to scan the sample data matrix and the goniometer offset.

        0: Tool Number
        1: DataMatrix Scan (1: Enabled, 0: Disabled)
        2: Gonio X Shift (µm)
        3: Gonio Y Shift (µm)
        4: Gonio Z Shift (µm)
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.UNMOUNT_SAMPLE,
        const=True,
    )
    args: conlist(item_type=int, min_items=5, max_items=5,) = Field(
        title="Arguments",
    )

    @root_validator(pre=True)
    def compute_full_args(cls, values: Dict[str, Any]):  # noqa: B902
        # Since our input arguments aren't in the correct position for the generated
        # command, we need to shift them into place.
        args = [0] * 13
        if len(values.get("args", [])) == 5:
            args[0], args[3], args[10], args[11], args[12] = values["args"]
        values["full_args"] = cls.trim_args(args)
        return values


class RobotTrajUnmountAndMountSampleCmd(BaseTrajectoryCmd):
    """Robot Trajectory Unmount, Mount And Prepick Sample Command

    Get the sample currently mounted on the goniometer,
    put it back into the Dewar and mount the specified sample
    on the goniometer eventually reading its datamatrix
    (no heating of the gripper between both operations).

    The sample needed for the next exchange can be then pre-picked
    (only available for double grippers with process requiring soaking phases).

    args : list[int]
        List containing thirteen integers to select sample to mounted
        and the sample to be prepicked.

        0: Tool Number
        1: Puck Number
        2: Sample Number
        3: DataMatrix Scan (1: Enabled, 0: Disabled)
        4: Next Puck Number (Set to "0" to skip prepick)
        5: Next Sample Number (Set to "0" to skip prepick)
        6: Sample Type (1: Hampton; 0: other caps)
        7: Next Sample Type (1: Hampton; 0: other caps)
        8: Sample Detection Inhibition (0: Detection enable, 1: detection disabled)
        9: Next Sample Detection Inhibition (0: Detection enable, 1: detection disabled)
        10: Gonio X Shift (µm)
        11: Gonio Y Shift (µm)
        12: Gonio Z Shift (µm)
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.UNMOUNT_MOUNT_AND_PREPICK_SAMPLE,
        const=True,
    )
    args: conlist(item_type=int, min_items=13, max_items=13,) = Field(
        title="Arguments",
    )


class RobotTrajPrepickSampleCmd(BaseTrajectoryCmd):
    """Robot Trajectory Prepick Sample Command

    Pick a sample for the next mounting, eventually read its
    datamatrix and go back to soaking position (only
    available for double grippers with process requiring
    soaking phases).

    args : list[int]
        List containing six integers to select sample to be prepicked.

        0: Tool Number
        1: Puck Number
        2: Sample Number
        3: DataMatrix Scan (1: Enabled, 0: Disabled)
        4: Sample Type (1: Hampton Crystal Cap or Crystal Cap Copper; 0: other caps)
        5: Sample Detection Inhibition (0: Detection enable, 1: detection disabled)
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.PREPICK_SAMPLE,
        const=True,
    )
    args: conlist(item_type=int, min_items=6, max_items=6,) = Field(
        title="Arguments",
    )

    @root_validator(pre=True)
    def compute_full_args(cls, values: Dict[str, Any]):  # noqa: B902
        # Since our input arguments aren't in the correct position for the generated
        # command, we need to shift them into place.
        args = [0] * 13
        if len(values.get("args", [])) == 6:
            args[0], args[1], args[2], args[3], args[6], args[8] = values["args"]
        if any(args):
            args = cls.trim_args(args)
        values["full_args"] = args
        return values


class RobotTrajReadSampleCmd(BaseTrajectoryCmd):
    """Robot Trajectory Read Sample Command

    Take a sample from the Dewar, read the datamatrix
    and put the sample back into the Dewar.

    args : list[int]
        List containing five integers to select sample to be read.

        0: Tool Number
        1: Puck Number
        2: Sample Number
        3: Sample Type (1: Hampton Crystal Cap or Crystal Cap Copper; 0: other caps)
        4: Sample Detection Inhibition (0: Detection enable, 1: detection disabled)
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.READ_SAMPLE,
        const=True,
    )
    args: conlist(item_type=int, min_items=5, max_items=5,) = Field(
        title="Arguments",
    )

    @root_validator(pre=True)
    def compute_full_args(cls, values: Dict[str, Any]):  # noqa: B902
        # Since our input arguments aren't in the correct position for the generated
        # command, we need to shift them into place.
        args = [0] * 13
        if len(values.get("args", [])) == 5:
            args[0], args[1], args[2], args[6], args[8] = values["args"]
        if any(args):
            args = cls.trim_args(args)
        values["full_args"] = args
        return values


class RobotTrajReturnSampleCmd(BaseTrajectoryCmd):
    """Robot Trajectory Return Sample Command

    Put the sample in the gripper back in the Dewar to its memorized position
    (generally used after a “recover” path).

    args : list[int]
        List containing a single integer to select
        the tool holding the sample to be returned.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.RETURN_SAMPLE,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajPickAndMoveSampleCmd(BaseTrajectoryCmd):
    """Robot Trajectory Pick And Move Sample Command

    Take a sample from the Dewar and move to the goniometer mounting position
    without releasing it (path to test goniometer position).

    args : list[int]
        List containing five integers to select sample to be picked and moved.

        0: Tool Number
        1: Puck Number
        2: Sample Number
        3: Sample Type (1: Hampton Crystal Cap or Crystal Cap Copper; 0: other caps)
        4: Sample Detection Inhibition (0: Detection enable, 1: detection disabled)
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.PICK_AND_MOVE_SAMPLE,
        const=True,
    )
    args: conlist(item_type=int, min_items=5, max_items=5,) = Field(
        title="Arguments",
    )

    @root_validator(pre=True)
    def compute_full_args(cls, values: Dict[str, Any]):  # noqa: B902
        # Since our input arguments aren't in the correct position for the generated
        # command, we need to shift them into place.
        args = [0] * 13
        if len(values.get("args", [])) == 5:
            args[0], args[1], args[2], args[6], args[8] = values["args"]
        if any(args):
            args = cls.trim_args(args)
        values["full_args"] = args
        return values


class RobotTrajMountPlateCmd(BaseTrajectoryCmd):
    """Robot Trajectory Mount Plate Command

    Take a plate from the hotel and put in onto the goniometer.

    args : list[int]
        List containing two integers to select the tool and desired plate to mount.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.MOUNT_PLATE,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=2, max_items=2,) = Field(
        title="Arguments",
    )


class RobotTrajUnmountPlateCmd(BaseTrajectoryCmd):
    """Robot Trajectory Unmount Plate Command

    Take the plate from the goniometer and put it back in the hotel.

    args : list[int]
        List containing a single integer to select the tool holding the plate.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.UNMOUNT_PLATE,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajPickAndMovePlateCmd(BaseTrajectoryCmd):
    """Robot Trajectory Pick And Move Plate Command

    Take a plate from the hotel and put in onto the goniometer.

    args : list[int]
        List containing two integers to select the tool and desired plate to pick.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.PICK_AND_MOVE_PLATE,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=2, max_items=2,) = Field(
        title="Arguments",
    )


class RobotTrajTeachGonioCmd(BaseTrajectoryCmd):
    """Robot Trajectory Teach Goniometer Command

    Launch automatic teaching of goniometer position (available only with laser tool).

    args : list[int]
        List containing a single integer to select the tool.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.TEACH_GONIOMETER,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajTeachPuckCmd(BaseTrajectoryCmd):
    """Robot Trajectory Teach Puck Command

    Launch automatic teaching of the puck given in argument
    (available only with laser tool).

    args : list[int]
        List containing two integers to select the tool and puck to teach.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.TEACH_PUCK,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=2, max_items=2,) = Field(
        title="Arguments",
    )


class RobotTrajTeachDewarCmd(BaseTrajectoryCmd):
    """Robot Trajectory Teach Dewar Command

    Launch automatic teaching of all puck positions inside the dewar,
    starting from the puck number specified (available only with laser tool).

    args : list[int]
        List containing two integers to select the tool and the starting puck.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.TEACH_DEWAR,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=2, max_items=2,) = Field(
        title="Arguments",
    )


class RobotTrajTeachPlateHolderCmd(BaseTrajectoryCmd):
    """Robot Trajectory Teach Plate Holder Command

    Launch automatic teaching of plates hotel.

    args : list[int]
        List containing a single integer to select the tool.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.TEACH_PLATE_HOLDER,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajSoakToolCmd(BaseTrajectoryCmd):
    """Robot Trajectory Soak Tool Command

    Chilling of the gripper (only for grippers with process
    requiring drying and soaking phases).

    args : list[int]
        List containing a single integer to select the tool.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.SOAK_TOOL,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajDryToolCmd(BaseTrajectoryCmd):
    """Robot Trajectory Dry Tool Command

    Dry the gripper.

    /!\\ Do not dry a gripper already in warm conditions /!\\

    args : list[int]
        List containing a single integer to select the tool.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.DRY_TOOL,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajChangeToolCmd(BaseTrajectoryCmd):
    """Robot Trajectory Change Tool Command

    Launch automatic tool change, the robot will put its current tool
    on the parking and pick the one given in argument.

    args : list[int]
        List containing a single integer to select the desired tool to switch out.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.CHANGE_TOOL,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )


class RobotTrajCalibrateToolCmd(BaseTrajectoryCmd):
    """Robot Trajectory Calibrate Tool Command

    Start gripper or laser tool calibration until the precision criterion is reached.

    args : list[int]
        List containing a single integer to select the desired tool calibrate.
    """

    sub_cmd: TrajectorySubCmds = Field(
        title="Sub Command",
        default=TrajectorySubCmds.CALIBRATE_TOOL,
        const=True,
    )
    args: conlist(item_type=conint(ge=1), min_items=1, max_items=1,) = Field(
        title="Arguments",
    )
