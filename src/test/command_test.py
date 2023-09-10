from unittest import TestCase

from src.config import Config
from src.containers import Objects, Resolvers, Items
from src.enums import PlayerActionPreposition
from src.command import Command, CommandValidator
from src.environment import Environment
from src.player import Player
from src.test.fixtures import create_command


class CommandTest(TestCase):
    command = Command

    @classmethod
    def setUpClass(cls) -> None:
        cls.command.__init__ = lambda self, command: None

    def test_dissect_command_single(self):
        command = "test"
        self.assertEqual(Command._dissect_cmd(command), ["TEST"])

    def test_dissect_command_multiple(self):
        command = "test command please"
        self.assertEqual(Command._dissect_cmd(command), ["TEST", "COMMAND", "PLEASE"])

    def test_dissect_command_trailing_spaces(self):
        command = "test command please  "
        self.assertEqual(Command._dissect_cmd(command), ["TEST", "COMMAND", "PLEASE"])

    def test_dissect_command_leading_spaces(self):
        command = "  test command please"
        self.assertEqual(Command._dissect_cmd(command), ["TEST", "COMMAND", "PLEASE"])

    def test_dissect_command_leading_and_trailing_spaces(self):
        command = "  test command please  "
        self.assertEqual(Command._dissect_cmd(command), ["TEST", "COMMAND", "PLEASE"])

    def test_dissect_command_empty(self):
        command = ""
        self.assertEqual(Command._dissect_cmd(command), [""])

    def test_dissect_command_only_spaces(self):
        command = "   "
        self.assertEqual(Command._dissect_cmd(command), [""])

    def test_dissect_command_multiple_spaces(self):
        command = "test   command please"
        self.assertEqual(Command._dissect_cmd(command), ["TEST", "COMMAND", "PLEASE"])

    def test_dissected_cmd_has_preposition(self):
        dissected_cmd = [str(PlayerActionPreposition.WITH)]
        self.assertTrue(Command._dissected_cmd_has_preposition(dissected_cmd))

    def test_extract_action_str(self):
        dissected_cmd = ["some_action"]
        action_str = Command._extract_action(dissected_cmd)
        self.assertEqual("some_action", action_str)

    def test_extract_action_str_multiple_words(self):
        dissected_cmd = ["some_action", "command", "please"]
        action_str = Command._extract_action(dissected_cmd)
        self.assertEqual("some_action", action_str)

    def test_extract_preposition(self):
        dissected_cmd = ["some_action", str(PlayerActionPreposition.WITH)]
        command = create_command(action_str="some_action")
        preposition_str = command._extract_preposition(dissected_cmd)
        self.assertEqual(str(PlayerActionPreposition.WITH), preposition_str)

    def test_extract_preposition_no_preposition(self):
        dissected_cmd = ["some_action", "obj"]
        command = create_command(action_str="some_action")
        preposition_str = command._extract_preposition(dissected_cmd)
        self.assertIsNone(preposition_str)

    def test_extract_object_command_len_1(self):
        dissected_cmd = ["some_action"]
        object_str = create_command()._extract_object(dissected_cmd)
        self.assertEqual(object_str, None)

    def test_extract_object_without_preposition(self):
        dissected_cmd = ["some_action", "obj"]
        command = create_command(action_str="some_action")
        object_str = command._extract_object(dissected_cmd)
        self.assertEqual(object_str, "obj")

    def test_extract_object_with_preposition_single_word(self):
        dissected_cmd = ["fill", "some_object", "with"]
        command = create_command(
            action_str="fill",
            preposition_str="with",
        )
        object_str = command._extract_object(dissected_cmd)
        self.assertEqual("some_object", object_str)

    def test_extract_object_with_preposition_multiple_words(self):
        dissected_cmd = ["some_action", "some", "object", "with"]
        command = create_command(action_str="some_action", preposition_str="with")
        object_str = command._extract_object(dissected_cmd)
        self.assertEqual("some object", object_str)

    def test_extract_preposition_object_no_preposition(self):
        dissected_cmd = ["some_action", "some", "object"]
        command = create_command(action_str="some_action")
        preposition_object_str = command._extract_preposition_object(dissected_cmd)
        self.assertIsNone(preposition_object_str)

    def test_extract_preposition_object_with_preposition_single_word(self):
        dissected_cmd = [
            "some_action",
            "obj",
            str(PlayerActionPreposition.WITH),
            "some_preposition_object",
        ]
        command = create_command(
            action_str="some_action", preposition_str=str(PlayerActionPreposition.WITH)
        )
        preposition_object_str = command._extract_preposition_object(dissected_cmd)
        self.assertEqual("some_preposition_object", preposition_object_str)

    def test_extract_preposition_object_with_preposition_multiple_words(self):
        dissected_cmd = [
            "some_action",
            "obj",
            str(PlayerActionPreposition.WITH),
            "some",
            "preposition",
            "object",
        ]
        command = create_command(
            action_str="some_action", preposition_str=str(PlayerActionPreposition.WITH)
        )
        preposition_object_str = command._extract_preposition_object(dissected_cmd)
        self.assertEqual(
            "some preposition object",
            preposition_object_str,
        )


