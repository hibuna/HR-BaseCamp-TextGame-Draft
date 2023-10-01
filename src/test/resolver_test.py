from copy import copy
from unittest import TestCase
from unittest.mock import patch, MagicMock

from dependency_injector.providers import Singleton

from src.containers import Resolvers, Items, Services, Objects
from src.object.base import Object
from src.object.items import SpaceSuit
from src.object.objects import ControlPanel
from src.test.fixtures import create_command


class ObjectResolverTest(TestCase):
    resolver = Resolvers.objects()

    def test_resolve_by_str_reference_valid(self):
        result = self.resolver._resolve_by_str("panel", "key", Objects.control_panel())
        self.assertEqual(Objects.control_panel(), result)

    def test_resolve_by_str_name_valid(self):
        result = self.resolver._resolve_by_str("control panel", "key", Objects.control_panel())
        self.assertEqual(Objects.control_panel(), result)

    @patch.object(ControlPanel, "name", new_callable=lambda: "some_name")
    def test_resolve_by_str_key_valid(self, _):
        self.assertEqual("some_name", Objects.control_panel().name)
        result = self.resolver._resolve_by_str("control panel", "control panel", Objects.control_panel())
        self.assertEqual(Objects.control_panel(), result)

    def test_resolve_by_str_invalid(self):
        result = self.resolver._resolve_by_str("invalid", "key", Objects.control_panel())
        self.assertIsNone(result)

    def test_resolve_by_object_type_valid(self):
        resolver = copy(self.resolver)
        resolver.container = MagicMock()
        resolver.container.members.items = {"key": Singleton(ControlPanel)}
        result = self.resolver.resolve(ControlPanel)
        self.assertEqual(Objects.control_panel(), result)

    def test_resolve_by_object_type_invalid(self):
        resolver = copy(self.resolver)
        resolver.container = MagicMock()
        resolver.container.members.items = {"key": Singleton(ControlPanel)}
        result = self.resolver.resolve(SpaceSuit)
        self.assertIsNone(result)


class ItemResolverTest(TestCase):
    def test_resolve_valid(self):
        resolver = Resolvers.items()
        result = resolver.resolve("space suit")
        self.assertEqual(Items.space_suit(), result)

    def test_resolve_invalid(self):
        resolver = Resolvers.items()
        result = resolver.resolve("invalid")
        self.assertIsNone(result)


class ServiceResolverTest(TestCase):
    resolver = Resolvers.services()

    def test_resolve_by_item_instance_valid(self):
        result = self.resolver.resolve(Items.space_suit())
        self.assertEqual(Services.space_suit_service(), result)

    def test_resolve_by_item_type_valid(self):
        result = self.resolver.resolve(SpaceSuit)
        self.assertEqual(Services.space_suit_service(), result)

    def test_resolve_by_object_instance_valid(self):
        result = self.resolver.resolve(Objects.control_panel())
        self.assertEqual(Services.control_panel_service(), result)

    def test_resolve_by_object_type_valid(self):
        result = self.resolver.resolve(ControlPanel)
        self.assertEqual(Services.control_panel_service(), result)

    def test_resolve_by_object_invalid(self):
        result = self.resolver.resolve(Object)
        self.assertIsNone(result)


class CommandObjectResolverTest(TestCase):
    resolver = Resolvers.command_object()

    def test_resolve_command_object_invalid(self):
        command = create_command(
            object_str="invalid_object",
            preposition_object_str="invalid_preposition_object",
        )
        command = self.resolver.resolve_command(command)
        self.assertIsNone(command.object)
        self.assertIsNone(command.preposition_object)

    def test_resolve_command_object_valid(self):
        command = create_command(object_str="space suit", preposition_object_str="space suit")
        command = self.resolver.resolve_command(command)
        self.assertEqual(Items.space_suit(), command.object)
        self.assertEqual(Items.space_suit(), command.preposition_object)

    def test_resolve_item_str_valid(self):
        result = self.resolver.resolve("space suit")
        self.assertEqual(Items.space_suit(), result)

    def test_resolve_item_str_invalid(self):
        result = self.resolver.resolve("invalid_item")
        self.assertIsNone(result)

    def test_resolve_object_str_valid(self):
        result = self.resolver.resolve("control panel")
        self.assertEqual(Objects.control_panel(), result)

    def test_resolve_object_str_invalid(self):
        result = self.resolver.resolve("invalid_object")
        self.assertIsNone(result)
