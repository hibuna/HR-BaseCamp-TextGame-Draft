import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.enums import EquipableSlot
    from src.effect import Effect
    from src.environment import Environment
    from src.object.base import Equipable, Item


class Player:
    """
    The player is the main character of the game.

    Attributes:
    -----------
    name : str
        The name of the player.
    environment : Environment
        The environment that the player is currently in.
    effects : list[Effect]
        A list of effects that the player is currently under.
    inventory : list[Item]
        A list of items that the player is carrying.
    equipped : list[Equipable]
        A list of items that the player has equipped.
    """

    name: str = "player"
    environment: "Environment"

    def __init__(
        self,
        environment: "Environment" = None,
        effects: list["Effect"] = None,
        inventory: list["Item"] = None,
        equipped: list["Equipable"] = None,
    ):
        self.environment = environment
        self.effects = effects or []
        self.inventory = inventory or []
        self.equipped = equipped or []

    def _get_equipped(self, slot: "EquipableSlot") -> Optional["Equipable"]:
        """Returns the equipped item in the given slot."""
        return next(iter([item for item in self.equipped if item.slot is slot]), None)

    def equip(self, item: "Equipable") -> str:
        """Equips the given item."""
        logging.debug(f"Equipping item: {item}")

        if item in self.equipped:
            return f"Already equipped: {item}."

        if self._get_equipped(item.slot):
            return f"You already have something equipped: {item.slot}"

        self.equipped.append(item)
        logging.debug(f"Equipment: {self.equipped}")

        effects = self.add_effects(item.effects)

        return f"Equipped: {item}. {effects}".strip()

    def add_effects(self, effects: list["Effect"]) -> str:
        """Adds the given effects to the player."""
        effects = sorted(set(effects), key=lambda x: x.name)
        logging.debug(f"Adding effects: {effects}")

        self.effects.extend(
            [effect for effect in effects if effect not in self.effects]
        )

        logging.debug(f"Effects: {self.effects}")

        if effects:
            effects_str = ", ".join([effect.name.upper() for effect in effects])
            return f"You gain the following effects: {effects_str}."

        return ""

    def unequip(self, item: "Equipable") -> str:
        """Unequips the given item."""
        logging.debug(f"Unequipping item: {item}")

        if item not in self.equipped:
            return f"You don't have that equipped: {item}"

        self.equipped.remove(item)
        logging.debug(f"Equipment: {self.equipped}")

        effects = self.remove_effects(item.effects)

        return f"Unequipped: {item}. {effects}".strip()

    def remove_effects(self, effects: list["Effect"]) -> str:
        """Removes the given effects from the player."""
        effects = sorted(set(effects), key=lambda x: x.name)
        logging.debug(f"Removing effects: {effects}")

        self.effects = [effect for effect in self.effects if effect not in effects]
        logging.debug(f"Effects: {self.effects}")

        if effects:
            effects_str = ", ".join([effect.name.upper() for effect in effects])
            return f"You lose the following effects: {effects_str}."

        return ""
