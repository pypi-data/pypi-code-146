from drf_extra_utils.annotations.objects import Annotation, AnnotationList


class model_annotation:
    """
    This is a decorator that allows you to annotate models with calculated values. It can be accessed on an instance
    of the model as an attribute, its value will be annotated in instance queryset otherwise calculated on the fly by
    the ORM.
    """

    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, model=None):
        annotation_value = self.func(instance)

        if isinstance(annotation_value, dict):
            annotation_object = AnnotationList(
                annotations=annotation_value,
                model=model
            )
        else:
            annotation_object = Annotation(
                name=self.name,
                annotation=annotation_value,
                model=model,
            )

        if instance is None:
            return annotation_object.get_annotation_expression()

        attribute = annotation_object.get_attribute(instance)
        setattr(instance, self.name, attribute)
        return attribute
