from copy import copy
from unittest import TestCase
from unittest.mock import patch, MagicMock

from dependency_injector.providers import Singleton

from src.containers import Resolvers, Items, Services, Objects
from src.object.base import Object
from src.object.items import Bucket
from src.object.objects import Well
from src.service import WellService
from src.test.fixtures import create_command


class ObjectResolverTest(TestCase):
    resolver = Resolvers.objects()

    def test_resolve_by_str_reference_valid(self):
        result = self.resolver._resolve_by_str("water well", "key", Objects.well())
        self.assertEqual(Objects.well(), result)

    def test_resolve_by_str_name_valid(self):
        result = self.resolver._resolve_by_str("well", "key", Objects.well())
        self.assertEqual(Objects.well(), result)

    @patch.object(Well, "name", new_callable=lambda: "some_name")
    def test_resolve_by_str_key_valid(self, _):
        self.assertEqual("some_name", Objects.well().name)
        result = self.resolver._resolve_by_str("well", "well", Objects.well())
        self.assertEqual(Objects.well(), result)

    def test_resolve_by_str_invalid(self):
        result = self.resolver._resolve_by_str("invalid", "key", Objects.well())
        self.assertIsNone(result)

    def test_resolve_by_object_type_valid(self):
        resolver = copy(self.resolver)
        resolver.container = MagicMock()
        resolver.container.members.items = {"key": Singleton(Well)}
        result = self.resolver.resolve(Well)
        self.assertEqual(Objects.well(), result)

    def test_resolve_by_object_type_invalid(self):
        resolver = copy(self.resolver)
        resolver.container = MagicMock()
        resolver.container.members.items = {"key": Singleton(Well)}
        result = self.resolver.resolve(Bucket)
        self.assertIsNone(result)


class ItemResolverTest(TestCase):
    def test_resolve_valid(self):
        resolver = Resolvers.items()
        result = resolver.resolve("bucket")
        self.assertEqual(Items.bucket(), result)

    def test_resolve_invalid(self):
        resolver = Resolvers.items()
        result = resolver.resolve("invalid")
        self.assertIsNone(result)


class ServiceResolverTest(TestCase):
    resolver = Resolvers.services()

    def test_resolve_by_item_instance_valid(self):
        result = self.resolver.resolve(Items.bucket())
        self.assertEqual(Services.bucket_service(), result)

    def test_resolve_by_item_type_valid(self):
        result = self.resolver.resolve(Bucket)
        self.assertEqual(Services.bucket_service(), result)

    def test_resolve_by_object_instance_valid(self):
        result = self.resolver.resolve(Objects.well())
        self.assertEqual(Services.well_service(), result)

    def test_resolve_by_object_type_valid(self):
        result = self.resolver.resolve(Well)
        self.assertEqual(Services.well_service(), result)

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
        command = create_command(object_str="bucket", preposition_object_str="bucket")
        command = self.resolver.resolve_command(command)
        self.assertEqual(Items.bucket(), command.object)
        self.assertEqual(Items.bucket(), command.preposition_object)

    def test_resolve_item_str_valid(self):
        result = self.resolver.resolve("bucket")
        self.assertEqual(Items.bucket(), result)

    def test_resolve_item_str_invalid(self):
        result = self.resolver.resolve("invalid_item")
        self.assertIsNone(result)

    def test_resolve_object_str_valid(self):
        result = self.resolver.resolve("well")
        self.assertEqual(Objects.well(), result)

    def test_resolve_object_str_invalid(self):
        result = self.resolver.resolve("invalid_object")
        self.assertIsNone(result)
