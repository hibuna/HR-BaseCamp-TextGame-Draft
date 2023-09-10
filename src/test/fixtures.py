from src.command import Command
from src.enums import PlayerAction, PlayerActionPreposition
from src.object.base import Object


def create_command(
    action_str: str = None,
    object_str: str = None,
    preposition_str: str = None,
    preposition_object_str: str = None,
    action: PlayerAction = None,
    object_: Object = None,
    preposition: PlayerActionPreposition = None,
    preposition_object: Object = None,
):
    command = Command("")
    command.action_str = action_str
    command.object_str = object_str
    command.preposition_str = preposition_str
    command.preposition_object_str = preposition_object_str
    command.action = action
    command.object_ = object_
    command.preposition = preposition
    command.preposition_object = preposition_object
    return command
