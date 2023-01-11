# coding=utf-8
"""
run the test from the sr/invesytoolbox directory:
python ../tests/test_text_name.py
"""

import sys
import unittest
import random

sys.path.append(".")

from itb_text_name import \
    and_list, \
    capitalize_name, \
    get_gender, \
    leet, \
    normalize_name, \
    sort_names, \
    could_be_a_name

reference_names = {
    'Georg Pfolz': {
        'lowercase': 'georg pfolz',
        'capitalized': 'Georg Pfolz',
        'gender': 'male',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Georg',
            'middle': '',
            'last': 'Pfolz',
            'suffix': '',
            'nickname': ''
        }
    },
    'Patrizia Höfstädter': {
        'lowercase': 'patrizia höfstädter',
        'capitalized': 'Patrizia Höfstädter',
        'gender': 'female',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Patrizia',
            'middle': '',
            'last': 'Höfstädter',
            'suffix': '',
            'nickname': ''
        }
    },
    'Eugénie Caraçon': {
        'lowercase': 'eugénie caraçon',
        'capitalized': 'Eugénie Caraçon',
        'gender': 'female',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Eugénie',
            'middle': '',
            'last': 'Caraçon',
            'suffix': '',
            'nickname': ''
        }
    },
    'Joanna MacArthur': {
        'lowercase': 'joanna macarthur',
        'capitalized': 'Joanna MacArthur',
        'gender': 'female',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Joanna',
            'middle': '',
            'last': 'MacArthur',
            'suffix': '',
            'nickname': ''
        }
    },
    'Sandra de Vitt': {
        'lowercase': 'sandra de vitt',
        'capitalized': 'Sandra de Vitt',
        'gender': 'female',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Sandra',
            'middle': '',
            'last': 'de Vitt',
            'suffix': '',
            'nickname': ''
        }
    },
    'Bea-Regina Obersteigen': {
        'lowercase': 'bea-regina obersteigen',
        'capitalized': 'Bea-Regina Obersteigen',
        'gender': 'female',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Bea-Regina',
            'middle': '',
            'last': 'Obersteigen',
            'suffix': '',
            'nickname': ''
        }
    },
    'Roland Meier-Lansky': {
        'lowercase': 'roland meier-lansky',
        'capitalized': 'Roland Meier-Lansky',
        'gender': 'male',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Roland',
            'middle': '',
            'last': 'Meier-Lansky',
            'suffix': '',
            'nickname': ''
        }
    },
    'Bogumila Österreicher': {
        'lowercase': 'bogumila österreicher',
        'capitalized': 'Bogumila Österreicher',
        'gender': 'unknown',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Bogumila',
            'middle': '',
            'last': 'Österreicher',
            'suffix': '',
            'nickname': ''
        }
    },
    'Rafael': {
        'lowercase': 'rafael',
        'capitalized': 'Rafael',
        'gender': 'male',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Rafael',
            'middle': '',
            'last': '',
            'suffix': '',
            'nickname': ''
        }
    },
    'Maria Helena Blawatsky': {
        'lowercase': 'maria helena blawatsky',
        'capitalized': 'Maria Helena Blawatsky',
        'gender': 'female',
        'is_a_name': True,
        'human_name': {
            'title': '',
            'first': 'Maria',
            'middle': 'Helena',
            'last': 'Blawatsky',
            'suffix': '',
            'nickname': ''
        }
    },
    'DsZHkfNijWFPrET JGLAjuaqZ': {
        'lowercase': 'dszhkfnijwfpret jglajuaqz',
        'capitalized': 'Dszhkfnijwfpret Jglajuaqz',
        'gender': 'unknown',
        'is_a_name': False,
        'human_name': {
            'title': '',
            'first': 'DsZHkfNijWFPrET',
            'middle': '',
            'last': 'JGLAjuaqZ',
            'suffix': '',
            'nickname': ''
        }
    }
}

reference_names_sorted = [
    'Maria Helena Blawatsky',
    'Eugénie Caraçon',
    'Patrizia Höfstädter',
    'DsZHkfNijWFPrET JGLAjuaqZ',
    'Joanna MacArthur',
    'Roland Meier-Lansky',
    'Bea-Regina Obersteigen',
    'Bogumila Österreicher',
    'Georg Pfolz',
    'Rafael',
    'Sandra de Vitt'
]

lower_text = 'das ist ein Beispiel-Text, der kapitalisiert werden kann.'


class TestTextName(unittest.TestCase):
    def test_and_list(self):
        a_list = [1, 'Georg', 'Haus', True]
        correct_str = '1, Georg, Haus and True'

        and_str = and_list(a_list)

        self.assertEqual(
            and_str,
            correct_str
        )

    def test_leet(self):
        for _ in range(3):
            string_to_leet = random.choice(list(reference_names))
            max_length = random.randint(6, 12)
            start_at_begin = random.randint(0, 1)

            print(f'{string_to_leet} --> {leet(string_to_leet)}')
            leeted_text = leet(
                text=string_to_leet,
                max_length=max_length,
                start_at_begin=start_at_begin
            )
            print(
                f'{string_to_leet}, {max_length = }  {start_at_begin = } --> {leeted_text}'
            )

        # because of the use of random, using Asserts does not make any sense here

    def test_capitalize_name(self):
        for name_dict in reference_names.values():
            capitalized_name = capitalize_name(
                text=name_dict.get('lowercase')
            )
            self.assertEqual(
                name_dict.get('capitalized'),
                capitalized_name
            )

    def test_get_gender(self):
        for name, name_dict in reference_names.items():
            correct_gender = name_dict.get('gender')
            gender = get_gender(name.split()[0])  # prename

            try:
                self.assertEqual(
                    gender,
                    correct_gender
                )
            except AssertionError:
                msg = f'{gender} != {correct_gender} for {name}'
                raise AssertionError(msg)

    def test_normalize_name(self):
        for name, name_dict in reference_names.items():
            normalized_name = normalize_name(
                name=name
            )
            self.assertEqual(
                name,
                normalized_name
            )

            name_data = normalize_name(
                name=name,
                returning='dict'
            )
            self.assertEqual(
                name_dict.get('human_name'),
                name_data
            )

    def test_sort_names(self):
        names_list = list(reference_names)
        sorted_names = sort_names(names=names_list)

        self.assertEqual(
            sorted_names,
            reference_names_sorted
        )

    def test_could_be_a_name(self):
        for name, vals in reference_names.items():
            kwargs = {'name': name}

            if not ' ' in name:
                kwargs['prename'] = True

            self.assertEqual(
                could_be_a_name(**kwargs),
                vals.get('is_a_name')
            )


if __name__ == '__main__':
    unittest.main()
