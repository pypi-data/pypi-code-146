from enum import Enum
from typing import Optional, Sequence, Union

import numpy as np

from truera.client.nn.client_configs import Dimension


class TrueraDimension(Enum):
    QOI = 1


def _get_data_dimension_order_indices(
    standard_dimension_order: Sequence[Union[Dimension, TrueraDimension]],
    data_dimension_order: Optional[Sequence[Union[Dimension,
                                                  TrueraDimension]]] = None,
):
    '''
    Constructs the transpose ordering. 
    eg) if standard dimension is batch x dim 1 x dim 2, and the data dimension is dim1 x batch x dim2
    then the transpose is (index of batch in data dimension) x (index of dim 1 in data dimension) x (index of dim 2 in data dimension)
    '''
    assert standard_dimension_order is not None
    if data_dimension_order is None:
        data_dimension_order = standard_dimension_order
    data_dimension_order_indices = []
    for dimension in standard_dimension_order:
        assert dimension in data_dimension_order
        data_dimension_order_indices.append(
            data_dimension_order.index(dimension)
        )
    return data_dimension_order_indices


def transpose_to_standard_dimensions(
    data: np.ndarray,
    standard_dimension_order: Sequence[Union[Dimension, TrueraDimension]],
    data_dimension_order: Optional[Sequence[Union[Dimension,
                                                  TrueraDimension]]] = None,
):
    if not standard_dimension_order or not data_dimension_order:
        return data
    assert len(data_dimension_order) == len(standard_dimension_order)

    data_dimension_order_indices = _get_data_dimension_order_indices(
        standard_dimension_order, data_dimension_order
    )
    return data.transpose(tuple(data_dimension_order_indices))


def reverse_transpose_back_to_original_dimensions(
    data: np.ndarray,
    standard_dimension_order: Sequence[Union[Dimension, TrueraDimension]],
    data_dimension_order: Optional[Sequence[Union[Dimension,
                                                  TrueraDimension]]] = None,
):
    '''
    Assumption is that the data is in the standard dimension order, and needs to return back to the data dimension order
    '''
    data_dimension_order_indices = _get_data_dimension_order_indices(
        standard_dimension_order, data_dimension_order
    )

    # The data dimension order will have moved each dimension to the standard.
    # to return, we must find the index of the moved indices,
    # if the 0th index dimension of the original was moved to a different index,
    # we can return it back by finding that index in in the data_dimension_order_indices
    reverse_transpose_order = []
    for i in range(len(data_dimension_order_indices)):
        reverse_transpose_order.append(data_dimension_order_indices.index(i))
    return data.transpose(tuple(reverse_transpose_order))
