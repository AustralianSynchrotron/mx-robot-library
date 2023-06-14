from typing import Any, Annotated, Optional, TYPE_CHECKING
from time import sleep, time
from functools import wraps
from inspect import signature, BoundArguments
from collections import OrderedDict
from pydantic import validate_arguments
from pydantic.typing import AnyCallable

from .schemas.common.tool import RobotTools, Tool
from .schemas.common.path import RobotPaths, Path
from .schemas.responses.base import BaseResponse
from .schemas.responses.trajectory import TrajectoryResponse
from .exceptions.commands.trajectory import ChangeToolError, ToolAlreadyEquiped
from .exceptions.commands.common import SystemFault
from .logger import get_logger
from .client.base import RootClient, BaseClient, SubClient

if TYPE_CHECKING:
    from .client import Client

logger = get_logger()


def _get_bound_args(func: AnyCallable, *args, **kwargs) -> OrderedDict[str, Any]:
    """Get bound method arguments.

    Parameters
    ----------
    func : AnyCallable
        Method to be wrapped.

    Returns
    -------
    OrderedDict[str, Any]
        Bound arguments.
    """
    # Get callable signature
    _func_sig = signature(func)

    try:
        # Bind positional and named args to signature applying defaults
        _bound_args: BoundArguments = _func_sig.bind(*args, **kwargs)
        _bound_args.apply_defaults()
        return _bound_args.arguments
    except TypeError:
        return OrderedDict()


@validate_arguments
def inject_client(
    func: Optional[AnyCallable] = None,
    *,
    client: Optional[RootClient] = None,
):
    """Inject tool into wrapped method args.

    Parameters
    ----------
    func : Optional[AnyCallable], optional
        Method to be wrapped, by default None.
    client : Optional[RootClient], optional
        Client instance to inject into wrapped method, by default None.

    Returns
    -------
    Any
        Result of wrapped method call.
    """

    def _inject_client(_func: AnyCallable) -> AnyCallable:

        @wraps(_func)
        def wrapper_function(
            *args,
            client: Optional[RootClient] = client,
            **kwargs,
        ):
            _func_args = _get_bound_args(_func, *args, **kwargs)

            # Default client from call arguments
            if client is None and isinstance(_func_args.get("self"), BaseClient):
                _client: BaseClient = _func_args["self"]
                if isinstance(_client, SubClient):
                    # Pickup root client from sub-client
                    _client = _client._client
                client = _client

            if client is not None:
                from .client import Client
                if isinstance(client, RootClient):
                    # Upgrade root client to full client instance
                    client = Client(
                        host=client.host,
                        status_port=client.status_port,
                        cmd_port=client.cmd_port,
                        readonly=client.readonly,
                    )
                elif not isinstance(client, Client):
                    client = None

            return _func(*args, client=client, **kwargs)

        return wrapper_function

    if func is not None:
        return _inject_client(func)
    return _inject_client


@validate_arguments
def inject_tool(
    func: Optional[AnyCallable] = None,
    *,
    tool: Optional[Annotated[Tool, RobotTools]] = None,
):
    """Inject tool into wrapped method args.

    Parameters
    ----------
    func : Optional[AnyCallable], optional
        Method to be wrapped, by default None.
    tool : Optional[Annotated[Tool, RobotTools]], optional
        Tool to inject into wrapped method, by default None.

    Returns
    -------
    Any
        Result of wrapped method call.
    """

    def _inject_tool(_func: AnyCallable) -> AnyCallable:

        @wraps(_func)
        def wrapper_function(
            *args,
            tool: Optional[Annotated[Tool, RobotTools]] = tool,
            **kwargs,
        ):

            if tool is not None and not isinstance(tool, Tool):
                # Try to convert tool value to instance of Tool
                try:
                    tool = Tool.validate(value=tool)
                except Exception:
                    pass

            return _func(*args, tool=tool, **kwargs)

        return wrapper_function

    if func is not None:
        return _inject_tool(func)
    return _inject_tool


