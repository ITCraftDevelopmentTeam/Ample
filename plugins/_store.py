import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, TypeVar, Generic, Optional, Iterable, Protocol


_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)


class SupportsKeysAndGetItem(Protocol[_KT, _VT_co]):
    def keys(self) -> Iterable[_KT]: ...
    def __getitem__(self, __key: _KT) -> _VT_co: ...


def load_json(
    path: Path | str,
    default_factory: Callable[[], _VT_co] = dict
) -> _VT_co:
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


class Json(defaultdict, Generic[_KT, _VT_co]):
    def __init__(
        self,
        path: Path | str,
        default_factory: Callable[[], _VT_co] = int
    ) -> None:
        self.path = Path("data") / path
        data = load_json(self.path)
        assert isinstance(data, dict)
        super().__init__(default_factory, data)

    def __setitem__(self, __key: _KT, __value: _VT_co) -> None:
        super().__setitem__(__key, __value)
        self.save()

    def __delitem__(self, __key: _KT) -> None:
        super().__delitem__(__key)
        self.save()

    def update(self, __m: Optional[
            SupportsKeysAndGetItem[_KT, _VT_co]
            | Iterable[tuple[_KT, _VT_co]]
    ] = None, **kwargs: _VT_co) -> None:
        if __m is None:
            super().update(**kwargs)
        else:
            super().update(__m, **kwargs)
        self.save()

    def pop(self, __key: _KT) -> _VT_co:
        value = super().pop(__key)
        self.save()
        return value

    def save(self) -> None:
        dump_json(self, self.path)
