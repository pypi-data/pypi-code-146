"""Tests for utilities"""

from ...common.util import Util


def test_int_val_to_api_bool():
    assert Util.val_to_api_bool(-1) == 'false'
    assert Util.val_to_api_bool(0) == 'false'
    assert Util.val_to_api_bool(1) == 'true'
    assert Util.val_to_api_bool(2) == 'false'
    assert Util.val_to_api_bool(3) == 'false'
    assert Util.val_to_api_bool(99) == 'false'


def test_bool_val_to_api_bool():
    assert Util.val_to_api_bool(False) == 'false'
    assert Util.val_to_api_bool(True) == 'true'


def test_error_val_to_api_bool():
    # String
    assert Util.val_to_api_bool(
        'False') == "Error: Value False is of type <class 'str'>"
    assert Util.val_to_api_bool(
        'True') == "Error: Value True is of type <class 'str'>"

    # Double
    float_error_msg = "Error: Value 2.23232e-07 is of type <class 'float'>"
    assert Util.val_to_api_bool(0.000000223232) == float_error_msg


def test_get_opt_hash_val():
    h01 = {
        'test_01': 'value_01',
        'test_02': 'value_02',
        # 'test_03': '',
        'test_04': ''
    }
    val01 = Util.get_opt_hash_val(h01, 'test_01', "I'm the default value!")
    val01_without_default = Util.get_opt_hash_val(h01, 'test_01')
    assert val01 == 'value_01'
    assert val01_without_default == 'value_01'

    val02 = Util.get_opt_hash_val(h01, 'test_02', "I'm the default value!")
    val02_without_default = Util.get_opt_hash_val(h01, 'test_02')
    assert val02 == 'value_02'
    assert val02_without_default == 'value_02'

    val03 = Util.get_opt_hash_val(h01, 'test_03', "I'm the default value!")
    val03_without_default = Util.get_opt_hash_val(h01, 'test_03')
    assert val03 == "I'm the default value!"
    assert val03_without_default == ''

    val04 = Util.get_opt_hash_val(h01, 'test_04', "I'm the default value!")
    val04_without_default = Util.get_opt_hash_val(h01, 'test_04')
    assert val04 == ''
    assert val04_without_default == ''
