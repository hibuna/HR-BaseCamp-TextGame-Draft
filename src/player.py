from typing import TYPE_CHECKING

from src.enums import EquipableSlot

if TYPE_CHECKING:
    from src.item import Item, Equipable
    from src.effect import Effect
    from src.environment import Environment


class Player:
    name: str = "player"
    level: int = 1
    strength: int = 1
    dexterity: int = 1
    intelligence: int = 1
    health: int = 100
    max_health: int = 100
    environment: "Environment"

    effects: list["Effect"]
    inventory: list["Item"]
    equipped: list["Equipable"]

    def __init__(
            self,
            effects: list["Effect"] = None,
            inventory: list["Item"] = None,
            equipped: list["Equipable"] = None,
    ):
        self.effects = effects or []
        self.inventory = inventory or []
        self.equipped = equipped or []

    def _get_equipped(self, slot: EquipableSlot):
        return next(iter([item for item in self.equipped if item.slot is slot]), None)

    @property
    def equipped_head(self):
        return self._get_equipped(EquipableSlot.head)

    @property
    def equipped_body(self):
        return self._get_equipped(EquipableSlot.body)

    @property
    def equipped_legs(self):
        return self._get_equipped(EquipableSlot.legs)

    @property
    def equipped_feet(self):
        return self._get_equipped(EquipableSlot.feet)

    @property
    def equipped_hand(self):
        return self._get_equipped(EquipableSlot.hand)

    @property
    def equipped_offhand(self):
        return self._get_equipped(EquipableSlot.offhand)

    @property
    def equipped_neck(self):
        return self._get_equipped(EquipableSlot.neck)

    @property
    def equipped_finger(self):
        return self._get_equipped(EquipableSlot.finger)
