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

    @property
    def description(self):
        str_ = "You wake up, hazily. You have a headache, and it's not from the loud buzzing alarms. You smell fire. You see fire. You feel fire. Fuck. "
        str_ += self.shown_objects_and_items_str
        return str_.strip()


class Cockpit(Environment):
    name = "cockpit"
    description = "You are in the cockpit."
