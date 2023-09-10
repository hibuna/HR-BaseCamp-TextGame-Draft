import logging
from typing import TYPE_CHECKING, Union, Optional

from src.enums import PlayerAction
from src.command import Command
from src.utils import subclass_in_list
from src.object.base import Item

if TYPE_CHECKING:
    from src.service import Service
    from src.player import Player
    from src.containers import Items, Objects, Services, Resolvers
    from src.config import Config
    from src.command import Command
    from src.object.base import Object
    from src.command import CommandValidator


class Engine:
    player: "Player"
    items_c: type["Items"]
    objects_c: type["Objects"]
    services_c: type["Services"]
    resolvers_c: type["Resolvers"]
    command_validator: "CommandValidator"
    config: type["Config"]

    def __new__(
            cls,
            player: "Player",
            items_c: type["Items"],
            objects_c: type["Objects"],
            services_c: type["Services"],
            resolvers_c: type["Resolvers"],
            command_validator: "CommandValidator",
            config: type["Config"],
    ):
        cls.player = player
        cls.items_c = items_c
        cls.objects_c = objects_c
        cls.services_c = services_c
        cls.resolvers_c = resolvers_c
        cls.config = config
        cls.command_validator = command_validator
        return super().__new__(cls)

    @classmethod
    def start(cls):
        while not cls._execute_command():
            pass

    @classmethod
    def _execute_command(cls) -> Optional[bool]:
        try:
            command = cls._get_command()
        except Exception as e:
            cls._print(e)
            return

        if not command:
            return

        if command.action is PlayerAction.QUIT:
            return True

        if command.action is PlayerAction.HELP:
            return cls._print_help()

        service = cls._get_service(command)
        logging.debug(f"Service: {type(service)}")

        response = service.interact(command)
        cls._print(response)

    @classmethod
    def _get_service(cls, command: "Command") -> Optional["Service"]:
        service = cls.resolvers_c.services().resolve(command.object)
        if service:
            return service
        if subclass_in_list(command.object, [Item]):
            return cls.services_c.item_service()
        return cls.services_c.generic_service()

    @classmethod
    def _get_command(cls) -> Optional["Command"]:
        user_input = cls._ask_input()
        if not user_input:
            return

        command = Command(user_input)
        cls.command_validator.validate(command)

        command = cls.resolvers_c.command_object().resolve_command(command)
        logging.debug(f"Command: {vars(command)}")

        return command

    @classmethod
    def _print(cls, msg: Union[str, Exception]) -> None:
        if isinstance(msg, Exception):
            msg = str(msg)
        print(msg)

    @classmethod
    def _print_help(cls) -> None:
        print("Help text")

    @classmethod
    def _inspect(cls, command: "Command") -> None:
        if command.object:
            cls._print(command.object.description)
        else:
            cls._print(cls.player.environment.description)

    @classmethod
    def _ask_input(cls) -> str:
        return input(cls.config.user_prompt)

    @classmethod
    def _is_object_available(cls, object_: "Object") -> bool:
        if object_ in cls.player.inventory:
            return True
        if object_ in cls.player.environment.objects:
            return True
        if object_ in cls.player.environment.items:
            return True
        return False
