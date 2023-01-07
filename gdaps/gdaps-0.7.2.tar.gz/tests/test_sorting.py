import pytest
from django.template import Template, TemplateSyntaxError
from django.template.context import Context

from gdaps.api import Interface
from gdaps.api.interfaces import ITemplatePluginMixin


def render_template(string: str, context: dict = None):
    """A simple template render helper"""
    context = context or {}
    context = Context(context)
    return Template(string).render(context)


@Interface
class Interface1:
    __service__ = False


# classes in reverse declaration order, but correct "weight" attrs
class Impl2(Interface1):
    weight = 1


class Impl1(Interface1):
    weight = 0


def test_interface_list_weights_reverse_declaration():
    """test order of interfaces without "weight" attribute"""
    implementations_list = [a for a in Interface1]
    # despite reverse declaration order, they must be in correct order
    assert implementations_list[0] is Impl1
    assert implementations_list[1] is Impl2


@Interface
class Interface2:
    __service__ = False


class Impl3(Interface2):
    weight = 10


class Impl4(Interface2):
    """this class implicitly gets weight=0"""

    # weight = 0


def test_interface_list_with_one_impl_without_weight():
    """test order of interfaces where one implementation has no "weight" attribute"""
    implementations_list = [a for a in Interface2]
    assert implementations_list[0] is Impl4
    assert implementations_list[1] is Impl3


@Interface
class I3:
    __service__ = False


def test_interface_list_without_weight():
    """test order of interfaces without "weight" attribute"""
    implementations_list = [a for a in Interface2]
    # despite reverse declaration order, they must be in correct order
    assert implementations_list[0] is Impl4
    assert implementations_list[1] is Impl3
