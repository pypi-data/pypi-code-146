"""
@Author = 'Michael Stanley'

============ Change Log ============
10/1/2020 = Created.

============ License ============
Copyright (C) 2020 Michael Stanley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import wmul_test_utils

from collections import namedtuple


def test_make_namedtuple_one_field():
    class_name = "class_name"
    field_one = "field_one"
    field_one_value = "field_one_value"

    expected_named_tuple_class = namedtuple(
        class_name,
        [
            field_one
        ]
    )

    expected_named_tuple = expected_named_tuple_class(
        field_one=field_one_value
    )

    received_namedtuple = wmul_test_utils.make_namedtuple(
        class_name,
        field_one=field_one_value
    )

    assert expected_named_tuple == received_namedtuple


def test_make_namedtuple_multiple_fields():
    class_name = "class_name"
    field_one = "field_one"
    field_one_value = "field_one_value"
    field_two = "field_two"
    field_two_value = "field_two_value"

    expected_named_tuple_class = namedtuple(
        class_name,
        [
            field_one,
            field_two
        ]
    )

    expected_named_tuple = expected_named_tuple_class(
        field_one=field_one_value,
        field_two=field_two_value
    )

    received_namedtuple = wmul_test_utils.make_namedtuple(
        class_name,
        field_one=field_one_value,
        field_two=field_two_value
    )

    assert expected_named_tuple == received_namedtuple


def test_generate_true_false_matrix_from_namedtuple():
    my_test_flags = namedtuple("my_test_flags", ["with_cheese", "with_ketchup", "with_mustard"])

    tfm, test_ids = wmul_test_utils.generate_true_false_matrix_from_namedtuple(input_namedtuple=my_test_flags)

    expected_tfm = [
        my_test_flags(with_cheese=False, with_ketchup=False, with_mustard=False),
        my_test_flags(with_cheese=True, with_ketchup=False, with_mustard=False),
        my_test_flags(with_cheese=False, with_ketchup=True, with_mustard=False),
        my_test_flags(with_cheese=True, with_ketchup=True, with_mustard=False),
        my_test_flags(with_cheese=False, with_ketchup=False, with_mustard=True),
        my_test_flags(with_cheese=True, with_ketchup=False, with_mustard=True),
        my_test_flags(with_cheese=False, with_ketchup=True, with_mustard=True),
        my_test_flags(with_cheese=True, with_ketchup=True, with_mustard=True)
    ]

    expected_ids = [
        'my_test_flags(with_cheese=False, with_ketchup=False, with_mustard=False)',
        'my_test_flags(with_cheese=True, with_ketchup=False, with_mustard=False)',
        'my_test_flags(with_cheese=False, with_ketchup=True, with_mustard=False)',
        'my_test_flags(with_cheese=True, with_ketchup=True, with_mustard=False)',
        'my_test_flags(with_cheese=False, with_ketchup=False, with_mustard=True)',
        'my_test_flags(with_cheese=True, with_ketchup=False, with_mustard=True)',
        'my_test_flags(with_cheese=False, with_ketchup=True, with_mustard=True)',
        'my_test_flags(with_cheese=True, with_ketchup=True, with_mustard=True)'
    ]

    assert tfm == expected_tfm
    assert test_ids == expected_ids
