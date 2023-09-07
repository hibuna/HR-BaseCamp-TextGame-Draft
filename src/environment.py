from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.item import Item
    from src.object import Object
    from src.enums import PlayerAction


class Interactable:
    name: str
    description: str
    interactions: dict["PlayerAction", str | dict]
    _references: list[str]

    @property
    def references(self):
        try:
            return (self._references or []) + [self.name]
        except AttributeError:
            return [self.name]


class Environment:
    name: str
    description: str

    def __init__(self, objects: list[type["Object"]], items: list[type["Item"]] = None):
        self.objects = objects
        self.items = items or []


class TownSquare(Environment):
    name = "Town Square"

    @property
    def description(self):
        str_ = "You are in the town square. "
        if self.objects:
            str_ += (f"You see these objects: "
                     f"{', '.join([obj.name for obj in self.objects])}. ")
        if self.items:
            str_ += (f"You see these items: "
                     f"{', '.join([item.name for item in self.items])}. ")
        return str_.strip()

