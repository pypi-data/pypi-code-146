import json
from dataclasses import asdict
from typing import Union

from dataclasses_json import DataClassJsonMixin


class ArthurBaseJsonDataclass(DataClassJsonMixin):
    @staticmethod
    def clean_nones(d):
        """Helper function to filter out None objects from a json or dictionary representation of an object

        :param d: a Dictionary or Json representation of an ArthurBaseJsonDataclass object
        :return: Dictionary of the object with all None components removed
        """
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return list(filter(lambda item: item is not None, map(ArthurBaseJsonDataclass.clean_nones, d)))
        return {k: v for k, v in ((k, ArthurBaseJsonDataclass.clean_nones(v)) for k, v in d.items()) if v is not None }

    def to_json(self, skip_none=True) -> str: # type: ignore
        """Creates a json representation of this object

        This function can be applied to any extension of the ArthurBaseJsonDataClass

        :return: json of object data
        """
        obj_dict = asdict(self)
        if skip_none:
            obj_dict = self.clean_nones(obj_dict)
        return json.dumps(obj_dict)

    def to_dict(self, skip_none=True) -> dict:
        """Creates a dictionary representation of this object

        This function can be applied to any extension of the ArthurBaseJsonDataClass

        :return: Dictionary of object data
        """
        obj_dict = asdict(self)
        if skip_none:
            obj_dict = self.clean_nones(obj_dict)
        return obj_dict


NumberType = Union[int, float]