from typing import Union

from pydantic import validate_arguments

from .schemas.common.sample import Pin, PinType, Puck
from .client.base import SubClient, CmdChannel


class Utils(SubClient, channel=CmdChannel.CMD):
    """Robot Utils"""

    @validate_arguments
    def get_puck(self, id: int) -> Puck:
        """Get puck model instance from ID.

        Parameters
        ----------
        id : int
            Puck ID.

        Returns
        -------
        Puck
            New puck model instance.
        """

        return Puck(id=id)

    @validate_arguments
    def get_pin(
        self,
        id: int,
        puck: Union[Puck, int],
        type: PinType = PinType.OTHER,
    ) -> Pin:
        """Get pin model instance from ID.

        Parameters
        ----------
        id : int
            Pin ID.
        puck : Union[Puck, int]
            Puck model instance or ID.
        type : PinType, optional
            Pin type, by default PinType.OTHER

        Returns
        -------
        Pin
            New pin model instance.
        """

        if isinstance(puck, int):
            puck = self.get_puck(id=puck)

        return Pin(id=id, puck=puck, type=0)
