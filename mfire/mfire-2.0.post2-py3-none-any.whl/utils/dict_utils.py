import sys
from typing import Any, Union, Dict
from collections import UserDict


class FormatDict(UserDict):
    """FormatDict: dictionnary extension for handling string formatting
    with missing keys. For instance :
    >>> dico = {"key1" : "value1"}
    >>> "la valeur 1 = {key1}, la valeur 2 = {key2}".format_map(dico)
    ...
    KeyError: "value2" missing
    >>> dico = FormatDict(dico)
    >>> dico
    {"key1" : "value1"}
    >>> "la valeur 1 = {key1}, la valeur 2 = {key2}".format_map(dico)
    "la valeur 1 = value1, la valeur 2 = {key2}"

    Inheritance:
        UserDict
    """

    def __missing__(self, key: Any) -> str:
        return f"{{{key}}}"


def recursive_format(
    obj: Union[dict, list, str],
    values: Dict[str, str],
) -> Union[dict, list, str]:
    """Function that recursively formats str values within a dict or a list.

    >>> dico = {
        "id": "{nom}_{prenom}",
        "nom": "{nom}",
        "prenoms": ["{prenom}"],
        "intro": "Bonjour, je suis {prenom} {nom}, j'ai {age} ans.",
    }
    >>>  values = {
        "nom": "La Blague",
        "prenom": "Toto",
        "age": 8,
    }
    >>> fill_values(dico, values)
    {'id': 'La Blague_Toto',
    'nom': 'La Blague',
    'prenoms': ['Toto'],
    'intro': "Bonjour, je suis Toto La Blague, j'ai 8 ans."}

    Args:
        obj (Union[dict, list, str]): Object containing values to format.
        values (Dict[str, str]): Mapping of values to format.

    Returns:
        Union[dict, list, str]: Given obj with formatted values.
    """
    if isinstance(obj, str) and "{" in obj and "}" in obj:
        return obj.format_map(FormatDict(values))
    if isinstance(obj, list):
        return [recursive_format(o, values) for o in obj]
    if isinstance(obj, dict):
        return {key: recursive_format(val, values) for key, val in obj.items()}
    return obj


def dict_diff(
    left: Any,
    right: Any,
    index_list: str = "",
    verbose: int = 2,
    **kwargs,
) -> bool:
    """Recursive function made to check the difference between two given values
    and to highlight the differences.

    Args:
        left (Any): Value 1
        right (Any): Value 2
        index_list (str, optional): Inde. Defaults to "".
        verbose (int, optional): Level of description of the differences..
            Defaults to 2.

    Returns:
        bool: True if left and right are equal, else False
    """

    def log(msg: str) -> None:
        header = f"{index_list}\t: " if index_list else ""
        if verbose:
            channel = sys.stdout if verbose == 1 else sys.stderr
            print(f"{header}{msg}", file=channel)

    if not isinstance(left, type(right)):
        log(f"type mismatch ('{type(left)}' | '{type(right)}')")
        return False

    if isinstance(left, dict):
        keysl = set(left)
        keysr = set(right)
        results = []
        if keysl - keysr:
            log(f"missing keys in right dict {keysl - keysr}")
            results += [False]
        if keysr - keysl:
            log(f"missing keys in left dict {keysr - keysl}")
            results += [False]
        for key in keysl & keysr:
            results += [
                dict_diff(
                    left=left[key],
                    right=right[key],
                    index_list=index_list + f"['{key}']",
                    verbose=verbose,
                    **kwargs,
                )
            ]
        return all(results)

    if isinstance(left, list):
        len_left = len(left)
        len_right = len(right)
        if len_left != len_right:
            log(f"lengths of iterables don't match ({len_left} | {len_right})")
            return False

        if len_left > 0 and all([isinstance(d, dict) for d in left]):
            sorting_key = next(
                (key for key in ("hazard", "level") if key in left[0]), None
            )
            if sorting_key is not None:
                sorted_left = sorted(left, key=lambda d: d[sorting_key])
                sorted_right = sorted(right, key=lambda d: d[sorting_key])
                return all(
                    [
                        dict_diff(
                            left=sorted_left[i],
                            right=sorted_right[i],
                            index_list=index_list
                            + f"[{sorting_key}={sorted_left[i][sorting_key]}]",
                            verbose=verbose,
                            **kwargs,
                        )
                        for i in range(len_left)
                    ]
                )

        return all(
            [
                dict_diff(
                    left=left[i],
                    right=right[i],
                    index_list=index_list + f"[{i}]",
                    verbose=verbose,
                    **kwargs,
                )
                for i in range(len_left)
            ]
        )

    if isinstance(left, str):
        if left == right:
            return True
        if kwargs is None:
            log(f"str values don't match ('{left}' | '{right}')")
            return False
        format_kwargs = FormatDict(kwargs)
        formatted_left = left.format_map(format_kwargs)
        formatted_right = right.format_map(format_kwargs)
        if formatted_left != formatted_right:
            log(
                "formatted str values don't match "
                f"('{formatted_left}' | '{formatted_right}')"
            )
            return False
        return True

    if left != right:
        log(f"values don't match ('{left}' | '{right}')")
        return False

    return True
