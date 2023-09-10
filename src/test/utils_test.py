from unittest import TestCase

from src.enums import PlayerAction
from src.utils import (
    overlap,
    casefold_index,
    casefold_equals,
    casefold_in,
    enum_get,
    subclass_in_list,
)


class OverlapTest(TestCase):
    def test_ints_overlap(self):
        expected = [1]
        result = overlap([1, 2, 3], [1, 4, 5])
        self.assertEqual(expected, result)

    def test_ints_dont_overlap(self):
        expected = []
        result = overlap([1, 2, 3], [4, 5, 6])
        self.assertEqual(expected, result)

    def test_strings_overlap(self):
        expected = ["a"]
        result = overlap(["a", "b", "c"], ["a", "d", "e"])
        self.assertEqual(expected, result)

    def test_strings_dont_overlap(self):
        expected = []
        result = overlap(["a", "b", "c"], ["d", "e", "f"])
        self.assertEqual(expected, result)

    def test_multiple_overlap(self):
        expected = [1, 2]
        result = overlap([1, 2, 3], [1, 2, 4])
        self.assertEqual(expected, result)

    def test_custom_enum_overlap(self):
        expected = [PlayerAction.FILL]
        result = overlap(PlayerAction, ["a", PlayerAction.FILL, "e"])
        self.assertEqual(expected, result)


class CasefoldIndexTest(TestCase):
    def test_casefold_index(self):
        expected = 1
        result = casefold_index(["a", "b", "c"], "b")
        self.assertEqual(expected, result)

    def test_casefold_index_folded(self):
        expected = 1
        result = casefold_index(["a", "b", "c"], "B")
        self.assertEqual(expected, result)

    def test_casefold_index_not_found(self):
        result = casefold_index(["a", "b", "c"], "D")
        self.assertIsNone(result)


class CasefoldEqualsTest(TestCase):
    def test_casefold_equals(self):
        result = casefold_equals("a", "a")
        self.assertTrue(result)

        result = casefold_equals("a", "A")
        self.assertTrue(result)

        result = casefold_equals("A", "a")
        self.assertTrue(result)

    def test_casefold_not_equals(self):
        result = casefold_equals("a", "b")
        self.assertFalse(result)


class CasefoldInTest(TestCase):
    def test_casefold_in(self):
        result = casefold_in("a", ["b", "A", "b"])
        self.assertTrue(result)

    def test_casefold_in_not_in(self):
        result = casefold_in("a", ["b", "b"])
        self.assertFalse(result)


class EnumGetTest(TestCase):
    def test_enum_get(self):
        result = enum_get("fill", PlayerAction)
        self.assertEqual(PlayerAction.FILL, result)

    def test_enum_get_not_found(self):
        result = enum_get("abcde", PlayerAction)
        self.assertIsNone(result)


class EnumHasTest(TestCase):
    def test_enum_has(self):
        result = enum_get("fill", PlayerAction)
        self.assertEqual(PlayerAction.FILL, result)

    def test_enum_has_not_found(self):
        result = enum_get("abcde", PlayerAction)
        self.assertIsNone(result)


class SubclassInListTest(TestCase):
    class Int(int):
        ...

    class Int2(Int):
        ...

    def test_subclass_in_list_type_class(self):
        ls = [float, int, str]
        result = subclass_in_list(self.Int, ls)
        self.assertTrue(result)

    def test_subclass_in_list_type_object(self):
        ls = [float, int, str]
        result = subclass_in_list(self.Int(1), ls)
        self.assertTrue(result)

    def test_subclass_in_list_type_class2(self):
        ls = [float, int, str]
        result = subclass_in_list(self.Int2, ls)
        self.assertTrue(result)

    def test_subclass_in_list_type_object2(self):
        ls = [float, int, str]
        result = subclass_in_list(self.Int2(1), ls)
        self.assertTrue(result)

    def test_subclass_in_list_class_class(self):
        ls = [float, self.Int, str]
        result = subclass_in_list(self.Int, ls)
        self.assertTrue(result)

    def test_subclass_in_list_class_object(self):
        ls = [float, self.Int, str]
        result = subclass_in_list(self.Int(1), ls)
        self.assertTrue(result)

    def test_subclass_in_list_class_class2(self):
        ls = [float, self.Int, str]
        result = subclass_in_list(self.Int2, ls)
        self.assertTrue(result)

    def test_subclass_in_list_class_object2(self):
        ls = [float, self.Int, str]
        result = subclass_in_list(self.Int2(1), ls)
        self.assertTrue(result)

    def test_subclass_in_list_not_found(self):
        ls = [float, str]
        result = subclass_in_list(list, ls)
        self.assertFalse(result)
