from types import MappingProxyType
from typing import Any, Union

from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Self


class BaseRobotItem(BaseModel):
    """Abstract Robot Item Model"""

    id: int = Field(title="ID")
    name: str = Field(title="Name")
    description: str = Field(title="Description")

    model_config = ConfigDict(frozen=True)

    def __int__(self: Self) -> int:
        return self.id

    def __str__(self: Self) -> str:
        return self.name


class BaseRobotMeta(type):
    """Abstract Robot Meta"""

    def __init_subclass__(metacls, item_cls: type[BaseRobotItem]) -> None:
        metacls._item_cls = item_cls
        return super().__init_subclass__()

    def __new__(
        metacls: type[Self],
        name: str,
        bases: tuple[type, ...],
        _dict: dict[str, Any],
    ) -> Self:
        metacls.__items__: tuple[BaseRobotItem, ...] = tuple(
            sorted(
                [
                    item
                    for _, item in _dict.items()
                    if isinstance(item, metacls._item_cls)
                ],
                key=lambda item: item.id,
            )
        )
        return type.__new__(metacls, name, bases, _dict)

    def __getitem__(cls, item: Union[str, int]) -> BaseRobotItem:
        if isinstance(item, str):
            if item in cls._item_by_name:
                return cls._item_by_name[item]
            return getattr(cls, item)
        elif isinstance(item, int):
            return cls._item_by_id[item]

    def __len__(cls) -> int:
        return len(cls.__items__)

    def __contains__(cls, item: Union[BaseRobotItem, str, int]) -> bool:
        if isinstance(item, str):
            if item in cls._item_by_name:
                return True
            return hasattr(cls, item) and isinstance(getattr(cls, item), cls._item_cls)
        elif isinstance(item, int):
            return item in cls._item_by_id
        return item in cls.__items__

    @property
    def _item_by_name(cls) -> MappingProxyType[str, BaseRobotItem]:
        """Fetch items mapped by name.

        Returns
        -------
        MappingProxyType[str, BaseRobotItem]
            Items mapped by name.
        """
        return MappingProxyType({item.name: item for item in cls.__items__})

    @property
    def _item_by_id(cls) -> MappingProxyType[int, BaseRobotItem]:
        """Fetch items mapped by ID.

        Returns
        -------
        MappingProxyType[int, BaseRobotItem]
            Items mapped by ID.
        """
        return MappingProxyType({item.id: item for item in cls.__items__})
