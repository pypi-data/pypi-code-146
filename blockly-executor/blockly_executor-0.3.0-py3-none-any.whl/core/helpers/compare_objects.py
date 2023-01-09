__author__ = 'ma.razgovorov'

from copy import deepcopy
from blockly_executor.helper import obj_get_path_value


def compare_objects(fist_object, second_object, compare_params):
    props = compare_params.get('PROPS')
    delimiter = '.'
    result_difference = ''
    if props:
        obj1_props = get_compare_object(fist_object, props, delimiter=delimiter)
        obj2_props = get_compare_object(second_object, props, delimiter=delimiter)
        difference, delta = compare(obj1_props, obj2_props)
        if difference:
            result_difference += _difference_string(delta)

    compare_table_index = 0
    while True:
        compare_table_path = compare_params.get(f'TABLE{compare_table_index}_NAME')
        if not compare_table_path:
            break
        group = compare_params.get(f'TABLE{compare_table_index}_GROUP')
        fields = compare_params.get(f'TABLE{compare_table_index}_FIELDS')
        table1 = obj_get_path_value(fist_object, compare_table_path)
        table2 = obj_get_path_value(second_object, compare_table_path)
        obj1_props = index_list(table1, group, fields, delimiter=delimiter)
        obj2_props = index_list(table2, group, fields, delimiter=delimiter)
        difference, delta = compare(obj1_props, obj2_props)
        if difference:
            result_difference += _difference_string(delta, compare_table_path)
        compare_table_index += 1

    return result_difference


def compare(base, new):
    if isinstance(base, dict):
        difference = False
        res = {}
        if new:
            for elem in new:
                try:
                    if base and elem in base:
                        if isinstance(new[elem], dict):
                            _difference, _res = compare(base[elem], new[elem])
                            if _difference:
                                difference = True
                                res[elem] = deepcopy(_res)
                        else:
                            if new[elem] != base[elem]:
                                difference = True
                                res[elem] = new[elem]
                    else:
                        difference = True
                        res[elem] = new[elem]
                except Exception as e:
                    raise Exception('compare: {0}'.format(str(e)), elem)
        else:
            if base != new:
                difference = True
                res = base
    else:
        difference = False
        res = None
        if base != new:
            difference = True
            res = new
    return difference, res


def _difference_string(_delta, _prefix=None):
    result = ''
    if _prefix:
        result += f'{_prefix}: '
    for key in _delta:
        result += f'{key}, '
    return f'{result[:-2]}; '


def get_compare_object(obj, keys, **kwargs):
    compare_obj = {}
    for key in keys:
        compare_obj[key] = obj_get_path_value(obj, key, **kwargs)
    return compare_obj


def index_list(items, group, fields, **kwargs):
    compare_obj = {}
    if items:
        for item in items:
            uid = ''
            for key in group:
                uid += f'{obj_get_path_value(item, key, default="-", **kwargs)}_'
            if uid not in compare_obj:
                compare_obj[uid] = {}
            for key in fields:
                value = obj_get_path_value(item, key, **kwargs)
                if isinstance(value, (int, float)):
                    if key not in compare_obj[uid]:
                        compare_obj[uid][key] = 0
                    compare_obj[uid][key] += value
                else:
                    compare_obj[uid][key] = value
    return compare_obj
