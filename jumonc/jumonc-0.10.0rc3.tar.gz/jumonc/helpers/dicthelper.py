from typing import Dict
from typing import Union


def mergeDictionaryAndAdd(dict_1: Union[str, Dict[str, Union[int, float, str]]],
                          dict_2: Union[str, Dict[str, Union[int, float, str]]]
                         ) -> Union[str, Dict[str, Union[int, float, str]]]:
    if not isinstance(dict_1, str)and  not isinstance(dict_2, str):
        dict_3 = {**dict_1, **dict_2}
        for key, value in dict_1.items():
            if key in dict_2:
                second_value = dict_2[key]
                if not isinstance(value, str)and  not isinstance(second_value, str):
                    dict_3[key] = value + second_value
        return dict_3
    return {}
