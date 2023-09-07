import logging
from typing import Generic, TypeVar, TYPE_CHECKING

from src.enums import PlayerAction
from src.item import Item, Equipable
from src.object import Well, Object, River

if TYPE_CHECKING:
    from containers import Effects, Items, Objects, Environments
    from src.player import Player
    from src.item import Bucket


T = TypeVar('T', bound=Object)


class Service(Generic[T]):
    object_type: T = type(None)

    def __init__(self, player: "Player", effects_c: "Effects", items_c: "Items", objects_c: "Objects", environments_c: "Environments"):
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

    def interact(self, action: "PlayerAction", object_: "Object", preposition_object: "Object" = None):
        action = self._action_mapping.get(action)
        if action is None:
            raise ValueError(f"Object '{object_.name}' does not support action {action}")
        return action(object_, preposition_object)  # noqa

    def _pickup(self, object_: "Object", preposition_object: "Object" = None):
        return "You can't pick that up."

    def _fill(self, object_: "Object", preposition_object: "Object" = None):
        return "You can't fill that."

    def _empty(self, object_: "Object", preposition_object: "Object" = None):
        return "You can't empty that."

    def _inspect(self, object_: "Object", preposition_object: "Object" = None):
        object_ = object_ or self._player.environment
        return object_.description

    def _enter(self, object_: "Object", preposition_object: "Object" = None):
        return "You can't enter that."

    def _equip(self, object_: "Object", preposition_object: "Object" = None):
        return "You can't equip that."

    def _unequip(self, object_: "Object", preposition_object: "Object" = None):
        return "You can't unequip that."


class ItemService(Service[Item]):
    object_type = Item

    def _pickup(self, object_: "Item", preposition_object: "Object" = None):
        if not issubclass(type(object_), Item):
            return "You can't pick that up."
        if PlayerAction.PICKUP not in object_.interactions:
            return "You can't pick that up."
        self._player.environment.items.remove(object_)  # noqa
        self._player.inventory.append(object_)  # noqa
        return f"You pick up '{object_.name}'."

    def _equip(self, object_: "Item", preposition_object: "Object" = None):
        if object_ not in self._player.inventory:
            return "You don't have that."
        if not issubclass(type(object_), Equipable):
            return "You can't equip that."
        if PlayerAction.EQUIP not in object_.interactions:
            return "You can't equip that."
        if object_ in self._player.equipped:
            return "You already have that equipped."
        self._player.equipped.append(object_)
        logging.debug(f"Equipped: {self._player.equipped}")
        self._player.effects.extend(object_.effects or [])
        logging.debug(f"Effects: {self._player.effects}")
        return f"You equip '{object_.name}'."

    def _unequip(self, object_: "Item", preposition_object: "Object" = None):
        if object_ not in self._player.equipped:
            return "You don't have that equipped."
        self._player.equipped.remove(object_)
        logging.debug(f"Equipped: {self._player.equipped}")
        self._player.effects = [
            effect for effect in self._player.effects if effect not in object_.effects
        ]
        logging.debug(f"Effects: {self._player.effects}")
        return f"You unequip '{object_.name}'."


class WellService(Service[Well]):
    object_type = Well

    player: "Player"

    def _fill(self, object_: Well, preposition_object: "Object" = None):
        if not isinstance(preposition_object, type(self._items_c.bucket())):
            return f"You can't fill the well with '{preposition_object}'."
        if preposition_object not in self._player.inventory:
            return "You don't have that."
        if preposition_object in self._player.equipped:
            return "You can't fill the well with something you have equipped."
        if preposition_object.state is preposition_object.States.EMPTY:
            return "The bucket is empty."
        if preposition_object.state is not preposition_object.States.WATER:
            return "You don't think filling the well with that is a good idea."
        if object_.state is self.object_type.States.FULL:
            return "The well is already full."
        object_.fills_until_full -= 1
        if object_.fills_until_full == 0:
            object_.state = self.object_type.States.FULL
            return "The well is full of water."
        preposition_object.state = preposition_object.States.EMPTY
        return "You fill the well with water."

    def _empty(self, object_: Well, preposition_object: "Object" = None):
        return self._fill(object_, preposition_object)

    def _inspect(self, object_: Well, preposition_object: "Object" = None):
        str_ = object_.description
        if object_.state is self.object_type.States.FULL:
            str_ += " The well is full of water."
        elif object_.fills_until_full:
            str_ += " The well has some water in it."
        else:
            str_ += " The well is empty."
        return str_

    def _enter(self, object_: Well, preposition_object: "Object" = None):
        if object_.state is not self.object_type.States.FULL:
            return "Your body refuses to jump in without a way back up."
        print(self._effects_c.water_breathing(), self._player.effects)
        if self._effects_c.water_breathing() in self._player.effects:
            object_.items.remove(self._items_c.sword())
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

    def _fill_bucket(self, bucket: "Bucket"):
        if bucket not in self._player.inventory:
            return "You don't have a bucket."
        if bucket in self._player.equipped:
            return "You can't fill something you have equipped."
        if bucket.state is not bucket.States.EMPTY:
            return "The bucket is already full."
        bucket.state = bucket.States.WATER
        return "You fill the bucket with water."

    def _fill(self, object_: River, preposition_object: "Object" = None):
        if isinstance(preposition_object, type(self._items_c.bucket())):
            return self._fill_bucket(preposition_object)  # noqa
        return f"You can't fill '{preposition_object}' in the river."

