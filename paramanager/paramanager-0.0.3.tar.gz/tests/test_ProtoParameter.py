import paramanager as pm
import pytest


def test_default_allowed_chars():
    with pytest.raises(ValueError):
        pm.ProtoParameter("This has spaces so should fail", 0.0)

    with pytest.raises(ValueError):
        pm.ProtoParameter("fail!", 0.0)

    pm.ProtoParameter("test1_test", 0.0)


def test_set_value():
    pp = pm.ProtoParameter("para", 0.0)
    pp.set_value("Hi_this_does_not_make_sense")
    assert pp().value == 0.0

    pp.set_value("0.1")
    assert pp().value == 0.1
