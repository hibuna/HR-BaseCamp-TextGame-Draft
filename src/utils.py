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


def die_in_void(opening_door=False, inside=False):
    str_ = ""
    if opening_door:
        str_ += "You open the door and it flies open. "
    if inside:
        str_ += (
            "In an instant, you fly out the room and disappear into the insatiable nothingness. "
        )
    str_ += (
        "No training could have prepared you for these forces. "
        "A thousand glistening eyes merrily welcome you into the void. "
        "Your hear two loud pops accompanied by a sharp pain in your ears. "
        "Your lungs collapse. You are frozen in a state of windedness. "
        "In your last moments, you feel your innards clawing to escape the confines of your skin. "
        "Your vision distorts as your eyes swell to the size of tennis balls while you "
        "desperately try to keep them inside of your skull. "
        "Pop. Pop. You try to scream but you are stuck in your eternal gasp. "
        "You pray for mercy to whatever god, that He may allow you to asphyxiate before you explode. "
        "But you are an astronaut, a scientist. "
        "Your kind has killed God a long time ago. "
        "Your fibers tear apart and violently, yet silently, your body ruptures. "
        "Nothing remains of you but a chunky mist of blood and gore. "
        "You somewhat resemble a partially digested spaghetti bolognese."
        '"Where is your God now?" the void whispers as you transcend. '
        "Turns out your only true God was the Flying Spaghetti Monster."
    )
    print(str_)
    exit(0)