@validate_arguments
def check_tool(
    func: Optional[AnyCallable] = None,
    *,
    tool: Optional[Annotated[Tool, RobotTools]] = None,
    client: Optional[RootClient] = None,
    on_error: bool = False,
):
    """Check tool currently mounted on the robot arm and trigger the robot
    to change tool automatically if the wrong tool is mounted.

    Parameters
    ----------
    func : Optional[AnyCallable], optional
        Method to be wrapped, by default None.
    tool : Optional[Annotated[Tool, RobotTools]], optional
        Tool required to execute wrapped method, by default None.
    client : Optional[RootClient], optional
        Instance of the robot client, by default None.
    on_error : bool, optional
        Whether automatic toolchange should occur before the decorated method is called
        or after a "ChangeToolError" is raised, by default False.

    Returns
    -------
    Any
        Result of wrapped method call.
    """

    def _check_tool(_func: AnyCallable) -> AnyCallable:

        @inject_tool(tool=tool)
        @inject_client(client=client)
        @wraps(_func)
        def wrapper_function(
            *args,
            client: Optional["Client"] = None,
            tool: Optional[Annotated[Tool, RobotTools]] = None,
            on_error: bool = on_error,
            **kwargs,
        ):
            def _change_tool(client: "Client", tool: Annotated[Tool, RobotTools]):
                logger.debug(f"Auto-changing tool to {tool.name}...")
                try:
                    _res: TrajectoryResponse = client.trajectory.change_tool(
                        tool=tool,
                    )
                    if isinstance(_res.error, ToolAlreadyEquiped):
                        raise _res.error
                except ToolAlreadyEquiped as ex:
                    # Tool is already equiped
                    logger.debug("Auto tool change failed, tool already equipped.")

            if not on_error and client is not None and tool is not None:
                # Check if correct tool is mounted
                _mounted_tool = client.status.state.tool
                if _mounted_tool != tool:
                    # Toolchange required
                    _change_tool(client, tool)

            try:
                # Call method
                res: TrajectoryResponse = _func(*args, tool=tool, **kwargs)
            except ChangeToolError as ex:
                if not on_error:
                    raise ex

                if client is not None and tool is not None:
                    # Check if correct tool is mounted
                    _mounted_tool = client.status.state.tool
                    if _mounted_tool != tool:
                        # Toolchange required
                        _change_tool(client, tool)

                    # Call method
                    res: TrajectoryResponse = _func(*args, tool=tool, **kwargs)

            return res

        return wrapper_function

    if func is not None:
        return _check_tool(func)
    return _check_tool


@validate_arguments
def raise_ex(
    func: Optional[AnyCallable] = None,
    *,
    client: Optional[RootClient] = None,
):
    """Raise unresolved PLC errors returned in response.

    Parameters
    ----------
    func : Optional[AnyCallable], optional
        Method to be wrapped, by default None.
    client : Optional[RootClient], optional
        Instance of the robot client, by default None.

    Returns
    -------
    Any
        Result of wrapped method call.

    Raises
    ------
    PLCError
        Robot PLC Error.
    """

    def _raise_ex(_func: AnyCallable) -> AnyCallable:

        @inject_client(client=client)
        @wraps(_func)
        def wrapper_function(
            *args,
            client: Optional["Client"] = None,
            **kwargs,
        ):

            # Call method
            res = _func(*args, **kwargs)

            # Pickup unresolved PLC error
            if isinstance(res, BaseResponse) and res.error is not None:
                if isinstance(res.error, SystemFault):
                    # TODO: Raise detailed PLC error message from status
                    pass
                raise res.error

            return res

        return wrapper_function

    if func is not None:
        return _raise_ex(func)
    return _raise_ex


@validate_arguments
def wait_for_path(
    func: Optional[AnyCallable] = None,
    *,
    path: Annotated[Path, RobotPaths],
    end_path: Annotated[Path, RobotPaths] = RobotPaths.UNDEFINED,
    always: bool = False,
    timeout: float = 120.0,
    client: Optional[RootClient] = None,
):
    """ """

    def _wait_for_path(
        _func: AnyCallable,
        path: Annotated[Path, RobotPaths] = path,
        end_path: Annotated[Path, RobotPaths] = end_path,
        always: bool = always,
        timeout: float = timeout,
    ) -> AnyCallable:

        @inject_client(client=client)
        @wraps(_func)
        def wrapper_function(
            *args,
            client: Optional["Client"] = None,
            wait: bool = False,
            **kwargs,
        ):

            # Call method
            res = _func(*args, **kwargs)

            if client is not None and always or wait:
                if isinstance(res, BaseResponse) and res.error is None:
                    # TODO: Find a better way to do this, maybe using AsyncIO futures.
                    max_time = time() + timeout
                    # Wait for robot to start running the path
                    while client.status.state.path != path:
                        if time() >= max_time:
                            break
                        sleep(0.5)

                    # Wait for robot to finish running the path
                    while client.status.state.path != end_path:
                        if time() >= max_time:
                            break
                        sleep(0.5)

            return res

        return wrapper_function

    if func is not None:
        return _wait_for_path(func)
    return _wait_for_path