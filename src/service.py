from typing import TYPE_CHECKING, Generic, TypeVar

from src.enums import PlayerAction
from src.object.base import Object, Item, Equipable
from src.object.objects import (
    HeavyDoor,
    PrologueControlPanel,
    PrologueControlPanelButton,
    HeavyDoorWheel,
)


if TYPE_CHECKING:
    from src.player import Player
    from src.containers import Effects, Items, Objects, Environments
    from src.command import Command


T = TypeVar("T", bound=Object)


class Service(Generic[T]):
    """
    Generic service class for interacting with objects. Separates the responsibility
    of interaction with an object from the object itself.

    Attributes:
    -----------
    object_type : type
        The type of object that this service interacts with.
    _player : Player
        The player.
    _effects_c : Effects
        The effects container.
    _items_c : Items
        The items container.
    _objects_c : Objects
        The objects container.
    _environments_c : Environments
        The environments container.
    _action_mapping : dict[PlayerAction, function]
        A mapping of actions to functions that perform the action.
    """

    object_type: T = type(None)

    def __init__(
        self,
        player: "Player",
        effects_c: "Effects",
        items_c: "Items",
        objects_c: "Objects",
        environments_c: "Environments",
    ):
        self._player = player
        self._effects_c = effects_c
        self._items_c = items_c
        self._objects_c = objects_c
        self._environments_c = environments_c

        self._action_mapping = {
            PlayerAction.EQUIP: self._equip,
            PlayerAction.UNEQUIP: self._unequip,
            PlayerAction.PICKUP: self._pickup,
            PlayerAction.FILL: self._fill,
            PlayerAction.EMPTY: self._empty,
            PlayerAction.INSPECT: self._inspect,
            PlayerAction.ENTER: self._enter,
            PlayerAction.USE: self._use,
            PlayerAction.HIT: self._hit,
            PlayerAction.TURN: self._turn,
            PlayerAction.PRESS: self._press,
            PlayerAction.OPEN: self._open,
        }

    def interact(self, cmd: "Command") -> str:
        """Interact with an object with dynamically using the action and preposition
        object."""
        action_method = self._action_mapping.get(cmd.action)
        if action_method is None:
            raise ValueError(f"Action '{cmd.action_str.upper()}' is not recognized")
        return action_method(cmd)  # noqa

    def _pickup(self, cmd: "Command") -> str:
        """Default pickup method. Can be overridden by subclasses."""
        return "You can't pick that up."

    def _fill(self, cmd: "Command") -> str:
        """Default fill method. Can be overridden by subclasses."""
        return "You can't fill that."

    def _empty(self, cmd: "Command") -> str:
        """Default empty method. Can be overridden by subclasses."""
        return "You can't empty that."

    def _inspect(self, cmd: "Command") -> str:
        """Default inspect method. Can be overridden by subclasses."""
        object_ = cmd.object or self._player.environment
        return object_.description

    def _enter(self, cmd: "Command") -> str:
        """Default enter method. Can be overridden by subclasses."""
        return "You can't enter that."

    def _equip(self, cmd: "Command") -> str:
        """Default equip method. Can be overridden by subclasses."""
        return "You can't equip that."

    def _unequip(self, cmd: "Command") -> str:
        """Default unequip method. Can be overridden by subclasses."""
        return "You can't unequip that."

    def _use(self, cmd: "Command") -> str:
        """Default use method. Can be overridden by subclasses."""
        return "You can't use that."

    def _hit(self, cmd: "Command") -> str:
        """Default hit method. Can be overridden by subclasses."""
        return f"You hit {cmd.object}. Nothing happens."

    def _turn(self, cmd: "Command") -> str:
        """Default turn method. Can be overridden by subclasses."""
        return "You can't turn that."

    def _press(self, cmd: "Command") -> str:
        """Default press method. Can be overridden by subclasses."""
        return "You can't press that."

    def _open(self, cmd: "Command") -> str:
        """Default open method. Can be overridden by subclasses."""
        return "You can't open that."


class ItemService(Service[Item]):
    object_type = Item

    def _pickup(self, cmd: "Command") -> str:
        """Generic item pickup method."""
        if not issubclass(type(cmd.object), Item):
            return "You can't pick that up."

        if PlayerAction.PICKUP not in cmd.object.interactions:
            return "You can't pick that up."

        self._player.environment.items.remove(cmd.object)
        self._player.inventory.append(cmd.object)

        return f"Picked up: {cmd.object.name.upper()}"

    def _equip(self, cmd: "Command") -> str:
        """Generic item equip method."""
        if cmd.object not in self._player.inventory:
            return "You don't have that."

        if not issubclass(type(cmd.object), Equipable):
            return "You can't equip that."

        if PlayerAction.EQUIP not in cmd.object.interactions:
            return "You can't equip that."

        return self._player.equip(cmd.object)  # noqa

    def _unequip(self, cmd: "Command") -> str:
        """Generic item unequip method.""" ""
        if cmd.object not in self._player.equipped:
            return f"You don't have that equipped: {cmd.object.name.upper()}"

        return self._player.unequip(cmd.object)  # noqa


class PrologueControlPanelService(Service[PrologueControlPanel]):
    object_type = PrologueControlPanel


class PrologueControlPanelButtonService(Service[PrologueControlPanelButton]):
    object_type = PrologueControlPanelButton

    def _press(self, cmd: "Command") -> str:
        self._player.environment = self._environments_c.cockpit()
        return "A vent opens and you hear a hissing sound. You start feeling woozy and pass out."

    def _use(self, cmd: "Command"):
        return self._press(cmd)

    def _hit(self, cmd: "Command"):
        return self._press(cmd)


class HeavyDoorService(Service[HeavyDoor]):
    object_type = HeavyDoor

    def _inspect(self, cmd: "Command"):
        wheel = self._objects_c.heavy_door_wheel()
        direction = "left" if wheel.state is wheel.States.OPEN else "right"
        return (
            f"A heavy door with a wheel on it. The wheel is turned to the {direction}."
        )

    def _open(self, cmd: "Command"):
        wheel = self._objects_c.heavy_door_wheel()
        if wheel.state is wheel.States.CLOSED:
            return "The door is locked."
        if wheel.state is wheel.States.OPEN:
            print(
                "You open the door and it flies open. You are sucked into the void. In your last moments, you feel the pressure escaping your body. Your eyes pop and your head explodes. You are dead."
            )
            exit(0)


class HeavyDoorWheelService(Service[HeavyDoorWheel]):
    object_type = HeavyDoorWheel

    def _turn(self, cmd: "Command"):
        wheel = self._objects_c.heavy_door_wheel()
        if wheel.state is wheel.States.OPEN:
            wheel.state = wheel.States.CLOSED
        if wheel.state is wheel.States.CLOSED:
            wheel.state = wheel.States.OPEN
        return "You turn the wheel."
