import pytest
from uuid import UUID, uuid5

import attr

from budosystems.models import validation
from budosystems.models.core import Entity, BasicInfo, ValueObject, validate, from_dict, MissingUUID


class TestBudoEntity:
    def test_bad_id_int(self) -> None:
        ent = Entity(id_name=12345)
        with pytest.warns(validation.ValidationWarning) as record:
            validate(ent)
        assert len(record) == 1
        warning = record[0].message
        assert isinstance(warning, validation.ValidationWarning)
        assert isinstance(warning.details, dict)

    def test_good_id_str(self) -> None:
        ent = Entity(id_name='abcdef')
        assert validate(ent)
        assert isinstance(ent.entity_id, UUID)
        assert ent.entity_id is not MissingUUID()

    def test_no_id_param(self) -> None:
        ent = Entity()
        assert validate(ent)
        assert isinstance(ent.entity_id, UUID)
        assert ent.entity_id is not MissingUUID()

    def test_roundtrip_asdict_from_dict(self) -> None:
        ent = Entity()
        ent_dict = attr.asdict(ent)
        ent2 = from_dict(Entity, ent_dict)
        assert ent == ent2

    def test_fail_validation(self) -> None:
        class Entity_A(Entity):
            a_int: int

        with pytest.warns(validation.ValidationWarning) as wrn:
            a = Entity_A(a_int='one')
            validate(a)

        assert wrn
        assert len(wrn.list) == 1
        v_warn = wrn.pop()
        assert isinstance(v_warn.message, validation.ValidationWarning)

    def test_dict_convert_warning(self) -> None:
        class Entity_B(Entity):
            b_int: int

        b_dict = {
                "b_int": "1"
        }

        with pytest.warns(validation.DeserializationWarning) as wrn:
            b = from_dict(Entity_B, b_dict)

        assert isinstance(b, Entity_B)
        assert wrn
        assert len(wrn.list) == 1
        v_warn = wrn.pop()
        assert isinstance(v_warn.message, validation.DeserializationWarning)


class TestBasicInfo:
    def test__id_name_as_property(self) -> None:
        bi = BasicInfo(name="Home Page", slug="home", description="Welcome!")
        assert bi.name == "Home Page"
        assert bi.slug == "home"
        assert bi.description == "Welcome!"
        assert bi.id_name == "home"
        assert bi.entity_id == uuid5(BasicInfo.uuid, bi.slug)

    def test_error_on_missing_required_values(self) -> None:
        with pytest.raises(TypeError):
            _bi = BasicInfo(slug="error", description="Oh no!")

    def test_allow_missing_optional_value(self) -> None:
        bi = BasicInfo(name="No Description!", slug="undescribed")
        assert bi.description == ""
        assert bi.name == "No Description!"
        assert bi.slug == "undescribed"


class TestValueObject:
    def test_subclass(self) -> None:
        class SampleVO(ValueObject):
            v1: int
            v2: str

        assert attr.has(SampleVO)
