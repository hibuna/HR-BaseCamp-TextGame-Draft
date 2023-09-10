import enum
from typing import TYPE_CHECKING

from src.object.base import Object
from src.enums import PlayerAction

if TYPE_CHECKING:
    from src.object.base import Item


class Well(Object):
    class States(enum.Enum):
        EMPTY = enum.auto()
        FULL = enum.auto()

    name = "well"
    description = "A deep cobblestone well."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.FILL,
        PlayerAction.EMPTY,
        PlayerAction.ENTER,
    ]
    _references = ["water well"]
    items = None
    state = States.EMPTY

    fills_until_full = 3

    def __init__(self, items: list["Item"]):
        self.items = items


class River(Object):
    name = "river"
    description = "A river."
    interactions = [PlayerAction.INSPECT, PlayerAction.FILL]
    _references = []