class CommandValidatorTest(TestCase):
    config = Config
    validator = CommandValidator(
        player=Player(environment=Environment([])),
        command_object_r=Resolvers.command_object(),
        config=config,
    )

    def test_action_str_valid(self):
        self.validator.cmd = create_command(action_str="inspect")
        self.validator._validate_action()

    def test_action_empty(self):
        self.validator.cmd = create_command(action_str="")
        self.validator._validate_action()

    def test_action_str_invalid(self):
        self.validator.cmd = create_command(action_str="invalid")

        try:
            self.validator._validate_action()
        except ValueError as e:
            self.assertEqual("Action not recognized: INVALID", str(e))

    def test_object_valid(self):
        self.validator.cmd = create_command(action_str="inspect", object_str="well")
        self.validator._player.environment.objects = [Objects.well()]
        self.validator._validate_object()

    def test_object_missing(self):
        self.validator.cmd = create_command(action_str="fill", object_str=None)

        try:
            self.validator._validate_object()
        except ValueError as e:
            self.assertEqual(f"Action requires object: FILL", str(e))

    def test_object_not_required(self):
        self.validator.cmd = create_command(action_str="inspect", object_str=None)
        self.validator._validate_object()

    def test_object_invalid(self):
        self.validator.cmd = create_command(object_str="invalid")

        try:
            self.validator._validate_object()
        except ValueError as e:
            self.assertEqual("Object not found: INVALID", str(e))

    def test_object_unavailable(self):
        self.validator.cmd = create_command(action_str="fill", object_str="bucket")

        try:
            self.validator._validate_object()
        except ValueError as e:
            self.assertEqual("Object not found: BUCKET", str(e))

    def test_object_has_no_action(self):
        self.validator.cmd = create_command(action_str="equip", object_str="river")
        self.validator._player.environment.objects = [Objects.river()]

        try:
            self.validator._validate_object()
        except ValueError as e:
            self.assertEqual(f"Cannot perform: EQUIP on RIVER", str(e))

    def test_preposition_valid(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
            preposition_str="with",
        )
        self.validator._validate_preposition()

    def test_preposition_missing(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
        )

        try:
            self.validator._validate_preposition()
        except ValueError as e:
            self.assertEqual(f"Action requires preposition: FILL", str(e))

    def test_preposition_invalid(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
            preposition_str="invalid",
        )

        try:
            self.validator._validate_preposition()
        except ValueError as e:
            self.assertEqual(f"Preposition not recognized: INVALID", str(e))

    def test_preposition_not_for_action(self):
        self.validator.cmd = create_command(
            action_str="inspect",
            object_str="bucket",
            preposition_str="with",
        )

        try:
            self.validator._validate_preposition()
        except ValueError as e:
            self.assertEqual(f"Cannot perform: INSPECT with WITH", str(e))

    def test_preposition_object_valid(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
            preposition_str="with",
            preposition_object_str="river",
        )
        self.validator._player.environment.objects = [Objects.river()]
        self.validator._player.environment.items = [Items.bucket()]

        self.validator._validate_preposition_object()

    def test_preposition_object_not_required(self):
        self.validator.cmd = create_command(
            action_str="inspect",
        )

        self.validator._validate_preposition_object()

    def test_preposition_object_missing(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
            preposition_str="with",
        )

        try:
            self.validator._validate_preposition_object()
        except ValueError as e:
            self.assertEqual("Missing object after preposition: WITH", str(e))

    def test_preposition_object_invalid(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
            preposition_str="with",
            preposition_object_str="invalid",
        )

        try:
            self.validator._validate_preposition_object()
        except ValueError as e:
            self.assertEqual("Object not found: INVALID", str(e))

    def test_preposition_object_unavailable_object(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
            preposition_str="with",
            preposition_object_str="river",
        )

        try:
            self.validator._validate_preposition_object()
        except ValueError as e:
            self.assertEqual("Object not found: RIVER", str(e))

    def test_preposition_object_unavailable_item(self):
        self.validator.cmd = create_command(
            action_str="fill",
            object_str="bucket",
            preposition_str="with",
            preposition_object_str="bucket",
        )

        try:
            self.validator._validate_preposition_object()
        except ValueError as e:
            self.assertEqual("Object not found: BUCKET", str(e))

    # TODO: test helper methods and properties


# TODO: test command usage
