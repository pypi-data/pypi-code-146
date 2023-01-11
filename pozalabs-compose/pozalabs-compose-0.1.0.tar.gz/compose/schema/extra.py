from typing import Any, Callable, Type

from pydantic import BaseModel as PydanticBaseModel

SchemaExtraCallable = Callable[[dict[str, Any], Type[PydanticBaseModel]], None]


def schema_excludes(*excludes: str) -> SchemaExtraCallable:
    """OpenAPI 문서에서 특정 필드를 제외합니다. 외부에 노출하지 않아도 되는 필드를 문서에서 제외할 때 사용합니다."""

    def wrapper(schema: dict[str, Any], model_class: Type[PydanticBaseModel]) -> None:
        for exclude in excludes:
            schema.get("properties", {}).pop(exclude)

    return wrapper


def schema_by_field_name() -> SchemaExtraCallable:
    """OpenAPI 문서에서 스키마의 필드명을 `field.alias`가 아닌 원래의 필드명으로 표시합니다.
    FastAPI는 `field.alias`를 기본 필드명으로 사용하므로 스키마를 순회하며 스키마 필드명을 원 필드명으로 수정합니다.

    References:
        https://github.com/tiangolo/fastapi/issues/1810#issuecomment-895126406
    """

    def wrapper(schema: dict[str, Any], model_class: Type[PydanticBaseModel]) -> None:
        updated = dict()
        for field in model_class.__fields__.values():
            field_name = field.name
            alias = field.alias or field_name
            prop = schema.get("properties", {}).get(alias)
            updated[field_name] = prop

        schema.update({"properties": updated})

    return wrapper
