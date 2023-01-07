from django.http import HttpRequest
from django.template.context import RenderContext, Context


class InterfaceNotFound(Exception):
    """Interface with this name was not found"""

    pass


class ITemplatePluginMixin:
    """A mixin that can be inherited from to build renderable plugins.

    Create an interface that inherits from ITemplatePluginMixin. Each
    implementation must either have a `template` (direct string HTML template,
    for short ones) or `template_name` (which points to the template to render).

    You can add fixed `context`, or override `get_plugin_context` which receives
    the context of the view the plugin is rendered in.

    In your template, use
    ```
    {% load gdaps %}
    <ul class="alerts">
    {% render_plugin IMyListItem %}
    </ul>
    ```
    in your template anywhere, and all of your implementations are rendered,
    one after each other, in a line. Each plugin can come from another app.
    You can change the order of the rendering using the `weight` attribute.
    """

    template: str = ""
    template_name: str = ""
    context: dict = {}
    weight = 0

    def get_plugin_context(self, context: Context) -> Context:
        """Override this method to add custom context to the plugin.

        :param context: the context where the plugin is rendered in.
            You can update it with own values, and return it.
            The return variable of this function will be the context
            of the rendered plugin. So if you don't update the passed
            context, but just return a new one, the plugin will not get
            access to the global context.

        Per default, it merges the plugin's ``context`` attribute into
        the given global context.
        """
        context.update(self.context)
        return context
