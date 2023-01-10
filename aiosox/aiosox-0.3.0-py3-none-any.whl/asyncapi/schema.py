from typing import Any, Dict, List, Optional, Set, Union

from pydantic import Extra, Field, root_validator, validator

from aiosox.utils import BaseModel

from .enums import (
    JSONReference,
)

SPECIAL_PATH_FORMAT: str = "#-special-path-#-{}-#-special-#"


class JsonSchemaObject(BaseModel):
    __constraint_fields__: Set[str] = {
        "exclusiveMinimum",
        "minimum",
        "exclusiveMaximum",
        "maximum",
        "multipleOf",
        "minItems",
        "maxItems",
        "minLength",
        "maxLength",
        "pattern",
    }
    # __extra_key__: str = SPECIAL_PATH_FORMAT.format("extras")

    @root_validator(pre=True)
    def validate_exclusive_maximum_and_exclusive_minimum(cls, values: Dict[str, Any]) -> Any:
        exclusive_maximum: Union[float, bool, None] = values.get("exclusiveMaximum")
        exclusive_minimum: Union[float, bool, None] = values.get("exclusiveMinimum")

        if exclusive_maximum is True:
            values["exclusiveMaximum"] = values["maximum"]
            del values["maximum"]
        elif exclusive_maximum is False:
            del values["exclusiveMaximum"]
        if exclusive_minimum is True:
            values["exclusiveMinimum"] = values["minimum"]
            del values["minimum"]
        elif exclusive_minimum is False:
            del values["exclusiveMinimum"]
        return values

    @validator("ref")
    def validate_ref(cls, value: Any) -> Any:
        if isinstance(value, str) and "#" in value:
            if value.endswith("#/"):
                return value[:-1]
            elif "#/" in value or value[0] == "#" or value[-1] == "#":
                return value
            return value.replace("#", "#/")
        return value

    items: Union[List["JsonSchemaObject"], "JsonSchemaObject", None] = None
    # uniqueItem: Optional[bool]
    type: Union[str, List[str], None] = None
    format: Optional[str] = None
    # pattern: Optional[str]
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    minItems: Optional[int] = None
    maxItems: Optional[int] = None
    # multipleOf: Optional[float]
    # exclusiveMaximum: Union[float, bool, None]
    # exclusiveMinimum: Union[float, bool, None]
    additionalProperties: Union["JsonSchemaObject", bool, None] = None
    # patternProperties: Optional[Dict[str, "JsonSchemaObject"]]
    oneOf: Optional[List["JsonSchemaObject"]] = None
    anyOf: Optional[List["JsonSchemaObject"]] = None
    allOf: Optional[List["JsonSchemaObject"]] = None
    enum: Optional[List[Any]] = None
    # writeOnly: Optional[bool]
    properties: Optional[Dict[str, "JsonSchemaObject"]] = None
    required: List[str] = []
    ref: Optional[str] = Field(default=None, alias="$ref")
    nullable: Optional[bool] = False
    # x_enum_varnames: List[str] = Field(default=[], alias="x-enum-varnames")
    description: Optional[str] = None
    title: Optional[str] = None
    example: Any
    examples: Any
    default: Optional[Any] = None
    id: Optional[str] = Field(default=None, alias="$id")
    custom_type_path: Optional[str] = Field(default=None, alias="customTypePath")

    extras: Dict[str, Any] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data: Any) -> None:  # type: ignore
        super().__init__(**data)
        self.extras = {k: v for k, v in data.items() if k not in EXCLUDE_FIELD_KEYS}

    def is_object(self) -> bool:
        return (
            self.properties is not None
            or self.type == "object"
            and not self.allOf
            and not self.oneOf
            and not self.anyOf
            and not self.ref
        )

    def is_array(self) -> bool:
        return self.items is not None or self.type == "array"

    def ref_object_name(self) -> str:  # pragma: no cover
        return self.ref.rsplit("/", 1)[-1]  # type: ignore

    @validator("items", pre=True)
    def validate_items(cls, values: Any) -> Any:
        # this condition expects empty dict
        return values or None

    def has_default(self) -> bool:
        return "default" in self.__fields_set__

    def has_constraint(self) -> bool:
        return bool(self.__constraint_fields__ & self.__fields_set__)

    def ref_type(self) -> Optional[JSONReference]:
        if self.ref:
            return JSONReference(self.ref)
        return None  # pragma: no cover


class ApiSchema(JsonSchemaObject):

    discriminator: Optional[str] = None

    class Config:
        extra = Extra.forbid


DEFAULT_FIELD_KEYS: Set[str] = {
    "example",
    "examples",
    "description",
    "title",
}

EXCLUDE_FIELD_KEYS = (set(JsonSchemaObject.__fields__) - DEFAULT_FIELD_KEYS) | {
    "$id",
    "$ref",
    # JsonSchemaObject.__extra_key__,
}
