import pytest

from chalk.features import feature, features, unwrap_feature


@features
class CustomNameClass:
    id: str
    other: str = feature(name="other_name")


def test_custom_name():
    assert CustomNameClass(other="papaya").other == "papaya"
    assert CustomNameClass(id="4", other="papaya") == CustomNameClass(id="4", other="papaya")
    assert unwrap_feature(CustomNameClass.other).name == "other_name"
    assert str(CustomNameClass(other="papaya")) == "CustomNameClass(other=papaya)"
    assert str(CustomNameClass(id="4", other="papaya")) == "CustomNameClass(id=4, other=papaya)"
    assert dict(CustomNameClass(id="4", other="papaya")) == {
        "custom_name_class.id": "4",
        "custom_name_class.other_name": "papaya",
    }
    assert len(CustomNameClass(id="4", other="papaya")) == 2
    assert len(CustomNameClass(id="4")) == 1


@features(name="prince")
class TheArtistFormerlyKnownAsPrince:
    id: str
    favorite_color: str = feature(name="fav")


def test_custom_namespace():
    assert TheArtistFormerlyKnownAsPrince(id="a").id == "a"
    assert TheArtistFormerlyKnownAsPrince(id="4", favorite_color="purple") == TheArtistFormerlyKnownAsPrince(
        id="4", favorite_color="purple"
    )
    assert str(TheArtistFormerlyKnownAsPrince.id) == "prince.id"
    assert str(TheArtistFormerlyKnownAsPrince.favorite_color) == "prince.fav"
    with pytest.raises(ValueError):

        @features(name="with spaces")
        class Spaced:
            id: int

    with pytest.raises(ValueError):

        @features(name="WithCaps")
        class CapitalizedCls:
            id: int
