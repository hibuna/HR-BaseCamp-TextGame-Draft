from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.object.base import Item, Object


class Environment:
    """
    An environment is a place in the game universe that contains objects and items.

    Attributes:
    -----------
    objects : list[Object]
        A list of objects in the environment.
    items : list[Item]
        A list of items in the environment.
    """

    name: str
    description: str
    objects: list["Object"]
    items: list["Item"]

    def __init__(self, objects: list[type["Object"]], items: list[type["Item"]] = None):
        self.objects = objects or []
        self.items = items or []

    @property
    def shown_objects(self):
        return [obj for obj in self.objects if obj.shown]

    @property
    def objects_and_items(self):
        return self.objects + self.items

    @property
    def shown_objects_and_items(self):
        return self.shown_objects + self.items

    @property
    def shown_objects_and_items_str(self):
        str_ = ""

        if self.shown_objects:
            str_ += (
                f"You see these objects: "
                f"{', '.join([obj.name for obj in self.shown_objects])}. "
            )

        if self.items:
            str_ += (
                f"You see these items: "
                f"{', '.join([item.name for item in self.items])}. "
            )

        return str_.strip()


class PrologueCockpit(Environment):
    name = "burning cockpit"
    description = "You wake up, hazily. You have a headache, and it's not from the loud buzzing alarms. You smell fire. You see fire. You feel fire. Fuck."


class Cockpit(Environment):
    name = "cockpit"
    description = "You are in the cockpit."


class Hallway(Environment):
    name = "hallway"
    description = "You are in a long empty hallway."


class Bathroom(Environment):
    name = "bathroom"
    description = "You are in a bathroom. You see 107 doors with different signs."


class EngineRoom(Environment):
    name = "engine room"
    description = "You are in the engine room. You see a huge round metal contraption. That must be the engine."


class Workshop(Environment):
    name = "workshop"
    description = "You are in the workshop. You see a workbench."


class Bedroom(Environment):
    name = "bedroom"
    description = "You are in the bedroom. There's a single bed. You must be dry as a bone."


class StorageRoom(Environment):
    name = "storage room"
    description = "You are in the storage room."


class Armory(Environment):
    name = "armory"
    description = "You are in the armory."


class Canteen(Environment):
    name = "canteen"
    description = "You are in the canteen. You see a table with a few chairs."


class Outside(Environment):
    name = "outside"
    description = "You are floating around the ship."
