import pytest
from src.collection_frameworkvsss.unique_characters import unique


@pytest.mark.parametrize("text, expected", [("abbbccdf", 3),
                                            ("aabbccdd", 0),
                                            ("asvbsfkldiss", 8)])
def test_unique(text, expected):
    assert unique(text) == expected


def test_ifdigit():
    with pytest.raises(TypeError):
        unique(123)
