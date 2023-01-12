from typing import Optional, Any, Type
from pydantic import BaseModel, BaseConfig, Field
from pydantic.fields import ModelField
from sqlalchemy import (
    Column,
    Table,
    Integer,
    Float,
    Boolean,
    String,
    JSON,
    PrimaryKeyConstraint,
)

__isbool = lambda __o: isinstance(__o, bool)
istrue = lambda __o: __isbool(__o) and __o == True
isfalse = lambda __o: __isbool(__o) and __o == False


class SQLAlchemyColumnInit(BaseModel):
    class Config(BaseConfig):

        arbitrary_types_allowed = True

    name: Optional[str] = Field(default=None)
    type: Optional[Type] = Field(default=None)
    autoincrement: Optional[Any] = Field(default=None)
    default: Optional[Any] = Field(default=None)
    doc: Optional[str] = Field(default=None)
    key: Optional[str] = Field(default=None)
    index: Optional[bool] = Field(default=None)
    info: Optional[dict] = Field(default=None)
    nullable: Optional[bool] = Field(default=None)
    onupdate: Optional[Any] = Field(default=None)
    primary_key: Optional[bool] = Field(default=None)
    server_default: Optional[Any] = Field(default=None)
    server_onupdate: Optional[Any] = Field(default=None)
    quote: Optional[Any] = Field(default=None)
    unique: Optional[bool] = Field(default=None)
    system: Optional[bool] = Field(default=None)
    comment: Optional[str] = Field(default=None)

    @property
    def is_primarykey(self) -> bool:
        return (
            isfalse(self.nullable)
            and istrue(self.unique)
            and istrue(self.autoincrement)
        )


class SQLAlchemyTypeInit(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    python: Optional[Type] = Field(default=None)
    sqlalchemy: Optional[Type] = Field(default=None)

    @property
    def python_typename(self) -> str:
        return self.python.__name__

    @property
    def sqlalchemy_typename(self) -> str:
        return self.sqlalchemy.__name__


class __TypeTable(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    python_type: Optional[Type] = Field(default=None)
    sqlalchemy_type: Optional[Type] = Field(default=None)

    @property
    def python_typename(self) -> str:
        return self.python_type.__name__

    @property
    def sqlalchemy_typename(self) -> str:
        return self.sqlalchemy_type.__name__


__TYPE_TABLES__ = [
    __TypeTable(python_type=python_type, sqlalchemy_type=sqlalchemy_type)
    for (python_type, sqlalchemy_type) in (
        (int, Integer),
        (str, String),
        (float, Float),
        (bool, Boolean),
    )
]


def __python_to_alchemy(__type: Type):
    return {
        typetable.python_typename: typetable.sqlalchemy_type
        for typetable in __TYPE_TABLES__
    }.get(__type.__name__, JSON)


def __alchemy_to_python(__type: Type):
    return {
        typetable.sqlalchemy_typename: typetable.python_type
        for typetable in __TYPE_TABLES__
    }.get(__type.__name__, dict)


def __typeinit(
    python_type: Optional[Type] = None, sqlalchemy_type: Optional[Type] = None
):
    if python_type is not None:
        if sqlalchemy_type is None:
            sqlalchemy_type = __python_to_alchemy(python_type)
    elif sqlalchemy_type is not None:
        if python_type is None:
            python_type = __alchemy_to_python(sqlalchemy_type)
    return SQLAlchemyTypeInit(python=python_type, sqlalchemy=sqlalchemy_type)


def __field_to_columninit(__field: ModelField):
    name = __field.name
    python_type = __field.type_
    typemap = __typeinit(python_type=python_type)
    result = SQLAlchemyColumnInit(name=name, type=typemap.sqlalchemy)
    if name == "id" and typemap.python_typename == "int":
        result.autoincrement = True
        result.nullable = False
        result.unique = True
    return result


def __columninit_kwargs(__ci: SQLAlchemyColumnInit):
    kwargs = {key: value for key, value in __ci.dict().items() if value is not None}
    for delkey in ("name", "type"):
        if delkey in kwargs:
            del kwargs[delkey]
    return kwargs


def __columninit_to_column(ci: SQLAlchemyColumnInit):
    result = None
    if ci.name is not None and ci.type is not None:
        kwargs = __columninit_kwargs(ci)
        result = (
            Column(ci.name, ci.type(), **kwargs)
            if kwargs
            else Column(ci.name, ci.type())
        )
    return result


def __form_sqlmodel(__schema: BaseModel, __Base):

    tablename = str(__schema.__name__).lower()
    fields = list(__schema.__fields__.values())

    columninits = list(map(__field_to_columninit, fields))

    columns = [__columninit_to_column(columninit) for columninit in columninits]

    constraints = [
        PrimaryKeyConstraint(columninit.name, name=f"{tablename}_pkey")
        for columninit in columninits
        if columninit.is_primarykey
    ]

    args = columns + constraints
    SQLModel = Table(tablename, __Base.metadata, *args)
    SQLModel.__tablename__ = tablename
    return SQLModel


def form_sqlmodel(__schema: BaseModel, Base):
    return __form_sqlmodel(__schema, Base)
