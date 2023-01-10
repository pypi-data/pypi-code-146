"""Test the helpers functions."""
from sugarpie.sugarpie.helpers import _set_bit, _clear_bit


def test_pisugar_set_bit_on():
    """Set one bit on a clear byte."""
    result = _set_bit(0x00, 7)
    assert result == 0x80


def test_pisugar_set_bit_on_again():
    """Set one bit that is already set on a byte."""
    result = _set_bit(0x80, 7)
    assert result == 0x80


def test_pisugar_set_bit_on_busy_byte():
    """Set one bit on a byte that has other bits set."""
    result = _set_bit(0x13, 7)
    assert result == 0x93


def test_pisugar_set_bit_off():
    """Set one bit off on a clear byte."""
    result = _clear_bit(0x00, 7)
    assert result == 0x00


def test_pisugar_set_bit_off_busy_byte():
    """Set one bit off on a byte that has other bits set."""
    result = _clear_bit(0x93, 7)
    assert result == 0x13
