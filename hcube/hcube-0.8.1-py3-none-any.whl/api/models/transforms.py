"""
Functionality to transform data obtained from the database. Equivalent to applying a function on
some of the rows.

Not all backends need to support all transforms.
"""
from abc import ABC
from typing import Optional, Union

from hcube.api.models.dimensions import Dimension


class Transform(ABC):

    """
    `dimension` is the dimension to be transformed.
    `name` is the field name under which the resulting value will appear
    """

    def __init__(self, dimension: Union[Dimension, str], name: Optional[str] = None):
        self.dimension = dimension
        dim_name = dimension.name if isinstance(dimension, Dimension) else dimension
        self.name = name if name else dim_name


class StoredMappingTransform(Transform):
    """
    This transform assumes that there is a mapping with `mapping_name` stored at the backend.
    The mapping may be multidimensional, so `mapping_field` is used to select the appropriate
    'row' from the mapping.
    """

    def __init__(
        self,
        dimension: Union[Dimension, str],
        mapping_name: str,
        mapping_field: Optional[str],
        name: Optional[str] = None,
    ):
        super().__init__(dimension, name=name)
        self.mapping_name = mapping_name
        self.mapping_field = mapping_field


StoredMap = StoredMappingTransform


class ExplicitMappingTransform(Transform):
    """
    This transform expects a dict-like mapping to be given as one of the params and then uses
    this mapping to convert values of `dimension` to the resulting values.
    """

    def __init__(self, dimension: Union[Dimension, str], mapping: dict, name: Optional[str] = None):
        super().__init__(dimension, name)
        self.mapping = mapping


# just an alias for simpler name
Map = ExplicitMappingTransform
