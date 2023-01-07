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


# simple template
@Interface
class IAnyItem(ITemplatePluginMixin):
    pass


class SimpleFooItem(IAnyItem):
    template = "<div>Foo</div>"


def test_render_plugin_with_simple_template():
    content = render_template("{% load gdaps %}{% render_plugins IAnyItem %}")
    assert content == "<div>Foo</div>"


def test_render_plugin_with_simple_template_with_interface_in_quotes():
    content = render_template("{% load gdaps %}{% render_plugins 'IAnyItem' %}")
    assert content == "<div>Foo</div>"


# template file
@Interface
class IAnyItemFile(ITemplatePluginMixin):
    pass


class SimpleFooItemFile(IAnyItemFile):
    template_name = "simple_foo_item.html"


def test_render_plugin_with_file_template():
    content = render_template("{% load gdaps %}{% render_plugins IAnyItemFile %}")
    assert content == "<div>Foo - template</div>"


# simple context
@Interface
class IAnyItem2(ITemplatePluginMixin):
    pass


class SimpleFooItem2(IAnyItem2):
    template = "<div>{{context1}}</div>"


def test_render_plugin_with_simple_passed_context():
    content = render_template(
        "{% load gdaps %}{% render_plugins IAnyItem2 %}",
        {"context1": "879d72z3d"},
    )
    assert content == "<div>879d72z3d</div>"


# simple context as attr
@Interface
class IContextItem(ITemplatePluginMixin):
    pass


class SimpleContextItem(IContextItem):
    context = {"foo": "bar"}
    template = "<div>{{foo}}</div>"


def test_render_plugin_with_simple_class_context():
    """test if context from "context" attr of plugin gets rendered"""
    content = render_template(
        "{% load gdaps %}{% render_plugins IContextItem %}",
    )
    assert content == "<div>bar</div>"


def test_render_plugin_with_simple_class_context_overridden():
    """test if context from "context" attr of plugin overrides global context"""
    content = render_template(
        "{% load gdaps %}{% render_plugins IContextItem %}",
        context={"foo": "must not be rendered!"},
    )
    assert content == "<div>bar</div>"


# context with get_plugin_context method
@Interface
class IContextMethodItem(ITemplatePluginMixin):
    pass


class SimpleContextMethodItem(IContextMethodItem):
    def get_plugin_context(self, context):
        return Context({"foo": "done with method"})

    template = "<div>{{foo}}</div>"


def test_render_template_with_tag_and_context_method():
    content = render_template("{% load gdaps %}{% render_plugins IContextMethodItem %}")
    assert content == "<div>done with method</div>"


# Wrong syntax etc.
def test_render_template_with_interface_syntax_wrong1():
    """interface arg syntax wrong"""
    with pytest.raises(TemplateSyntaxError):
        render_template("{% load gdaps %}{% render_plugins foo='IContextMethodItem' %}")


def test_render_template_with_interface_syntax_wrong2():
    """interface arg syntax wrong"""
    with pytest.raises(TemplateSyntaxError):
        render_template(
            "{% load gdaps %}{% render_plugins interface='IContextMethodItem' %}"
        )


def test_render_template_with_interface_syntax_wrong_additional_arg():
    """interface arg syntax wrong"""
    with pytest.raises(TemplateSyntaxError):
        render_template(
            "{% load gdaps %}{% render_plugins IContextMethodItem 'wrong_arg' %}"
        )


# rendering interface that has wrong parameters
@Interface
class IBadInterface:
    attr = "something"


class BadImplementation(IBadInterface):
    pass


def test_render_bad_interface():
    with pytest.raises(AttributeError):
        render_template("{% load gdaps %}{% render_plugins IBadInterface %}")
