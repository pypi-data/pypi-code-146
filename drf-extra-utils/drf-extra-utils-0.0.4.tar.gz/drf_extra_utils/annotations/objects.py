from dataclasses import dataclass
from django.db.models import Aggregate, Model
from typing import Dict, Type

# using prefix to avoid name conflicts.
ANNOTATION_PREFIX = 'annotation__'
ANNOTATION_LIST_PREFIX = 'annotation_list__'


@dataclass
class Annotation:
    """
    The Annotation class is used to retrieve the annotation value for a given model instance. If the annotation value
    has already been calculated and stored in the instance, it is retrieved directly. If the annotation value has not
    yet been calculated, it is fetched using the provided model. This allows for efficient retrieval of annotation
    values without the need to recalculate them every time they are accessed.
    """

    name: str
    annotation: Aggregate
    model: Type[Model]
    annotation_prefix: str = ANNOTATION_PREFIX

    def __post_init__(self):
        self.annotation_name = '{0}{1}'.format(self.annotation_prefix, self.name)

    def get_annotation_expression(self):
        return {self.annotation_name: self.annotation}

    def get_annotation_value(self, instance):
        return getattr(instance, self.annotation_name, None)

    def get_attribute(self, instance):
        annotation_value = self.get_annotation_value(instance)
        # check if annotation has been annotated.
        if annotation_value is not None:
            return annotation_value

        # fetch annotation.
        instance = self.model.objects.filter(pk=instance.pk).annotate(
            **self.get_annotation_expression()
        ).first()
        return self.get_annotation_value(instance)


@dataclass
class AnnotationList:
    """
    The AnnotationList class allows the storage and retrieval of multiple annotations as a dictionary, where the keys
    represent the names of the annotations and the values represent the annotated value. It functions similarly to the
    Annotation class, but is designed to handle multiple annotations at once. It can be used to fetch all the stored
    annotations at once.
    """

    annotations: Dict[str, Aggregate]
    model: Type[Model]

    def __post_init__(self):
        self.children = [
            Annotation(
                name=name,
                annotation=annotation,
                model=self.model,
                annotation_prefix=ANNOTATION_LIST_PREFIX,
            )
            for name, annotation in self.annotations.items()
        ]

    def get_annotation_expression(self):
        result = {}
        for child in self.children:
            result.update(child.get_annotation_expression())
        return result

    def get_annotation_value(self, instance):
        return {
            child.name: child.get_annotation_value(instance)
            for child in self.children
        }

    def get_attribute(self, instance):
        annotation_value = self.get_annotation_value(instance)
        # check if annotations has been annotated.
        if all(annotation_value.values()):
            return annotation_value

        # fetch annotations.
        instance = self.model.objects.filter(pk=instance.pk).annotate(
            **self.get_annotation_expression()
        ).first()
        return self.get_annotation_value(instance)
