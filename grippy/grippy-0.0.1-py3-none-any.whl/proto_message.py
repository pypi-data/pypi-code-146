import inspect

from pydantic import BaseModel

type_mapping = {
    int: "int32",
    str: "string"
}


class ProtoField(BaseModel):
    type: type
    name: str
    num: int

    @property
    def proto_type(self) -> str:
        return type_mapping[self.type]

    @property
    def field_spec(self) -> str:
        return f"{self.proto_type} {self.name} = {self.num};"


class ProtoMessage(BaseModel):
    name: str
    fields: list[ProtoField]

    def __str__(self) -> str:
        val = f"message {self.name} " + "{\n  "
        val += "\n  ".join(f.field_spec for f in self.fields)
        val += "\n}"
        return val

    @classmethod
    def from_model(cls, model: BaseModel) -> "ProtoMessage":
        return cls(
            name=model.__name__,
            fields=[
                ProtoField(type=type, name=name, num=i)
                for i, (name, type) in enumerate(
                    inspect.get_annotations(model).items(),
                    start=1
                )
            ]
        )
