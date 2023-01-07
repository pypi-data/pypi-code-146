from inspect import isclass
from typing import Any

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class RhinoBaseModel(BaseModel):
    session: Annotated[Any, Field(exclude=True)]
    _persisted: bool

    def __init__(self, **data):
        self._handle_aliases(data)
        self._handle_uids(data)
        self._handle_models(data)
        super().__init__(**data)

    def __str__(self):
        return f"{self.__class__.__name__} {super(RhinoBaseModel, self).__str__()}"

    class Config:
        """
        @autoapi False
        """

        ignore_extra = True
        underscore_attrs_are_private = True

    def _handle_uids(self, data):
        """
        Remap backend uid results to uid parameter
        """
        for field in self.__fields__:
            if data.get(field, None) is not None:  # User passed in or already converted
                continue
            if field.endswith("_uids"):
                old_key = field[:-5]
            elif field.endswith("_uid"):
                old_key = field[:-4]
            else:
                continue
            value = data.get(old_key, None)
            if value is not None:
                data[field] = value

    def _handle_models(self, data):
        """
        Add the session variable to any child models
        """
        session = getattr(self, "session", data.get("session"))
        for field, field_attr in self.__fields__.items():
            if isclass(field_attr.type_) and issubclass(field_attr.type_, RhinoBaseModel):
                value = data.get(field, None)
                if field_attr.sub_fields is not None and isinstance(value, list):
                    for entry in value:
                        if isinstance(entry, dict):
                            entry["session"] = session
                else:
                    if isinstance(value, dict):
                        data[field]["session"] = session

    def _handle_aliases(self, data):
        for field, field_attr in self.__fields__.items():
            if field_attr.name != field_attr.alias:
                value = data.get(field_attr.name, None)
                if value is not None:
                    data[field_attr.alias] = value

    def json(self, *args, **kwargs):
        # TODO: Need to reverse the uids
        super(RhinoBaseModel, self).json(*args, **kwargs)
