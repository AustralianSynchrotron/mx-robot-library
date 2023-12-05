import re
from typing import TYPE_CHECKING, Any, Generator, Mapping, Optional, Union, overload

from pydantic import validate_arguments
from typing_extensions import Self, TypeVar

from .client.base import CmdChannel, SubClient
from .config import get_settings
from .schemas.common.sample import Puck

if TYPE_CHECKING:
    from _collections_abc import dict_items, dict_keys, dict_values

PIN_POSITION_PATTERN = re.compile(r"^(.*)\[(\d+)\]$")
PUCK_POSITION_PATTERN = re.compile(r"^puck_(\d+)$")

config = get_settings()
T = TypeVar("T")


class Dewar(Mapping, SubClient, channel=CmdChannel.STATUS):
    """Robot Dewar"""

    @validate_arguments
    def __getitem__(self, key: Union[Puck, int, str]) -> Union[Puck, None]:
        _status = self._client.status

        if isinstance(key, Puck):
            # Refresh puck metadata for puck object instance
            key = key.id

        if isinstance(key, int):
            _idx = key - 1

            if key < 1:
                raise KeyError(
                    f"Key {key!r} is outside lower bounds for positional puck ID."
                )
            if key > config.ASC_NUM_PUCKS:
                raise KeyError(
                    f"Key {key!r} is outside upper bounds for positional puck ID."
                )

            if not _status.plc_outputs.puck_presense[_idx]:
                # Puck not present in dewar
                return None
            if len(_status.sample_data.puck_matrix[_idx]):
                # Puck present and datamatrix (barcode) has been recorded
                return Puck(
                    id=key,
                    name=_status.sample_data.puck_matrix[_idx],
                )
            # Puck present in dewar
            return Puck(id=key)

        _pin_position = PIN_POSITION_PATTERN.search(key)
        if _pin_position:
            # Strip references to pin position in puck, we just want the puck name
            key = _pin_position.groups(default=key)[0]

        _puck_position = PUCK_POSITION_PATTERN.search(key)
        if _puck_position:
            # Key matches default puck name pattern.
            # Strip out the puck positional ID and call "__getitem__" again.
            return self.__getitem__(_puck_position.groups()[-1])

        if key in _status.sample_data.puck_matrix:
            # Puck datamatrix (barcode) has been recorded by the puck loading assistant
            for _idx, _puck_name in enumerate(_status.sample_data.puck_matrix):
                # Duplicates may exist, use first entry that reports present in dewer
                if _puck_name == key and _status.plc_outputs.puck_presense[_idx]:
                    return Puck(id=_idx + 1, name=key)

        raise KeyError(
            f"Key {key!r} does not appear to reference any puck currently "
            "loaded in the dewar."
        )

    def __iter__(self: Self) -> Generator[int, Any, None]:
        for _idx in range(1, config.ASC_NUM_PUCKS + 1):
            yield _idx

    def __len__(self: Self) -> int:
        return config.ASC_NUM_PUCKS

    @property
    def pucks(self: Self) -> tuple[Union[Puck, None], ...]:
        """Get pucks in the robot dewar.

        Positionally safe, empty positions are returned as None to preserve padding.

        Returns
        -------
        tuple[Union[Puck, None], ...]
            Tuple of puck objects or None where the position in the dewar is empty.
        """
        return tuple(
            Puck(id=str(_idx), name=_name) if _populated else None
            for _idx, (_populated, _name) in enumerate(
                zip(  # noqa: B905
                    self._client.status.plc_outputs.puck_presense,
                    self._client.status.sample_data.puck_matrix,
                ),
                start=1,
            )
        )

    @property
    def loaded_pucks(self: Self) -> tuple[Puck, ...]:
        """Get pucks currently loaded in the robot dewar.

        Similar to the `pucks` property, but filters results to include only populated
        puck positions.

        Returns
        -------
        tuple[Puck, ...]
            Tuple of puck opjects currently loaded in the dewar.
        """
        return tuple(_puck for _puck in self.pucks if _puck is not None)

    if TYPE_CHECKING:

        @overload
        def get(self: Self, key: Union[Puck, int, str]) -> Union[Puck, None]:
            ...

        @overload
        def get(self: Self, key: Union[Puck, int, str], default: T) -> Union[Puck, T]:
            ...

        def get(
            self: Self,
            key: Union[Puck, int, str],
            default: Optional[Any] = None,
        ) -> Union[Puck, None]:
            raise NotImplementedError

        def keys(self: Self) -> "dict_keys[int, Union[Puck, None]]":
            raise NotImplementedError

        def items(self: Self) -> "dict_items[int, Union[Puck, None]]":
            raise NotImplementedError

        def values(self: Self) -> "dict_values[int, Union[Puck, None]]":
            raise NotImplementedError
