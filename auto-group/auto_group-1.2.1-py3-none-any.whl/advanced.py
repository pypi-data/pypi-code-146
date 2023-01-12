import re


def auto_group_list_into_tree_dict(tree_key_names: tuple, list_of_dicts: list[dict], include_key_names: bool = False) -> dict:
    """
    Group items based on values of given key names into dict tree structure recursively.
    Example: tree_key_names=("a", "b"), list_of_dicts=input1 = [
                {"a": "aa1", "b": "bb1", "c": 3, "d": 4},
                {"a": "aa1", "b": "bb2", "c": 33, "d": 44},
                {"a": "aa2", "b": "bb1", "c": 333, "d": 444},
                {"a": "aa2", "b": "bb2", "c": 3333, "d": 4444}
            ]
                ==>
            {
                'aa1': {
                            'bb1': [{'a': 'aa1', 'b': 'bb1', 'c': 3, 'd': 4}],
                            'bb2': [{'a': 'aa1', 'b': 'bb2', 'c': 33, 'd': 44}]
                },
                'aa2': {
                            'bb1': [{'a': 'aa2', 'b': 'bb1', 'c': 333, 'd': 444}],
                            'bb2': [{'a': 'aa2', 'b': 'bb2', 'c': 3333, 'd': 4444}]
                }
            }

    :param tree_key_names: Key names to create tree structure
    :param list_of_dicts: List of dicts to be transformed into tree
    :param include_key_names: Concat key name into key identifier separated by "|" char
    """
    def __get(dict_, key_value_):
        if isinstance(dict_.get(key_value_), list):
            return dict_[key_value_]
        dict_[key_value_] = []
        return dict_[key_value_]

    if not tree_key_names:
        return list_of_dicts

    result = {}
    key_name = tree_key_names[0]

    for item in list_of_dicts:
        result_key = "{}|{}".format(key_name, item.get(key_name)) if include_key_names else str(item.get(key_name))
        __get(result, result_key).append(item)

    if tree_key_names[1:]:
        for result_key, result_item in result.items():
            result[result_key] = auto_group_list_into_tree_dict(tree_key_names[1:], result_item, include_key_names)

    return result


def auto_group_list_into_tree_list(tree_key_names: tuple, list_of_dicts: list[dict]) -> list:
    """
    Group items based on values of given key names into list tree structure recursively.

        input1 = [
                        {"a": "aa1", "b": "bb1", "c": 3, "d": 4},
                        {"a": "aa1", "b": "bb2", "c": 33, "d": 44},
                        {"a": "aa2", "b": "bb1", "c": 333, "d": 444},
                        {"a": "aa2", "b": "bb2", "c": 3333, "d": 4444}
        ]

    ==>
        [
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
    :param tree_key_names: Key names to create tree structure. By adding +/- at the end of key name order of items (ASC or DESC) could be driven.
    :param list_of_dicts: List of dicts to be transformed into tree
    """
    def __get(items_, key_, key_value_):
        for item_ in items_:
            if item_.get(key_) == key_value_:
                return item_["items"]
        items_.append({
            key_: key_value_,
            "items": [],
        })
        return items_[-1]["items"]

    if not tree_key_names:
        return list_of_dicts

    result = []
    key_name = tree_key_names[0]
    sort_order = None
    sort_order_match = re.match(r".*[+-]$", key_name)
    if sort_order_match:
        sort_order = key_name[-1]
        key_name = key_name[:-1]

    for item in list_of_dicts:
        result_key = item.get(key_name)
        __get(result, key_name, result_key).append(item)

    if tree_key_names[1:]:
        for result_index, result_item in enumerate(result):
            result[result_index]["items"] = auto_group_list_into_tree_list(tree_key_names[1:], result_item["items"])

        if sort_order:
            result = sorted(result, key=lambda item_: item_[key_name], reverse=(sort_order == "-"))

    return result
