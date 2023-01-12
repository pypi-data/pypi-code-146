from auto_group.tools import sort_list_of_dicts

example1 = [
    {"id": 4, "name": "AAA"},
    {"id": 3, "name": "BBB"},
    {"id": 2, "name": "CCC"},
    {"id": 1, "name": "DDD"},
]
example2 = [
    {"id": 1, "name": "DDD"},
    {"id": 2, "name": "CCC"},
    {"id": 3, "name": "BBB"},
    {"id": 4, "name": "AAA"},
]


def test_sort_list_of_dicts():
    assert sort_list_of_dicts(example1, "id+") == example2
    assert sort_list_of_dicts(example1, "name+") == example1
    assert sort_list_of_dicts(example1, "id-") == example1
    assert sort_list_of_dicts(example1, "name-") == example2
