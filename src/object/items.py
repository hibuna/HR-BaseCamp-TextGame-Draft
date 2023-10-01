from src.enums import PlayerAction, EquipableSlot
from src.object.base import Armor, Item, Weapon


class SpaceSuit(Armor):
    name = "space suit"
    description = "A space suit."
    slot = EquipableSlot.BODY

    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.PICKUP,
        PlayerAction.EQUIP,
        PlayerAction.UNEQUIP,
    ]


class FireAxe(Weapon):
    name = "fire axe"
    description = "A fire axe."
    slot = EquipableSlot.HAND

    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.PICKUP,
        PlayerAction.EQUIP,
        PlayerAction.UNEQUIP,
    ]
    _references = ["fire axe", "axe"]


class RepairKit(Item):
    name = "repair kit"
    description = "A repair kit. You wonder what it's for."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.PICKUP,
        PlayerAction.USE,
    ]
    _references = ["repair kit", "kit"]


class FuelCan(Item):
    name = "fuel can"
    description = "A fuel can."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.PICKUP,
        PlayerAction.USE,
        PlayerAction.EMPTY,
    ]
    _references = ["fuel can", "can", "fuel"]
