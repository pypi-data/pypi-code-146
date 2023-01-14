from typing import Any, Dict


def dict_to_model(model: Any, dictionary: Dict[str, Any]):
    """
    Converts a dictionary to an OpenAPI model.

    Args:
        model (Any): The model to convert.
        dictionary (dict): A dictionary to convert.

    Returns:
        Model: The Generic Model
    """
    result = {}
    attribute_map: Dict[str, str] = dict((v, k) for k, v in model.attribute_map.items())
    for key, value in dictionary.items():
        try:
            result[attribute_map[key]] = value
        except KeyError:
            pass

    return model(**result)
