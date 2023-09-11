from typing import Union
from unittest.mock import MagicMock

from src.command import Command
from src.enums import PlayerAction, PlayerActionPreposition, EquipableSlot
from src.environment import Environment
from src.object.base import Object, Item, Equipable
from src.player import Player
from src.service import Service


def create_command(
    action_str: str = None,
    object_str: str = None,
    preposition_str: str = None,
    preposition_object_str: str = None,
    action: PlayerAction = None,
    object_: Union[Object, Item] = None,
    preposition: PlayerActionPreposition = None,
    preposition_object: Object = None,
):
    command = Command("")
    command.action_str = action_str
    command.object_str = object_str
    command.preposition_str = preposition_str
    command.preposition_object_str = preposition_object_str
    command.action = action
    command.object = object_
    command.preposition = preposition
    command.preposition_object = preposition_object
    return command


def create_object(
    name: str = None, description: str = None, interactions: list[PlayerAction] = None
):
    object_ = Object()
    object_.name = name or "some name"
    object_.description = description or "some description"
    object_.interactions = interactions or []
    return object_


def create_item(
    name: str = None, description: str = None, interactions: list[PlayerAction] = None
):
    item = Item()
    item.name = name or "some name"
    item.description = description or "some description"
    item.interactions = interactions or []
    return item


def create_equipable(
    name: str = None,
    description: str = None,
    interactions: list[PlayerAction] = None,
    slot: str = None,
):
    equipable = Equipable()
    equipable.name = name or "some name"
    equipable.description = description or "some description"
    equipable.interactions = interactions or []
    equipable.slot = slot or EquipableSlot.HEAD
    return equipable


def create_service(player: Player = None):
    return Service(
        player=player or MagicMock(),
        effects_c=MagicMock(),
        items_c=MagicMock(),
        objects_c=MagicMock(),
        environments_c=MagicMock(),
    )


def create_environment(
    name: str = None,
    description: str = None,
    items: list[Item] = None,
    objects: list[Object] = None,
):
    objects = objects or []
    items = items or []
    environment = Environment(objects=objects, items=items)
    environment.name = name or "some name"
    environment.description = description or "some description"
    return environment
