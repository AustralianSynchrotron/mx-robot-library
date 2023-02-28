from typing import Any, Union
from typing_extensions import Self
from types import MappingProxyType
from pydantic import BaseModel, Field


class BaseRobotItem(BaseModel):
    """Abstract Robot Item Model"""

    id: int = Field(title="ID")
    name: str = Field(title="Name")
    description: str = Field(title="Description")

    class Config:
        allow_mutation = False

    def __int__(self: Self) -> int:
        return self.id

    def __str__(self: Self) -> str:
        return self.name


class BaseRobotMeta(type):
    """Abstract Robot Meta"""

    def __init_subclass__(cls, item_cls: type[BaseRobotItem]) -> None:
        cls._item_cls = item_cls
        return super().__init_subclass__()

    def __new__(
        cls: type[Self],
        name: str,
        bases: tuple[type, ...],
        _dict: dict[str, Any],
    ) -> Self:
        cls.__items__: tuple[BaseRobotItem, ...] = tuple(sorted(
            [item for _, item in _dict.items() if isinstance(item, cls._item_cls)],
            key=lambda item: item.id,
        ))
        return type.__new__(cls, name, bases, _dict)

    def __getitem__(self: Self, item: Union[str, int]) -> BaseRobotItem:
        if isinstance(item, str):
            if item in self._item_by_name:
                return self._item_by_name[item]
            return getattr(self, item)
        elif isinstance(item, int):
            return self._item_by_id[item]

    def __len__(self: Self) -> int:
        return len(self.__items__)

    def __contains__(self: Self, item: Union[BaseRobotItem, str, int]) -> bool:
        if isinstance(item, str):
            if item in self._item_by_name:
                return True
            return hasattr(self, item) and isinstance(getattr(self, item), self._item_cls)
        elif isinstance(item, int):
            return item in self._item_by_id
        return item in self.__items__

    @property
    def _item_by_name(self: Self) -> MappingProxyType[str, BaseRobotItem]:
        """Fetch items mapped by name.

        Returns
        -------
        MappingProxyType[str, BaseRobotItem]
            Items mapped by name.
        """
        return MappingProxyType({item.name: item for item in self.__items__})

    @property
    def _item_by_id(self: Self) -> MappingProxyType[int, BaseRobotItem]:
        """Fetch items mapped by ID.

        Returns
        -------
        MappingProxyType[int, BaseRobotItem]
            Items mapped by ID.
        """
        return MappingProxyType({item.id: item for item in self.__items__})
