from __future__ import annotations
import inspect
import typing as t

_Item_t = t.TypeVar("_Item_t")


class IterSingleton(t.Generic[_Item_t]):

    _items: t.Set[_Item_t]
    __instance: t.Optional[IterSingleton] = None

    @staticmethod
    def _get_wrapper_new(
        older: t.Callable[[IterSingleton], IterSingleton],
    ) -> t.Callable[[IterSingleton], IterSingleton]:

        def wrapper(cls: IterSingleton) -> IterSingleton:
            older(cls)
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
            return cls.__instance

        return wrapper

    def __init_subclass__(cls) -> None:
        older_new = getattr(cls, "__new__")
        setattr(cls, "__new__", cls._get_wrapper_new(older_new))

        cls._items = {
            val for key, val in inspect.getmembers(cls)
            if not key.startswith("_")
        }

    def __iter__(self) -> t.Iterator[_Item_t]:
        return iter(self._items)

    def __contains__(self, item: _Item_t) -> bool:
        return item in self._items
