import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, TypeVar, Generic, Optional, Iterable, Protocol


_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class SupportsKeysAndGetItem(Protocol[_KT, _VT]):
    def keys(self) -> Iterable[_KT]: ...
    def __getitem__(self, __key: _KT) -> _VT: ...


def load_json(
    path: Path | str,
    default_factory: Callable[[], _VT] = dict
) -> _VT:
    if not path.exists():
        data = default_factory()
        dump_json(data, path)
        return data
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def dump_json(obj: Any, path: Path | str) -> None:
    if not (parent := path.parent).exists():
        parent.mkdir()
    with open(path, "w", encoding="utf-8") as file:
        json.dump(obj, file, ensure_ascii=False, indent=2, sort_keys=True)


class Json(defaultdict[_KT, _VT], Generic[_KT, _VT]):
    def __init__(
        self,
        path: Path | str,
        default_factory: Callable[[], _VT] = int
    ) -> None:
        self.path = Path("data") / path
        data = load_json(self.path)
        assert isinstance(data, dict)
        super().__init__(default_factory, data)

    def __setitem__(self, __key: _KT, __value: _VT) -> None:
        super().__setitem__(__key, __value)
        self.save()

    def __delitem__(self, __key: _KT) -> None:
        super().__delitem__(__key)
        self.save()

    def __del__(self) -> None:
        try:
            self.save()
        except NameError:
            pass

    def update(self, __m: Optional[
            SupportsKeysAndGetItem[_KT, _VT]
            | Iterable[tuple[_KT, _VT]]
    ] = None, **kwargs: _VT) -> None:
        if __m is None:
            super().update(**kwargs)
        else:
            super().update(__m, **kwargs)
        self.save()

    def pop(self, __key: _KT) -> _VT:
        value = super().pop(__key)
        self.save()
        return value

    def save(self) -> None:
        dump_json(self, self.path)
