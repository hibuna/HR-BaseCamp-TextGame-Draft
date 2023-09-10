import enum

from src.enums import PlayerAction
from src.object.base import Armor, Weapon


class Bucket(Armor):
    class States(enum.Enum):
        EMPTY = enum.auto()
        WATER = enum.auto()

    name = "bucket"
    description = "A bucket."
    slot = "head"
    defense = 10

    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.PICKUP,
        PlayerAction.FILL,
        PlayerAction.EMPTY,
        PlayerAction.EQUIP,
        PlayerAction.UNEQUIP,
    ]
    state = States.EMPTY


class Sword(Weapon):
    name = "sword"
    description = "A sharp sword."
    slot = "hand"
    damage = 10

    interactions = [PlayerAction.INSPECT, PlayerAction.EQUIP, PlayerAction.UNEQUIP]
    state = None
