import attr
from attr.exceptions import FrozenInstanceError, FrozenError, FrozenAttributeError
import pytest

from budosystems.models.meta import BudoMeta, BudoBase
from budosystems.events import MESSAGE_BUS
from budosystems.events.base import FieldModifiedEvent, FieldType


def test_plain():
    class A(metaclass=BudoMeta):
        pass

    assert isinstance(A, BudoMeta)
    assert attr.has(A)


def test_class_with_fields():
    class B(metaclass=BudoMeta):
        b_str: str
        b_int: int

    b_fields = attr.fields(B)

    assert len(b_fields) == 2
    assert b_fields[0].name == "b_str"
    assert b_fields[0].type == str
    assert b_fields[1].name == "b_int"
    assert b_fields[1].type == int


def test_instance_with_fields():
    class C(metaclass=BudoMeta):
        c_str: str
        c_int: int

    c = C(c_str="something", c_int=42)
    assert attr.has(C)
    assert c.c_str == "something"
    assert c.c_int == 42

    c2 = C(c_str="something", c_int=42)
    assert c == c2, 'Has implicit __eq__'


# def test_class_with_arbitrary_config_arg():
#     config = {"special": ..., "null": None, "fn": lambda x: x}
#
#     class E(metaclass=BudoMeta, config=config):
#         pass
#
#     assert E.config
#     assert E.config["special"] is ...
#     assert E.config["null"] is None
#     assert E.config["fn"](7) == 7


def test_class_with_attr_config_arg():
    attrs = {"eq": False}

    class F(metaclass=BudoMeta, attrs=attrs):
        f_int: int

    f1 = F(f_int=32)
    f2 = F(f_int=32)
    assert f1 != f2, "Implicit __eq__ prevented"


def test_class_with_other_kwargs():
    class G(metaclass=BudoMeta, letter=7, greek='gamma'):
        radiation: float

    assert G.metadata
    assert G.metadata['letter'] == 7
    assert G.metadata['greek'] == 'gamma'

def test_frozen_instance_assign_post_create():
    class H(metaclass=BudoMeta,  attrs={'frozen': True}):
        h_int: int
        h_str: str

    h1 = H(h_int=8, h_str="eight")
    assert h1.h_int == 8
    assert h1.h_str == "eight"

    with pytest.raises(FrozenInstanceError) as err:
        h1.h_int = 88

    assert issubclass(err.type, FrozenInstanceError)
    assert h1.h_int == 8

async def _print_field_event(event: FieldModifiedEvent[FieldType]) -> None:
    msg = f"'{event.field_name}' changed from '{event.old_value}' to '{event.new_value}'"
    print(msg)

def test_instance_assign_post_create_event(capsys):
    MESSAGE_BUS.unregister_event_handlers(all_handlers=True)  # shouldn't need, just making sure.
    MESSAGE_BUS.register_event_handler(FieldModifiedEvent, _print_field_event)

    class I(metaclass=BudoMeta):
        i_int: int
        i_str: str

    i1 = I(i_int = 9, i_str="iota")

    assert i1.i_int == 9
    assert i1.i_str == "iota"

    i1.i_str = "nine"
    captured_sys = capsys.readouterr()
    assert captured_sys.out.strip() == "'i_str' changed from 'iota' to 'nine'"
    MESSAGE_BUS.unregister_event_handlers(all_handlers=True)
