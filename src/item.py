import enum
from typing import TYPE_CHECKING

from src.enums import PlayerAction
from src.object import Object

if TYPE_CHECKING:
    from src.effect import Effect
    from src.enums import EquipableSlot


class Item(Object):
    """An object that can be picked up and put in the inventory."""
    pass


class Equipable(Item):
    """
    Can be equipped by the player.

    Attributes:
    -----------
    slot : EquipableSlot
        The slot that the item can be equipped in.
    effects : list[Effect]
        A list of effects that the item has on the player when equipped.
    """
    slot: "EquipableSlot"
    effects: list["Effect"]

    def __init__(self, effects: list["Effect"] = None):
        self.effects = effects or []


class Weapon(Equipable):
    damage: int


class Armor(Equipable):
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
