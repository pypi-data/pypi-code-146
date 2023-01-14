from typing import ClassVar, List, Dict


def contract_init(self):
    cls = type(self)
    for field in cls.__dict__:
        if is_contract_field(cls, field):
            self.__dict__[field] = cls.__dict__[field]


def get_contract(self) -> List[dict]:
    contract = []
    cls = type(self)
    fields = public_fields(cls)
    for field, _ in fields.items():
        if is_contract_field(cls, field):
            contract.append({
                "field": field,
                "name": cls.__dict__[contr_name(field)],
                "type": cls.__dict__[contr_type(field)],
                "default": cls.__dict__[field],
                "value": self.__dict__[field],
                "allowed": cls.__dict__[allowed_values(field)]
            })
    return contract


def set_value(self, field, value):
    cls = type(self)
    if is_contract_field(cls, field):
        if isinstance(value, valid_type := cls.__dict__[contr_type(field)]):
            if is_allowed(cls, field, value):
                self.__dict__[field] = value
            else:
                raise ValueError(f"'{value}' in not allowed for '{field}' in {cls} contract. Allowed: {cls.__dict__[allowed_values(field)]}")
        else:
            raise TypeError(f"{type(value)} is not a vaild type for '{field}' in {cls} contract. Use {valid_type}")
    else:
        raise AttributeError(f"'{field}' is not a part of {cls} contract")


def is_contract_field(cls: ClassVar, name: str) -> bool:
    return name in cls.__dict__ and contr_name(name) in cls.__dict__ and contr_type(name) in cls.__dict__


def is_allowed(cls: ClassVar, field: str, value) -> bool:
    alfield = allowed_values(field)
    if cls.__dict__[alfield]:
        return value in cls.__dict__[alfield]
    else:
        return True


def write_tuple(self, values: tuple) -> None:
    fields = tuple(public_fields(self).keys())
    if len(fields) != len(values):
        raise ValueError(f"Value amount mismatch. Contract has {len(fields)}, tuple got {len(values)}")

    for i,v in enumerate(values):
        set_value(self, fields[i], v)


def public_fields(obj) -> dict:
    return dict(filter(lambda i: not i[0].startswith("_"), obj.__dict__.items()))


def contr_name(field: str) -> str:
    return f"_{field}_contract_name"


def contr_type(field: str) -> str:
    return f"_{field}_contract_type"


def allowed_values(field: str) -> str:
    return f"_{field}_contract_allowed"