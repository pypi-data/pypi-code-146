import re


def sort_list_of_dicts(list_of_dicts: list[dict], sort_by: str) -> list[dict]:
    """
    Sort list of dicts by selected column
    :param list_of_dicts: Input dict
    :param sort_by: Column name. To change direction of sort add +/- at the end of column name. Example: "id-"
    """
    sort_direction = "+"
    sort_order_match = re.match(r".*[+-]$", sort_by)
    if sort_order_match:
        sort_direction = sort_by[-1]
        sort_by = sort_by[:-1]
    result_list = sorted(list_of_dicts, key=lambda item_: item_[sort_by], reverse=(sort_direction == "-"))
    return result_list


def dict_filter(d: dict, attributes: list) -> dict:
    """
    Whitelist dictionary attributes
    :param d: Dict instance
    :param attributes: Whitelist
    :return: Filtered dict
    """
    return {key: value for key, value in d.items() if key in attributes}
