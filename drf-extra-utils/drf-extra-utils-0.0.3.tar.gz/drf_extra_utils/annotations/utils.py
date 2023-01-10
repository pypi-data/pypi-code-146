from rest_framework.serializers import ModelSerializer, ReadOnlyField


def get_serializer_field_from_annotation(annotation):
    """
    This is a helper function that is used to get the appropriate serializer field for a given annotation.
    """
    try:
        return ModelSerializer.serializer_field_mapping[annotation.output_field.__class__]()
    except (AttributeError, KeyError):
        return ReadOnlyField()
