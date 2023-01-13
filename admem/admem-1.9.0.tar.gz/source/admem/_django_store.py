# Copyright (c) 2022-2023 Mario S. Könz; License: MIT
import dataclasses as dc
import enum
import types
import typing as tp
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db import models

from ._create_django_model import InspectDataclass
from ._decorator import BACKEND_LINKER
from ._decorator import django_model
from ._protocols import T


@dc.dataclass
class DjangoStore:
    identifier: str

    def dump(self, dc_obj: tp.Any) -> "tuple[models.Model, bool]":
        kwgs, m2m, update_origin = self.dataclass_to_django(dc_obj)
        identifying, defaults = self._split_off_pk(dc_obj, kwgs)
        dj_obj, created = self.backend_manager(dc_obj).update_or_create(
            **identifying, defaults=defaults
        )
        for key, fct in update_origin.items():
            try:
                setattr(dc_obj, key, fct(getattr(dj_obj, key)))
            except dc.FrozenInstanceError as err:
                raise RuntimeError(
                    f"cannot change attribute {key} due to dataclass being frozen, remove field or unfreeze!"
                ) from err

        for key, vals in m2m.items():
            # remove old ones
            if not created:
                getattr(dj_obj, key).clear()
            for val in vals:
                sub_dj_obj, _ = self.dump(val)
                getattr(dj_obj, key).add(sub_dj_obj)

        return dj_obj, created

    def load_all(self, dataclass: type[T], **filter_kwgs: tp.Any) -> tp.Iterator[T]:
        for instance in self.django_load_all(dataclass, **filter_kwgs):
            yield self.django_to_dataclass(instance)

    def django_load_all(
        self, dataclass: type[T], **filter_kwgs: tp.Any
    ) -> tp.Iterator[models.Model]:
        manager = self.backend_manager(dataclass)
        yield from manager.filter(**filter_kwgs).all()

    def dataclass_to_django(self, dc_obj: tp.Any) -> tp.Any:
        model = django_model(dc_obj)
        kwgs = {}
        m2m = {}
        update_origin = {}
        for field in dc.fields(dc_obj):
            key = field.name
            val = getattr(dc_obj, key)
            if type(val) in BACKEND_LINKER.dc_to_backend:
                val, _ = self.dump(val)
            if isinstance(val, enum.Enum):
                val = val.value
            if isinstance(val, Path) and val is not None:

                def get_file(path: Path) -> "File[tp.Any]":
                    return File(
                        open(path, "rb"),  # pylint: disable=consider-using-with
                        name=path.name,
                    )

                try:
                    val = get_file(val)
                    update_origin[key] = lambda x: Path(x.url)
                except FileNotFoundError as err:
                    loc = Path(settings.MEDIA_ROOT) / val.relative_to(val.root)
                    if not loc.exists():
                        raise err
                    val = get_file(loc)

            # pylint: disable=protected-access
            dj_model = model._meta.get_field(key)
            if isinstance(dj_model, models.ManyToManyField):
                m2m[key] = val
            else:
                kwgs[key] = val

        return kwgs, m2m, update_origin

    def django_to_dataclass(self, dj_obj: models.Model) -> tp.Any:
        dataclass = BACKEND_LINKER.backend_to_dc[type(dj_obj)]
        obj_kwgs = {}
        for field in dc.fields(dataclass):
            key = field.name
            val = getattr(dj_obj, key)
            if type(val) in BACKEND_LINKER.backend_to_dc:
                val = self.django_to_dataclass(val)

            field_type = field.type
            origin = tp.get_origin(field_type)
            if origin:
                # pylint: disable=protected-access
                dj_field = dj_obj._meta.get_field(key)
                if origin == types.UnionType:
                    field_type, none_type = tp.get_args(field_type)
                    if none_type != type(None):
                        raise NotImplementedError(
                            "Union not supported yet, except for Optional"
                        )
                    if not val and isinstance(dj_field, models.FileField):
                        val = None

                    if val is None:
                        field_type = type(None)

                elif origin == set:
                    assert isinstance(dj_field, models.ManyToManyField)
                    val = {self.django_to_dataclass(x) for x in val.all()}
                else:
                    raise RuntimeError(f"field type {origin} not supported yet!")

            if issubclass(field_type, enum.Enum):
                val = field_type(val)
            if issubclass(field_type, Path):
                val = Path(val.url)

            obj_kwgs[field.name] = val
        return dataclass(**obj_kwgs)

    parse = django_to_dataclass

    def backend_manager(self, dataclass: type[T]) -> tp.Any:
        return django_model(dataclass).objects.using(self.identifier)

    @classmethod
    def _split_off_pk(
        cls, dc_obj: tp.Any, kwgs: dict[str, tp.Any]
    ) -> tuple[dict[str, tp.Any], dict[str, tp.Any]]:
        ident_keys = InspectDataclass(dc_obj).get_identifying_parameter()
        return (
            {key: kwgs[key] for key in kwgs.keys() & ident_keys},
            {key: kwgs[key] for key in kwgs.keys() ^ ident_keys if key in kwgs},
        )
