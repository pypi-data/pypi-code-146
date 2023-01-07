from copy import copy

from django import template
from django.template import Template
from django.template.context import Context

from ..api import InterfaceRegistry, Interface
from ..api.interfaces import ITemplatePluginMixin

register = template.Library()


@register.tag(name="render_plugins")
def do_render_plugins(parser, token):
    """A template tag that renders all plugins that implement the given interface."""
    try:
        tag_name, interface_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly one argument: The interface to render"
            % token.contents.split()[0]
        )
    # remove quotes, if there
    if interface_name[0] == interface_name[-1] and interface_name[0] in ('"', "'"):
        interface_name = interface_name[1:-1]
    if not interface_name.isidentifier():
        raise template.TemplateSyntaxError(
            f"'{interface_name}' is not a valid Python identifier."
        )
    return PluginNode(InterfaceRegistry.get(interface_name))


class PluginNode(template.Node):
    def __init__(self, interface: Interface):
        self.interface = interface

    def render(self, context: Context) -> str:
        if self not in context.render_context:
            context.render_context[self] = self.interface

        interface = context.render_context[self]
        content = ""
        for plugin in interface:  # type: ITemplatePluginMixin
            # TODO is copy() needed? Test thread-safety!
            plugin_context = plugin.get_plugin_context(context)
            if plugin.template:
                template = Template(plugin.template)
            else:
                template = plugin_context.template.engine.get_template(
                    plugin.template_name
                )
            content += template.render(context=plugin_context)
        return content
