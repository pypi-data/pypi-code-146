import sys
from typing import Dict, List, Tuple, Union

import pytest

from typepigeon.types import subscripted_type


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires Python 3.8 or greater")
def test_subscripted_types():
    subscripted_type_1 = subscripted_type(List[str])
    subscripted_type_2 = subscripted_type(Tuple[str, float])
    subscripted_type_3 = subscripted_type(Dict[str, int])

    assert subscripted_type_1 == [str]
    assert subscripted_type_2 == (str, float)
    assert subscripted_type_3 == {str: int}


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires Python 3.8 or greater")
def test_mixed_types():
    mixed_type_1 = subscripted_type([str])
    mixed_type_2 = subscripted_type([Tuple[float, List[int]]])
    mixed_type_3 = subscripted_type({str: Tuple[str, int]})
    mixed_type_4 = subscripted_type({str: (Dict[int, str], str)})

    assert mixed_type_1 == [str]
    assert mixed_type_2 == [(float, [int])]
    assert mixed_type_3 == {str: (str, int)}
    assert mixed_type_4 == {str: ({int: str}, str)}


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires Python 3.8 or greater")
def test_union_types():
    with pytest.raises(NotImplementedError):
        subscripted_type(Union[str, int])
