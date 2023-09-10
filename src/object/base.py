from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from src.enums import PlayerAction, EquipableSlot
    from src.effect import Effect


class Interactable:
    """
    Anything in the game universe that can be interacted with.

    Attributes:
    -----------
    name : str
        The name of the interactable.
    description : str
        The description of the interactable.
    interactions : dict[PlayerAction, Union[str, dict]]
        A list of interactions that the player can perform on the interactable.
    state : Optional[enum.Enum]
        The current state of the interactable.
    _references : Optional[list[str]]
        A list of names that can be used to reference the interactable.
        Accessed via the `references` property. Defaults to the interactable's name.
    """
    class States:
        pass

    name: str
    description: str
    interactions: dict["PlayerAction", Union[str, dict]]
    state: Optional[States]
    _references: Optional[list[str]]

    def __str__(self):
        return f"<{self.name}>"

    @property
    def references(self):
        """Returns a list of names that can be used to reference the interactable."""
        try:
            return (self._references or []) + [self.name]
        except AttributeError:
            return [self.name]


class Object(Interactable):
    """
    Objects are interactable things in the game universe that may hold items.

    Attributes:
    -----------
    items : Optional[list[Item]]
        A list of items that the object contains.
    """
    items: Optional[list["Item"]]


class Item(Interactable):
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
