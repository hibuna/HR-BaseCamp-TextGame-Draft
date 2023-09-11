from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.containers import Services
from src.enums import PlayerAction
from src.player import Player
from src.service import Service
from src.test.fixtures import (
    create_command,
    create_service,
    create_object,
    create_environment,
    create_item,
    create_equipable,
)


class ServiceTest(TestCase):
    @patch.object(Service, "_fill")
    def test_interact(self, service_mock):
        service = create_service()
        command = create_command(
            action=PlayerAction.FILL,
            object_=MagicMock(),
            preposition_object=MagicMock(),
        )

        service.interact(command)
        service_mock.assert_called_once_with(command)

    def test_inspect_object(self):
        service = create_service()
        object_ = create_object(description="Test")
        command = create_command(action=PlayerAction.INSPECT, object_=object_)

        self.assertEqual("Test", service._inspect(command))

    def test_inspect_environment(self):
        environment = create_environment(description="Test")
        player = Player(environment=environment)
        service = create_service(player=player)
        command = create_command()

        self.assertEqual("Test", service._inspect(command))


class ItemServiceTest(TestCase):
    service = Services.generic_service()
    item_service = Services.item_service()

    def test_pickup_item_not_valid_type(self):
        command = create_command(object_=create_object())

        self.assertEqual("You can't pick that up.", self.service._pickup(command))

    def test_pickup_item_not_pickupable(self):
        command = create_command(object_=create_item())
        command.object.interactions = []

        self.assertEqual("You can't pick that up.", self.service._pickup(command))

    @patch.object(item_service, "_player", new_callable=MagicMock)
    def test_pickup_item(self, player_mock):
        item = create_item(interactions=[PlayerAction.PICKUP])
        command = create_command(object_=item)

        self.assertEqual("Picked up: SOME NAME", self.item_service._pickup(command))
        player_mock.environment.items.remove.assert_called_once_with(item)
        player_mock.inventory.append.assert_called_once_with(item)

    def test_equip_item_not_in_inventory(self):
        command = create_command(object_=create_item())

        self.assertEqual("You don't have that.", self.item_service._equip(command))

    @patch.object(item_service, "_player", new_callable=MagicMock)
    def test_equip_item_not_equippable(self, player_mock):
        item = create_item(interactions=[PlayerAction.EQUIP])
        command = create_command(object_=item)
        player_mock.inventory = [item]

        self.assertEqual("You can't equip that.", self.item_service._equip(command))

    @patch.object(item_service, "_player", new_callable=MagicMock)
    def test_equip_item_not_equippable_interaction(self, player_mock):
        item = create_equipable()
        command = create_command(object_=item)
        player_mock.inventory = [item]

        self.assertEqual("You can't equip that.", self.item_service._equip(command))

    @patch.object(item_service, "_player", new_callable=MagicMock)
    def test_equip_item(self, player_mock):
        item = create_equipable(interactions=[PlayerAction.EQUIP])
        command = create_command(object_=item)
        player_mock.inventory = [item]

        self.item_service._equip(command)
        player_mock.equip.assert_called_once_with(item)

    def test_unequip_item_not_in_equipped(self):
        command = create_command(object_=create_item(name="test"))

        self.assertEqual(
            f"You don't have that equipped: TEST", self.item_service._unequip(command)
        )

    @patch.object(item_service, "_player", new_callable=MagicMock)
    def test_unequip_item(self, player_mock):
        item = create_equipable()
        command = create_command(object_=item)
        player_mock.equipped = [item]

        self.item_service._unequip(command)
        player_mock.unequip.assert_called_once_with(item)
