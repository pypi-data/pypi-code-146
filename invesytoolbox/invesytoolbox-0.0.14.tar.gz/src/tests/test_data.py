# coding=utf-8
"""
run the test from the sr/invesytoolbox directory:
python ../tests/test_data.py
"""

import sys
import unittest
import datetime
import DateTime
from dateutil.parser import parse

sys.path.append(".")

from itb_data import \
    any_2boolean, \
    create_vcard, \
    dict_2unicode, \
    dict_2datatypes, \
    dict_from_dict_list, \
    dictlist_2datatypes, \
    sort_dictlist

dict_list = [
    {'a': 1, 'b': 2, 'c': 5},
    {'a': 2, 'b': 3, 'c': 4},
    {'a': 3, 'b': 4, 'c': 3}
]

dict_list_sorted_by_c = [
    {'a': 3, 'b': 4, 'c': 3},
    {'a': 2, 'b': 3, 'c': 4},
    {'a': 1, 'b': 2, 'c': 5}
]

dicts_from_dict_list = [
    {
        1: {'b': 2, 'c': 5},
        2: {'b': 3, 'c': 4},
        3: {'b': 4, 'c': 3}
    },
    {
        1: {'a': 1, 'b': 2, 'c': 5},
        2: {'a': 2, 'b': 3, 'c': 4},
        3: {'a': 3, 'b': 4, 'c': 3}
    },
    {
        1: 2,
        2: 3,
        3: 4
    },
    {
        1: 5,
        2: 4,
        3: 3
    }
]

test_boolean = {
    True: True,
    False: False,
    1: True,
    '2': True,
    2: True,
    0: False,
    '0': False,
    b'0': False,
    'False': False,
    'True': True,
    b'False': False,
    b'True': True,
    'xyz': True,
}

dict_for_testing = {
    1: 'test one',
    '2': b'test two',
    b'3': 'test three',
    True: 'test four',  # overrides 1
    'five': 5,
    b'six': True,
    b'7.0': ['1', b'2'],
    8.0: {'a': b'xy'},
    '9.0': 'False',
    b'False': b'True',
    'x': '01.04.2022',
    'y': '10:32'
}

dict_for_testing_unicoded = {
    1: 'test four',
    '2': 'test two',
    '3': 'test three',
    'five': 5,
    'six': True,
    '7.0': ['1', b'2'],
    8.0: {'a': b'xy'},
    '9.0': 'False',
    'False': 'True',
    'x': '01.04.2022',
    'y': '10:32'
}

dict_for_testing_datatyped = {
    1: 'test four',
    2: b'test two',
    3: 'test three',
    'five': 5,
    b'six': True,
    7.0: ['1', b'2'],
    8.0: {'a': b'xy'},
    9.0: False,
    False: True,
    'x': datetime.date(2022, 4, 1),
    'y': parse('10:32').time()
}

dict_for_testing_datatyped_unicoded = {
    1: 'test four',
    2: 'test two',
    3: 'test three',
    'five': 5,
    'six': True,
    7.0: ['1', b'2'],
    8.0: {'a': b'xy'},
    9.0: False,
    False: True,
    'x': DateTime.DateTime(2022, 4, 1),
    'y': '10:32'
}

vcard_data = {
    'prename': 'Georg',
    'surname': 'Tester',
    'email': 'georg.tester@test.at',
    'phone': '+43 699 123123123',
    'street': 'Teststraße 34',
    'city': 'Völkermarkt',
    'zipcode': '4321',
    'country': 'Österreich',
    'note': 'Eine hinzugefügte Notiz: Mit colon!'
}

sample_vcard = """BEGIN:VCARD
VERSION:3.0
ADR;TYPE=HOME,pref:;;Teststraße 34;Völkermarkt;;4321;Österreich
EMAIL;TYPE=INTERNET:georg.tester@test.at
FN:Georg Tester
N:Tester;Georg;;;
NOTE:Eine hinzugefügte Notiz: Mit colon!
TEL;TYPE=CELL,VOICE:+43 699 123123123
END:VCARD
"""


