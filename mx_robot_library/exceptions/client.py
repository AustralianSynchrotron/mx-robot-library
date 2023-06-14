from .base import RobotException


class Readonly(RobotException):
    """Connection is readonly.

    Trajectory commands will be rejected.
    """


class ClientReadonly(Readonly):
    """Client is restricted to readonly mode."""
