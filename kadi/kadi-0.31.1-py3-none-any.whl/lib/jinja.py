# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import render_template
from jinja2 import nodes
from jinja2.ext import Extension


class SnippetExtension(Extension):
    """Jinja extension to pass variables to HTML snippets.

    See :func:`render_snippet` for an explanation of the parameters.

    **Example:**

    .. code-block:: jinja

        {% snippet "my_snippet", foo=1, bar=2 %}
    """

    tags = {"snippet"}

    def parse(self, parser):
        """Parse the snippet tag and arguments."""
        kwargs = []

        # Token that started the tag.
        tag = next(parser.stream)

        # Parse the snippet name.
        name = parser.parse_expression()

        if parser.stream.skip_if("comma"):
            # Parse the key/value-arguments.
            while parser.stream.current.type != "block_end":
                if kwargs:
                    parser.stream.expect("comma")

                key = next(parser.stream)
                key = nodes.Const(key.value, lineno=key.lineno)

                parser.stream.expect("assign")

                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=key.lineno))

        return nodes.CallBlock(
            self.call_method("_render_snippet", [name, nodes.Dict(kwargs)]), [], [], []
        ).set_lineno(tag.lineno)

    def _render_snippet(self, name, kwargs, caller):
        return render_snippet(name, **kwargs)


def render_snippet(snippet, _module=None, **kwargs):
    r"""Render an HTML snippet.

    The snippet has to be in a directory called "snippets". Otherwise, the same rules
    apply as in Flask's ``render_template`` function.

    :param snippet: The name of the snippet without the ".html" extension.
    :param _module: (optional) If the snippet is part of a module, the name of this
        module can be specified using this parameter. It will be prepended before the
        snippet path.
    :param \**kwargs: The keyword arguments to pass to the snippet.
    :return: The rendered snippet.
    """
    module = f"{_module}/" if _module else ""
    return render_template([f"{module}snippets/{snippet}.html"], **kwargs)
