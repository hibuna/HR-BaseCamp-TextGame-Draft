from copy import copy
from unittest import TestCase
from unittest.mock import patch

from src.effect import Effect
from src.enums import EquipableSlot
from src.object.base import Equipable
from src.player import Player


class PlayerTest(TestCase):
    effect_1 = Effect()
    effect_2 = Effect()
    equipable = Equipable()

    @classmethod
    def setUpClass(cls):
        cls.effect_1.name = "Test Effect 1"
        cls.effect_1.description = "Test Description 1"
        cls.effect_2.name = "Test Effect 2"
        cls.effect_2.description = "Test Description 2"
        cls.equipable.name = "Test Equipable"
        cls.equipable.description = "Test Description"
        cls.equipable.slot = EquipableSlot.HEAD

    def test_get_equipped(self):
        player = Player()

        expected = None
        result = player._get_equipped(EquipableSlot.HEAD)
        self.assertEqual(expected, result)

    def test_get_equipped_with_item(self):
        player = Player(equipped=[self.equipable])

        expected = self.equipable
        result = player._get_equipped(EquipableSlot.HEAD)
        self.assertEqual(expected, result)

    def test_get_equipped_with_item_in_different_slot(self):
        player = Player(equipped=[self.equipable])

        expected = None
        result = player._get_equipped(EquipableSlot.BODY)
        self.assertEqual(expected, result)

    def test_add_effects_no_effects(self):
        player = Player()

        self.assertEqual("", player.add_effects([]))

    def test_add_effects_with_effects(self):
        player = Player()

        expected = f"You gain the following effects: TEST EFFECT 1, TEST EFFECT 2."
        result = player.add_effects([self.effect_1, self.effect_2])
        self.assertEqual(expected, result)

    def test_add_effects_duplicate_effects(self):
        player = Player()

        expected = f"You gain the following effects: TEST EFFECT 1."
        result = player.add_effects([self.effect_1, self.effect_1])
        self.assertEqual(expected, result)

    def test_remove_effects_no_effects(self):
        player = Player()

        self.assertEqual("", player.remove_effects([]))

    def test_remove_effects_with_effects(self):
        player = Player(effects=[self.effect_1])

        expected = f"You lose the following effects: TEST EFFECT 1."
        result = player.remove_effects([self.effect_1])
        self.assertEqual(expected, result)

    def test_remove_effects_duplicate_effects(self):
        player = Player(effects=[self.effect_1])

        expected = f"You lose the following effects: TEST EFFECT 1."
        result = player.remove_effects([self.effect_1, self.effect_1])
        self.assertEqual(expected, result)

    def test_equip_item(self):
        player = Player()

        expected = f"Equipped: TEST EQUIPABLE."
        result = player.equip(self.equipable)
        self.assertEqual(expected, result)

        expected = [self.equipable]
        result = player.equipped
        self.assertEqual(expected, result)

    def test_equip_item_already_equipped(self):
        player = Player(equipped=[self.equipable])

        expected = f"Already equipped: TEST EQUIPABLE."
        result = player.equip(self.equipable)
        self.assertEqual(expected, result)

        self.assertEqual([self.equipable], player.equipped)

    def test_equip_item_slot_taken(self):
        player = Player(equipped=[self.equipable])

        equipable = copy(self.equipable)

        expected = f"You already have something equipped: HEAD"
        result = player.equip(equipable)
        self.assertEqual(expected, result)

        self.assertEqual([self.equipable], player.equipped)

    @patch.object(Player, "add_effects", return_value="")
    def test_equip_item_with_effect(self, add_effects_mock):
        player = Player()
        equipable = copy(self.equipable)
        equipable.effects = [self.effect_1]

        expected = f"Equipped: TEST EQUIPABLE."
        result = player.equip(equipable)
        self.assertEqual(expected, result)

        expected = [equipable]
        result = player.equipped
        self.assertEqual(expected, result)

        add_effects_mock.assert_called_once_with([self.effect_1])

    def test_equip_item_integration_with_effect(self):
        player = Player()
        equipable = copy(self.equipable)
        equipable.effects = [self.effect_1]

        expected = (
            f"Equipped: TEST EQUIPABLE. You gain the following effects: TEST EFFECT 1."
        )
        result = player.equip(equipable)
        self.assertEqual(expected, result)

        self.assertEqual([equipable], player.equipped)
        self.assertEqual([self.effect_1], player.effects)

    def test_unequip_item(self):
        player = Player(equipped=[self.equipable])

        expected = f"Unequipped: TEST EQUIPABLE."
        result = player.unequip(self.equipable)
        self.assertEqual(expected, result)

        self.assertEqual([], player.equipped)

    def test_unequip_item_not_equipped(self):
        player = Player()

        expected = f"You don't have that equipped: TEST EQUIPABLE"
        result = player.unequip(self.equipable)
        self.assertEqual(expected, result)

        self.assertEqual([], player.equipped)

    @patch.object(Player, "remove_effects", return_value="")
    def test_unequip_item_with_effect(self, remove_effects_mock):
        equipable = copy(self.equipable)
        player = Player(equipped=[equipable], effects=[self.effect_1])
        equipable.effects = [self.effect_1]

        expected = f"Unequipped: TEST EQUIPABLE."
        result = player.unequip(equipable)
        self.assertEqual(expected, result)

        self.assertEqual([], player.equipped)
        remove_effects_mock.assert_called_once_with([self.effect_1])

    def test_unequip_item_integration_with_effect(self):
        equipable = copy(self.equipable)
        player = Player(equipped=[equipable], effects=[self.effect_1])
        equipable.effects = [self.effect_1]

        expected = f"Unequipped: TEST EQUIPABLE. You lose the following effects: TEST EFFECT 1."
        result = player.unequip(equipable)
        self.assertEqual(expected, result)

        self.assertEqual([], player.equipped)
        self.assertEqual([], player.effects)
