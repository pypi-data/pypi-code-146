from auto_group.advanced import auto_group_list_into_tree_dict
from auto_group.advanced import auto_group_list_into_tree_list


input1 = [
                {"a": "aa1", "b": "bb1", "c": 3, "d": 4},
                {"a": "aa1", "b": "bb2", "c": 33, "d": 44},
                {"a": "aa2", "b": "bb1", "c": 333, "d": 444},
                {"a": "aa2", "b": "bb2", "c": 3333, "d": 4444}
]

expected_dict1 = {
    'aa1': {
                'bb1': [{'a': 'aa1', 'b': 'bb1', 'c': 3, 'd': 4}],
                'bb2': [{'a': 'aa1', 'b': 'bb2', 'c': 33, 'd': 44}]
    },
    'aa2': {
                'bb1': [{'a': 'aa2', 'b': 'bb1', 'c': 333, 'd': 444}],
                'bb2': [{'a': 'aa2', 'b': 'bb2', 'c': 3333, 'd': 4444}]
    }
}

expected_dict2 = {
    'a|aa1': {
                'b|bb1': [{'a': 'aa1', 'b': 'bb1', 'c': 3, 'd': 4}],
                'b|bb2': [{'a': 'aa1', 'b': 'bb2', 'c': 33, 'd': 44}]
    },
    'a|aa2': {
                'b|bb1': [{'a': 'aa2', 'b': 'bb1', 'c': 333, 'd': 444}],
                'b|bb2': [{'a': 'aa2', 'b': 'bb2', 'c': 3333, 'd': 4444}]
    }
}


expected_list1 = [
    {'a': 'aa1', 'items': [
        {'b': 'bb1', 'items': [
            {'a': 'aa1', 'b': 'bb1', 'c': 3, 'd': 4}
        ]},
        {'b': 'bb2', 'items': [
            {'a': 'aa1', 'b': 'bb2', 'c': 33, 'd': 44}]}]
     },
    {'a': 'aa2', 'items': [
        {'b': 'bb1', 'items': [
            {'a': 'aa2', 'b': 'bb1', 'c': 333, 'd': 444}
        ]},
        {'b': 'bb2', 'items': [
            {'a': 'aa2', 'b': 'bb2', 'c': 3333, 'd': 4444}]
         }]
     }
]


def test_auto_group_list_into_tree_dict():
    assert auto_group_list_into_tree_dict(("a", "b"), input1) == expected_dict1
    assert auto_group_list_into_tree_dict(("a", "b"), input1, include_key_names=True) == expected_dict2


def test_auto_group_list_into_tree_list():
    assert auto_group_list_into_tree_list(("a", "b"), input1) == expected_list1
