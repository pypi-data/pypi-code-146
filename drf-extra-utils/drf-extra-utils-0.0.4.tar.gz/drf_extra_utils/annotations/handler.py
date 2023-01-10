from dataclasses import dataclass
from typing import Type
from collections import OrderedDict

from django.db.models import Model

from drf_extra_utils.annotations.decorator import model_annotation
from drf_extra_utils.annotations.fields import AnnotationListField
from drf_extra_utils.annotations.utils import get_serializer_field_from_annotation


@dataclass
class ModelAnnotationHandler:
    """
    The ModelAnnotationHandler class is a utility that simplifies the process of working with annotations on models.
    It stores all the annotations defined for a model in a dictionary and allows you to easily retrieve the annotations
    you need for a queryset by specifying their names.
    """

    model: Type[Model]

    def __post_init__(self):
        self.annotations = {
            name: getattr(self.model, name)
            for name, attr in vars(self.model).items()
            if hasattr(attr, '__class__') and attr.__class__ == model_annotation
        }

    def get_annotations(self, *fields):
        if '*' in fields:
            fields = self.annotations.keys()

        annotations = {}
        for name, annotation in self.annotations.items():
            if name in fields:
                annotations.update(annotation)

        return annotations


def _get_annotation_serializer_field(annotation):
    """
    Helper function that returns a serializer field for a given annotation.
    """

    if isinstance(annotation, dict):
        return AnnotationListField(annotations=annotation)

    return get_serializer_field_from_annotation(annotation)


@dataclass
class ModelAnnotationFieldHandler:
    """
    The ModelAnnotationFieldHandler class is used to generate serializer fields for a model annotations. It retrieves all
    model annotations and creates the corresponding serializer field for each one. If the annotation is a dictionary,
    it creates an AnnotationListField. Otherwise, it creates the serializer field based on the annotation.
    """

    model: Type[Model]

    def __post_init__(self):
        self.annotations = {
            name: attr.func(None)
            for name, attr in vars(self.model).items()
            if hasattr(attr, '__class__') and attr.__class__ == model_annotation
        }

    def get_annotation_serializer_fields(self):
        fields = OrderedDict()

        for name, annotation in self.annotations.items():
            fields[name] = _get_annotation_serializer_field(annotation)

        return fields
