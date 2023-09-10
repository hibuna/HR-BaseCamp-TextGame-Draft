import enum
from typing import Iterable, Optional, Union


def overlap(a: Iterable, b: Iterable) -> list:
    """Returns a list of elements that are in both iterables."""
    return [element for element in a if element in b]


def casefold_index(iterable: Iterable, value: str) -> Optional[int]:
    """Returns the index of the casefolded value in the iterable."""
    indices = (
        index
        for index, element in enumerate(iterable)
        if element.casefold() == value.casefold()
    )
    return next(indices, None)


def casefold_equals(a: str, b: str) -> bool:
    return a.casefold() == b.casefold()


def casefold_in(s: str, iterable: Iterable):
    for x in iterable:
        if isinstance(x, str):
            if s.casefold() == x.casefold():
                return True
    return False


def enum_get(a: str, enum_: enum.EnumType):
    try:
        return getattr(enum_, a.upper())
    except AttributeError:
        return None


def enum_has(a: str, enum_: enum.EnumType):
    return enum_get(a, enum_) is not None


def subclass_in_list(a: Union[object, type], b: list):
    if not isinstance(a, type):
        a = type(a)
    return any(a is x or issubclass(a, x) for x in b)
