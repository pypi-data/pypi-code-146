from dataclasses import dataclass
from typing import Optional, List


@dataclass
class FieldSpec:
    name: str
    pk: bool
    auto: bool
    nullable: bool
    fk: bool
    fk_table: Optional[str]
    fk_schema: Optional[str]
    fk_column: Optional[str]
    dtype: str
    dtype_spec: dict


@dataclass
class TableSpec:
    table: str
    pk: Optional[str]
    schema: str
    fields: List[FieldSpec]
