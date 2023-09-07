import enum
from typing import TYPE_CHECKING

from src.enums import PlayerAction
from src.object import Object

if TYPE_CHECKING:
    from src.effect import Effect
    from src.enums import EquipableSlot


class Item(Object):
    ...


class Equipable:
    slot: "EquipableSlot"
    effects: list["Effect"]

    def __init__(self, effects: list["Effect"] = None):
        self.effects = effects or []


class Weapon(Item, Equipable):
    damage: int


class Armor(Item, Equipable):
    defense: int


class Bucket(Armor):
    class States(enum.Enum):
        EMPTY = enum.auto()
        WATER = enum.auto()

    name = "bucket"
    description = "A bucket."
    slot = "head"
    defense = 10

    interactions = [
        PlayerAction.PICKUP,
        PlayerAction.FILL,
        PlayerAction.EMPTY,
        PlayerAction.EQUIP,
        PlayerAction.UNEQUIP
    ]
    state = States.EMPTY


class Sword(Weapon):
    name = "sword"
    description = "A sharp sword."
    slot = "hand"
    damage = 10

    interactions = [PlayerAction.EQUIP, PlayerAction.UNEQUIP]
    state = None
