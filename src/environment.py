from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.item import Item
    from src.object import Object


class Environment:
    """
    An environment is a place in the game universe that contains objects and items.

    Attributes:
    -----------
    objects : list[Object]
        A list of objects in the environment.
    items : list[Item]
        A list of items in the environment.
    """
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

