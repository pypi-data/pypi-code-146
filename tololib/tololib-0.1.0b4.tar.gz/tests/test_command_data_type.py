from unittest import TestCase

from tololib.command_data_type import Boolean, Integer, IntegerEnum, OptionalInteger
from tololib.const import LampMode


class BooleanTest(TestCase):
    def test_to_typed(self) -> None:
        cdt = Boolean()
        self.assertEqual(cdt.to_typed(True), True)
        self.assertEqual(cdt.to_typed("true"), True)
        self.assertEqual(cdt.to_typed("1"), True)
        self.assertEqual(cdt.to_typed("on"), True)
        self.assertEqual(cdt.to_typed("yes"), True)

        self.assertEqual(cdt.to_typed(False), False)
        self.assertEqual(cdt.to_typed("false"), False)
        self.assertEqual(cdt.to_typed("0"), False)
        self.assertEqual(cdt.to_typed("off"), False)
        self.assertEqual(cdt.to_typed("no"), False)

        self.assertRaises(ValueError, cdt.to_typed, "foobar")

    def test_to_byte(self) -> None:
        cdt = Boolean()
        self.assertEqual(cdt.to_byte(True), 1)
        self.assertEqual(cdt.to_byte(False), 0)


class IntegerTest(TestCase):
    def test_to_typed(self) -> None:
        cdt = Integer(10, 90)
        self.assertEqual(cdt.to_typed(42), 42)
        self.assertEqual(cdt.to_typed("42"), 42)

        self.assertRaises(ValueError, cdt.to_typed, 9)

        self.assertRaises(ValueError, cdt.to_typed, None)
        self.assertRaises(ValueError, cdt.to_typed, "foobar")


class OptionalIntegerTest(TestCase):
    def test_to_typed(self) -> None:
        cdt = OptionalInteger(1, 60, 61)
        self.assertEqual(cdt.to_typed(61), None)
        self.assertEqual(cdt.to_typed(42), 42)
        self.assertEqual(cdt.to_typed("42"), 42)

        self.assertRaises(ValueError, cdt.to_typed, 0)

    def test_to_byte(self) -> None:
        cdt = OptionalInteger(1, 60, 61)
        self.assertEqual(cdt.to_byte(None), 61)


class IntegerEnumTest(TestCase):
    def test_to_typed(self) -> None:
        cdt = IntegerEnum(LampMode)
        self.assertEqual(cdt.to_typed(LampMode.MANUAL), LampMode.MANUAL)
        self.assertEqual(cdt.to_typed(LampMode.AUTOMATIC), LampMode.AUTOMATIC)
        self.assertEqual(cdt.to_typed(0), LampMode.MANUAL)
        self.assertEqual(cdt.to_typed(1), LampMode.AUTOMATIC)
        self.assertEqual(cdt.to_typed("Manual"), LampMode.MANUAL)
        self.assertEqual(cdt.to_typed("automatic"), LampMode.AUTOMATIC)

        self.assertRaises(ValueError, cdt.to_typed, LampMode)

    def test_to_byte(self) -> None:
        cdt = IntegerEnum(LampMode)
        self.assertEqual(cdt.to_byte(LampMode.MANUAL), 0)
        self.assertEqual(cdt.to_byte(LampMode.AUTOMATIC), 1)
