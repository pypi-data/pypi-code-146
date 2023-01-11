from fnmatch import fnmatch
import re

import attr
from sumtypes import constructor
from sumtypes import match
from sumtypes import sumtype

from truera.rnn.general.service.sync_client import SyncClient


@sumtype
class Locator(object):
    # follows get_cache_path choices
    Artifact = constructor("project", "model", "data_collection", "split")
    Split = constructor("project", "data_collection", "split")
    DataCollection = constructor("project", "data_collection")
    Model = constructor("project", "model")
    Export = constructor(
        "project", "model", "data_collection", "split", "filename"
    )

    def to_locator_string(self):
        return "/".join(
            [
                getattr(self, field.name)
                for field in attr.fields(self.__class__)
            ]
        )

    @classmethod
    def of_str(cls, s: str):
        pieces = s.split("/")

        if len(pieces) == 3:
            project, t, model_or_dc = pieces

            if t.startswith('model'):
                return Locator.Model(project, model_or_dc)
            elif t.startswith('data_collection'):
                return Locator.DataCollection(project, model_or_dc)
            else:
                raise Exception(f"unknown locator type: {t}")

        elif len(pieces) == 4:
            project, t, dc, split = pieces

            if t.startswith('split'):
                return Locator.Split(project, dc, split)
            else:
                raise Exception(f"unknown locator type: {t}")

        elif len(pieces) == 5:
            project, t, dc, split, model = pieces

            if t.startswith('artifact'):
                return Locator.Artifact(project, model, dc, split)
            else:
                raise Exception(f"unknown locator type: {t}")

        else:
            raise Exception(f"cannot parse locator string: {s}")


@match(Locator)
class to_locator_string(object):

    def Artifact(project, model, data_collection, split):
        return "/".join([project, "artifact", model, data_collection, split])

    def Model(project, model):
        return "/".join([project, "model", model])

    def Split(project, data_collection, split):
        return "/".join([project, "split", data_collection, split])

    def DataCollection(project, data_collection):
        return "/".join([project, "data_collection", data_collection])

    def Export(project, model, data_collection, split, filename):
        return "/".join(
            [project, "export", model, data_collection, split, filename]
        )
