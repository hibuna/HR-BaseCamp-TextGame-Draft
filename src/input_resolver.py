# TODO: rename, separate(?), refactor
import logging
from typing import TYPE_CHECKING

from src.enums import PlayerAction, PlayerActionPreposition
from src.item import Item

if TYPE_CHECKING:
    from containers import Items, Objects, Services
    from src.object import Object


preposition_mapping = {
    PlayerAction.FILL: [PlayerActionPreposition.WITH, PlayerActionPreposition.IN],
    PlayerAction.EMPTY: [PlayerActionPreposition.INTO, PlayerActionPreposition.IN],
}


class Command:
    action: PlayerAction
    object: str = None
    preposition: PlayerActionPreposition = None
    preposition_object: str = None

    def __init__(self, command: str) -> None:
        dissected_command = self._dissect_command(command)
        self._extract_parts(dissected_command)

    @staticmethod
    def _dissect_command(command: str) -> list[str]:
        return command.strip().split(" ")

    def _extract_parts(self, dissected_cmd: list[str]) -> None:
        """
        :raises ValueError: The first word in the command is not a valid action,
          the action is not allowed to have a preposition
          or the action requires a preposition.
        """
        self.action = PlayerAction[dissected_cmd[0]]
        if self.action is None:
            raise ValueError(f"'{dissected_cmd[0].upper()}' not recognized")

        expected_prepositions = preposition_mapping.get(self.action)
        if any(word in PlayerActionPreposition for word in dissected_cmd):
            if not expected_prepositions:
                raise ValueError("This action has no preposition")
            self._extract_parts_preposition(dissected_cmd, expected_prepositions)
        else:
            if expected_prepositions:
                raise ValueError("This action requires a preposition")
            self._extract_parts_basic(dissected_cmd)

    def _extract_parts_basic(self, dissected_cmd: list[str]) -> None:
        """:raises ValueError: The action is not allowed to have an object."""
        object_ = " ".join(dissected_cmd[1:])
        if self.action is PlayerAction.HELP:
            object_ = object_ or None  # empty string -> None
        self.object = object_

    def _extract_parts_preposition(
            self,
            dissected_cmd: list[str],
            expected_prepositions: list[PlayerActionPreposition]
    ) -> None:
        """:raises ValueError: Preposition is incorrect."""
        preposition = next(
            word for word in dissected_cmd if word in PlayerActionPreposition
        )
        if preposition not in expected_prepositions:
            raise ValueError(f"Expected preposition")

        self.object = " ".join(dissected_cmd[1:dissected_cmd.index(preposition)])
        self.preposition_object = (
            " ".join(dissected_cmd[dissected_cmd.index(preposition) + 1:])
        )


class Engine:  # TODO: Separate printing from Engine?
    items_c: "type(Items)"
    objects_c: "type(Objects)"
    services_c: "type(Services)"
    error_prefix: str = "Error: "
    user_prompt: str = "> "

    def __new__(
            cls,
            items_c: "type(Items)",
            objects_c: "type(Objects)",
            services_c: "type(Services)"
    ):
        cls.items_c = items_c
        cls.objects_c = objects_c
        cls.services_c = services_c
        return super().__new__(cls)

    @classmethod
    def print_error(cls, error: str | Exception):
        if isinstance(error, Exception):
            error = str(error)
        print(cls.error_prefix, error)

    @classmethod
    def print_help(cls):
        print("Help text")

    @classmethod
    def ask_input(cls):
        command = input(cls.user_prompt)
        try:
            command = Command(command)
        except ValueError as error:
            cls.print_error(error)
            return
        logging.debug(f"Command: {vars(command)}")

        if command.action is PlayerAction.HELP:
            cls.print_help()
            return

        object_: "Object" = cls.objects_c.get(command.object)
        if not object_:
            object_ = cls.items_c.get(command.object)

        logging.debug(f"Object: {object_}")

        if command.action is PlayerAction.INSPECT and not object_:
            print(cls.services_c.generic_service().interact(command.action, object_))
            return

        if not object_:
            cls.print_error(f"What is a '{command.object}'?")
            return

        preposition_object = cls.objects_c.get(command.preposition_object)
        if not preposition_object:
            preposition_object = cls.items_c.get(command.preposition_object)
        if not preposition_object:
            preposition_object = command.preposition_object

        logging.debug(f"Preposition object: {preposition_object}")

        if command.action in [PlayerAction.FILL, PlayerAction.EMPTY]:
            if issubclass(type(object_), Item) and not isinstance(preposition_object, str):
                object_, preposition_object = preposition_object, object_

        service = cls.services_c.get(object_)
        if not service:
            if issubclass(type(object_), Item):
                service = cls.services_c.item_service()
            else:
                service = cls.services_c.generic_service()
        logging.debug(f"Service: {type(service)}")

        result = service.interact(command.action, object_, preposition_object)
        logging.debug(f"Result: {result}")
        print(result)
