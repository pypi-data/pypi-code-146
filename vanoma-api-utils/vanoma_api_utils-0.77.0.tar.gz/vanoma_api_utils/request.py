from typing import Any, Dict
from djangorestframework_camel_case.util import camelize  # type: ignore


def stringify_filters(filters: Dict[str, Any]) -> str:
    return "&".join(map(lambda item: f"{item[0]}={item[1]}", camelize(filters).items()))
