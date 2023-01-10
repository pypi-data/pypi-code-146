from typing import Any, Type
from rest_framework import generics
from rest_framework.serializers import BaseSerializer


class GenericAPIView(generics.GenericAPIView):
    """
    Extends GenericAPIView to add support for resolving serializer class based on the requested API version.
    """

    def get_serializer_class(self, *args: Any, **kwargs: Any) -> Type[BaseSerializer]:
        version_serializer_attr = self._get_version_serializer_attr()

        if version_serializer_attr is None:
            assert (
                self.serializer_class is not None
            ), "serializer_class attribute is required to support version-less requests."

            return self.serializer_class

        assert hasattr(
            self, version_serializer_attr
        ), f"{version_serializer_attr} attribute is missing. It is required to support {self.request.version}."

        return getattr(self, version_serializer_attr)

    def _get_version_serializer_attr(self) -> "str | None":
        if self.request.version is None:
            return None

        return "serializer_class_{}".format(self.request.version.replace(".", "_"))