class TestData(unittest.TestCase):
    def test_any_2boolean(self):
        for a, b in test_boolean.items():
            self.assertEqual(
                b,
                any_2boolean(value=a)
            )

    def test_dict_from_dict_list(self):
        kwargs_list = [
            {
                'dict_list': dict_list,
                'key': 'a',
                'single_value': None,
                'include_key': False
            },
            {
                'dict_list': dict_list,
                'key': 'a',
                'single_value': None,
                'include_key': True
            },
            {
                'dict_list': dict_list,
                'key': 'a',
                'single_value': 'b'
            },
            {
                'dict_list': dict_list,
                'key': 'a',
                'single_value': 'c',
                'include_key': True
            }
        ]

        for i, kwargs in enumerate(kwargs_list):
            a_dict = dict_from_dict_list(**kwargs)

            return_type = dict_from_dict_list.__annotations__['return']
            self.assertEqual(
                return_type,
                type(a_dict)
            )
            self.assertEqual(
                a_dict,
                dicts_from_dict_list[i]
            )
            for v in a_dict.values():
                if not kwargs.get('single_value'):  # with single value we don't know the type
                    self.assertEqual(
                        type(v),
                        dict
                    )

    def test_dict_2unicode(self):
        unicoded_dict = dict_2unicode(dict_for_testing)
        self.assertEqual(
            unicoded_dict,
            dict_for_testing_unicoded
        )

    def test_dict_2datatypes(self):
        # using json data is not tested yet
        # print('test_dict_2datatypes')
        # print(f'{dict_for_testing           = }')

        datatyped_dict = dict_2datatypes(
            d=dict_for_testing,
            convert_keys=True,
            dt='datetime'
        )

        # print(f'{datatyped_dict             = }')
        # print(f'{dict_for_testing_datatyped = }')
        self.assertEqual(
            datatyped_dict,
            dict_for_testing_datatyped
        )

        datatyped_dict = dict_2datatypes(
            d=dict_for_testing,
            metadata={
                'x': 'date',
                'y': 'time'
            },
            convert_keys=True,
            dt='datetime'
        )

        # print(f'{datatyped_dict             = }')
        # print(f'{dict_for_testing_datatyped = }')
        self.assertEqual(
            datatyped_dict,
            dict_for_testing_datatyped
        )

        datatyped_dict_unicoded = dict_2datatypes(
            d=dict_for_testing,
            convert_keys=True,
            convert_to_unicode=True,
            dt='DateTime')
        self.assertEqual(
            datatyped_dict_unicoded,
            dict_for_testing_datatyped_unicoded
        )

    def test_value_2datatype(self):
        pass  # this is already tested extensively in test_dict_2datatypes

    def test_sort_dictlist(self):
        sorted_dict_list = sort_dictlist(
            dictlist=dict_list,
            keys='c'
        )
        self.assertEqual(
            sorted_dict_list,
            dict_list_sorted_by_c
        )
        sorted_dict_list = sort_dictlist(
            dictlist=dict_list,
            keys=['c', 'a']
        )
        self.assertEqual(
            sorted_dict_list,
            dict_list_sorted_by_c
        )

    # @todo: - multiple values for email, phone and address
    #        - different types for email, phone and address
    #        - test invalid phone numbers
    def test_create_vcard(self):
        vcard = create_vcard(
            vcard_data,
            returning='pretty'
        )
        vcard = create_vcard(
            vcard_data
        ).replace('\r\n', '\n')  # remove Windows line breaks
        self.assertEqual(
            vcard,
            sample_vcard
        )

    def test_dictlist_2datatypes(self):
        dictlist_for_testing = [
            dict_for_testing,
            dict_for_testing,
            dict_for_testing
        ]
        dictlist_datatyped = [
            dict_for_testing_datatyped_unicoded,
            dict_for_testing_datatyped_unicoded,
            dict_for_testing_datatyped_unicoded
        ]

        dictlist_tested_datatyped = dictlist_2datatypes(
            dictlist=dictlist_for_testing,
            convert_keys=True,
            convert_to_unicode=True,
            dt='DateTime'
        )

        # print(f'{dictlist_datatyped=}')
        # print(f'{dictlist_tested_datatyped=}')

        self.assertEqual(
            dictlist_datatyped,
            dictlist_tested_datatyped
        )


if __name__ == '__main__':
    unittest.main()

    # print('finished format tests.')
