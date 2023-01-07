from natsort import natsorted


def sorted_dict(dic: dict, for_key_not_value: bool = False):
    if for_key_not_value:
        dic_sorted = {k: v for k, v in natsorted(dic.items(), key=lambda item: item[0])}
    else:
        dic_sorted = {k: v for k, v in natsorted(dic.items(), key=lambda item: item[1])}
    return dic_sorted
