import enum
from typing import TYPE_CHECKING, Optional

from src.enums import PlayerAction

if TYPE_CHECKING:
    from src.item import Item


class Interactable:
    """
    Anything in the game universe that can be interacted with.

    Attributes:
    -----------
    name : str
        The name of the interactable.
    description : str
        The description of the interactable.
    interactions : dict[PlayerAction, str | dict]
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
    interactions: dict["PlayerAction", str | dict]
    state: Optional["States"]
    _references: Optional[list[str]]

    def __str__(self):
        return self.name

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


class Well(Object):
    class States(enum.Enum):
        EMPTY = enum.auto()
        FULL = enum.auto()

    name = "well"
    description = "A deep cobblestone well."
    interactions = [PlayerAction.FILL, PlayerAction.EMPTY, PlayerAction.ENTER]
    _references = ["water well"]
    items = None
    state = States.EMPTY

    fills_until_full = 3

    def __init__(self, items: list["Item"]):
        self.items = items


class River(Object):
    name = "river"
    description = "A river."
    interactions = [PlayerAction.FILL]
