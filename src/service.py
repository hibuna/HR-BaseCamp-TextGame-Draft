from typing import TYPE_CHECKING, Generic, TypeVar

from src.enums import PlayerAction
from src.object.base import Object, Item, Equipable
from src.object.objects import Well, River
from src.object.items import Bucket
from src.command import switch_command_objects


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
        }

    def interact(self, cmd: "Command") -> str:
        """Interact with an object with dynamically using the action and preposition
        object."""
        action_method = self._action_mapping.get(cmd.action)
        if action_method is None:
            raise ValueError(f"Action '{cmd.action_str}' is not recognized")
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

        return f"You pick up '{cmd.object}'."

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
        if not issubclass(type(cmd.object), Equipable):
            return "You can't unequip that."

        return self._player.unequip(cmd.object)  # noqa


class WellService(Service[Well]):
    object_type = Well

    def _fill(self, cmd: "Command") -> str:
        cmd.object: Well  # noqa

        if not isinstance(cmd.preposition_object, type(self._items_c.bucket())):
            return f"You can't fill the well with '{cmd.preposition_object}'."
        cmd.preposition_object: "Bucket"  # noqa

        if cmd.preposition_object not in self._player.inventory:
            return "You don't have that."

        if cmd.preposition_object in self._player.equipped:
            return "You can't fill the well with something you have equipped."

        if cmd.preposition_object.state is cmd.preposition_object.States.EMPTY:
            return "The bucket is empty."

        if cmd.preposition_object.state is not cmd.preposition_object.States.WATER:
            return "You don't think filling the well with that is a good idea."

        if cmd.object.state is self.object_type.States.FULL:
            return "The well is already full."

        cmd.object.fills_until_full -= 1
        cmd.preposition_object.state = cmd.preposition_object.States.EMPTY

        if cmd.object.fills_until_full == 0:
            cmd.object.state = self.object_type.States.FULL
            return "The well is full of water."

        return "You fill the well with water."

    def _inspect(self, cmd: "Command") -> str:
        cmd.object: Well  # noqa

        str_ = cmd.object.description
        if cmd.object.state is cmd.object.States.FULL:
            str_ += " The well is full of water."
        elif cmd.object.fills_until_full:
            str_ += " The well has some water in it."
        else:
            str_ += " The well is empty."

        return str_

    def _enter(self, cmd: "Command") -> str:
        if cmd.object.state is not self.object_type.States.FULL:
            return "Your body refuses to jump in without a way back up."

        if self._effects_c.water_breathing() in self._player.effects:
            cmd.object.items.remove(self._items_c.sword())
            self._player.inventory.append(self._items_c.sword())
            return (
                "You firmly grab the the bucket over your head and slowly descend into "
                "the water. When you are at the bottom, you use one hand to feel "
                "around. You swim back up and realise you are holding a sword."
            )

        return (
            "You jump in the well but can't find the glimmer before running out of "
            "breath."
        )


class RiverService(Service[River]):
    object_type = River

    def _fill_bucket(self, bucket: "Bucket") -> str:
        if bucket not in self._player.inventory:
            return "You don't have a bucket."

        if bucket in self._player.equipped:
            return "You can't fill something you have equipped."

        if bucket.state is not bucket.States.EMPTY:
            return "The bucket is already full."

        bucket.state = bucket.States.WATER

        return "You fill the bucket with water."

    def _fill(self, cmd: "Command") -> str:
        if isinstance(cmd.preposition_object, type(self._items_c.bucket())):
            return self._fill_bucket(cmd.preposition_object)  # noqa
        return f"You can't fill '{cmd.preposition_object}' in the river."


class BucketService(ItemService):
    object_type = Bucket

    def _fill_bucket(self, bucket: "Bucket") -> str:
        if bucket not in self._player.inventory:
            return "You don't have a bucket."

        if bucket in self._player.equipped:
            return "You can't fill something you have equipped."

        if bucket.state is not bucket.States.EMPTY:
            return "The bucket is already full."

        bucket.state = bucket.States.WATER

        return "You fill the bucket with water."

    def _fill(self, cmd: "Command") -> str:
        if isinstance(cmd.preposition_object, type(self._objects_c.river())):
            from src.containers import Services

            with switch_command_objects(cmd):
                return Services.river_service()._fill(cmd)

        return f"You can't fill '{cmd.preposition_object}' in the river."

    def _empty(self, cmd: "Command") -> str:
        cmd.object: Bucket  # noqa

        if cmd.preposition_object is not self._objects_c.well():
            return f"You can't empty '{cmd.preposition_object}' in the well."
        cmd.preposition_object: "Well"  # noqa

        from src.containers import Services

        with switch_command_objects(cmd):
            return Services.well_service()._fill(cmd)
