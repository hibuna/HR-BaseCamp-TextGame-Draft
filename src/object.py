import enum
from typing import TYPE_CHECKING

from src.environment import Interactable
from src.enums import PlayerAction

if TYPE_CHECKING:
    from src.item import Item


class Object(Interactable):
    class States:
        pass

    name: str
    description: str
    interactions: dict["PlayerAction", str | dict]
    _references: list[str]

    items: list["Item"]
    state: enum.Enum


class Well(Object):
    class States(enum.Enum):
        EMPTY = enum.auto()
        FULL = enum.auto()

    name = "well"
    description = "A deep cobblestone well."
    interactions = [PlayerAction.FILL, PlayerAction.EMPTY, PlayerAction.ENTER]
    _references = ["water well"]
    items = None
    state = States.FULL

    fills_until_full = 3

    def __init__(self, items: list["Item"]):
        self.items = items


class River(Object):
    name = "river"
    description = "A river."
    interactions = [PlayerAction.FILL]
