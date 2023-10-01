import logging
from typing import TYPE_CHECKING, Optional, Union

from src.utils import casefold_index, enum_has, subclass_in_list, enum_get, casefold_in
from src.enums import PlayerAction, PlayerActionPreposition, UsageFormat
from src.object.base import Object, Item

if TYPE_CHECKING:
    from src.resolvers import CommandObjectResolver
    from config import Config
    from src.player import Player


class switch_command_objects:
    def __init__(self, cmd: "Command") -> None:
        self.cmd = cmd

    def _switch_objects(self):
        self.cmd.object_str, self.cmd.preposition_object_str = (
            self.cmd.preposition_object_str,
            self.cmd.object_str,
        )
        self.cmd.object, self.cmd.preposition_object = (
            self.cmd.preposition_object,
            self.cmd.object,
        )

    def __enter__(self):
        self._switch_objects()
        logging.debug(f"Switched objects: {self.cmd}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._switch_objects()


class CommandUsage:
    _format: list[UsageFormat]
    action: PlayerAction
    object_types: list[type]
    preposition: Optional[PlayerActionPreposition]
    preposition_object_types: list[type]

    def __str__(self):
        object_types = [t.__name__ for t in self.object_types or []]
        preposition_object_types = [
            t.__name__ for t in self.preposition_object_types or []
        ]
        return f"{self.action} {object_types} {self.preposition} {preposition_object_types}"

    def __repr__(self):
        return f"<{str(self)}>"

    def __init__(
        self,
        action: PlayerAction,
        object_types: list[type] = None,
        preposition: Optional[PlayerActionPreposition] = None,
        preposition_object_types: list[type] = None,
    ) -> None:
        self.action = action
        self.object_types = object_types
        self.preposition = preposition
        self.preposition_object_types = preposition_object_types

    @property
    def object_amt(self) -> int:
        return len([b for b in [self.object_types, self.preposition_object_types] if b])


class Command:
    action_str: Optional[str] = None
    object_str: Optional[str] = None
    preposition_str: Optional[str] = None
    preposition_object_str: Optional[str] = None

    action: Optional[PlayerAction] = None
    object: Optional[Union["Object", "Item"]] = None
    preposition: Optional[PlayerActionPreposition] = None
    preposition_object: Union["Object", "Item"] = None

    def __init__(self, command: str) -> None:
        self.dissected_cmd = self._dissect_cmd(command)
        self.action_str = self._extract_action(self.dissected_cmd)
        self.preposition_str = self._extract_preposition(self.dissected_cmd)
        self.object_str = self._extract_object(self.dissected_cmd)
        self.preposition_object_str = self._extract_preposition_object(
            self.dissected_cmd
        )

    def __str__(self):
        return f"Command({self.action_str}:{self.action} {self.object_str}:{self.object} {self.preposition_str}:{self.preposition} {self.preposition_object_str}:{self.preposition_object})"

    @staticmethod
    def _dissect_cmd(command: str) -> list[str]:
        """Remove extra spaces and split the command into a list of words."""
        return " ".join(command.upper().split()).split(" ")

    @staticmethod
    def _dissected_cmd_has_preposition(dissected_cmd: list[str]) -> bool:
        return any(enum_has(word, PlayerActionPreposition) for word in dissected_cmd)

    @staticmethod
    def _extract_action(dissected_cmd: list[str]) -> str:
        return dissected_cmd[0]

    def _extract_preposition(self, dissected_cmd: list[str]) -> Optional[str]:
        if not self._dissected_cmd_has_preposition(dissected_cmd):
            return None

        preposition_str = next(
            word for word in dissected_cmd if enum_has(word, PlayerActionPreposition)
        )
        return preposition_str

    def _extract_object(self, dissected_cmd: list[str]) -> Optional[str]:
        if len(dissected_cmd) == 1:
            return None

        if not self._dissected_cmd_has_preposition(dissected_cmd):
            return " ".join(dissected_cmd[1:])

        preposition_index = casefold_index(dissected_cmd, str(self.preposition_str))
        return " ".join(dissected_cmd[1:preposition_index])

    def _extract_preposition_object(self, dissected_cmd: list[str]) -> Optional[str]:
        if not self.preposition_str:
            return None

        preposition_index = casefold_index(dissected_cmd, str(self.preposition_str))
        return " ".join(dissected_cmd[preposition_index + 1 :]) or None


class CommandValidator:
    cmd: Command

    def __init__(
        self,
        player: "Player",
        command_object_r: "CommandObjectResolver",
        config: type["Config"],
    ) -> None:
        self._player = player
        self._command_object_r = command_object_r
        self._config = config

    def validate(self, cmd: Command) -> None:
        self.cmd = cmd
        self._validate_action()
        logging.debug(f"Validated action: {self.cmd.action_str}")
        self._validate_object()
        logging.debug(f"Validated object: {self.cmd.object_str}")
        self._validate_preposition()
        logging.debug(f"Validated preposition: {self.cmd.preposition_str}")
        self._validate_preposition_object()
        logging.debug(
            f"Validated preposition object: {self.cmd.preposition_object_str}"
        )
        self._validate_usage()
        logging.debug(f"Validated usage: {self._usage}")

    def _validate_action(self) -> None:
        if self.cmd.action_str == "":
            return
        if not enum_has(self.cmd.action_str, PlayerAction) or not self._usages:
            raise ValueError(f"Action not recognized: {self.cmd.action_str.upper()}")

    def _validate_object(self) -> None:
        if not self._object_required and not self.cmd.object_str:
            return

        if casefold_in(self.cmd.object_str, ["self", "player"]):
            return

        if self._object_required and not self.cmd.object_str:
            raise ValueError(f"Action requires object: {self.cmd.action_str.upper()}")

        if not self._object or not self._object_available(self._object):
            raise ValueError(f"Object not found: {self.cmd.object_str.upper()}")

        if self.cmd.action_str not in self._object.interactions:
            raise ValueError(
                f"Cannot perform: {self.cmd.action_str.upper()} on {self.cmd.object_str.upper()}"
            )

    def _validate_preposition(self) -> None:
        if not self._preposition_required and not self.cmd.preposition_str:
            return

        if self._preposition_required and not self.cmd.preposition_str:
            raise ValueError(
                f"Action requires preposition: {self.cmd.action_str.upper()}"
            )

        if not enum_has(self.cmd.preposition_str, PlayerActionPreposition):
            raise ValueError(
                f"Preposition not recognized: {self.cmd.preposition_str.upper()}"
            )

        if self.cmd.preposition_str not in self._expected_prepositions:
            raise ValueError(
                f"Cannot perform: {self.cmd.action_str.upper()} with {self.cmd.preposition_str.upper()}"
            )

    def _validate_preposition_object(self) -> None:
        if (
            not self._preposition_object_required
            and not self.cmd.preposition_object_str
        ):
            return

        if self._preposition_object_required and not self.cmd.preposition_object_str:
            raise ValueError(
                f"Missing object after preposition: {self.cmd.preposition_str.upper()}"
            )

        object_unavailable = (
            not self._preposition_object
            or self._is_object(self._preposition_object)
            and not self._object_available(self._preposition_object)
            or self._is_item(self._preposition_object)
            and not self._holding_object(self._preposition_object)
        )
        if object_unavailable:
            raise ValueError(
                f"Object not found: {self.cmd.preposition_object_str.upper()}"
            )

    def _validate_usage(self) -> None:
        if not self._usage:
            raise ValueError(f"Invalid usage for action {self.cmd.action_str.upper()}")

    def _is_item(self, object_: "Object") -> bool:
        return issubclass(type(object_), Item)

    def _is_object(self, object_: "Object") -> bool:
        return issubclass(type(object_), Object) and not self._is_item(object_)

    def _holding_object(self, object_: "Object") -> bool:
        return object_ in self._player.inventory

    def _object_available(self, object_: "Object") -> bool:
        if object_ in self._player.environment.objects_and_items:
            return True
        if object_ in self._player.inventory:
            return True

    @property
    def _usages(self) -> list[CommandUsage]:
        enum_action = enum_get(self.cmd.action_str, PlayerAction)
        return self._config.action_usage_mapping.get(enum_action, [])

    @property
    def _usage(self) -> Optional[CommandUsage]:
        for usage in self._usages:
            if self._command_matches_usage(usage):
                return usage

    def _command_matches_usage(self, usage: CommandUsage) -> bool:
        if self._object and not usage.object_types:
            return False
        if self._object and usage.object_types:
            if not subclass_in_list(self._object, usage.object_types):
                return False
        if self._preposition_object and not usage.preposition_object_types:
            return False
        if self._preposition_object and usage.preposition_object_types:
            if not subclass_in_list(
                self._preposition_object, usage.preposition_object_types
            ):
                return False
        if usage.object_amt != self._object_amt:
            return False
        return True

    @property
    def _object(self):
        return self._command_object_r.resolve(self.cmd.object_str)

    @property
    def _preposition_object(self):
        return self._command_object_r.resolve(self.cmd.preposition_object_str)

    @property
    def _object_amt(self) -> int:
        """Check if command has an appropriate amount of objects."""
        return len(
            [b for b in [self.cmd.object_str, self.cmd.preposition_object_str] if b]
        )

    @property
    def _valid_object_amts(self) -> list[int]:
        """Check if command has an appropriate amount of objects."""
        enum_action = enum_get(self.cmd.action_str, PlayerAction)
        return self._config.action_object_amt_mapping.get(enum_action, [])

    @property
    def _object_required(self):
        return 0 not in self._valid_object_amts

    @property
    def _preposition_object_required(self):
        return self._valid_object_amts == [2]

    @property
    def _expected_prepositions(self) -> Optional[list[PlayerActionPreposition]]:
        return [usage.preposition for usage in self._usages]

    @property
    def _preposition_required(self) -> bool:
        return all([usage.preposition for usage in self._usages])
