from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.writers.html5 import HTML5Translator
from sphinx import addnodes

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def visit_block_quote(self, node: nodes.block_quote):
    self.body.append('<blockquote class="blockquote p-4 border rounded">')


def depart_block_quote(self, node: nodes.block_quote):
    self.body.append("</blockquote>")


def visit_attribution(self, node: nodes.attribution):
    self.body.append('<footer class="blockquote-footer">')


def depart_attribution(self, node: nodes.attribution):
    self.body.append("</footer>")


def visit_definition_list(self, node: nodes.definition_list):
    if isinstance(node.parent, addnodes.glossary):
        super(HTML5Translator, self).visit_definition_list(node)
    else:
        self.body.append('<dl class="row">')


def depart_definition_list(self, node: nodes.definition_list):
    super(HTML5Translator, self).depart_definition_list(node)


def visit_term(self, node: nodes.term):
    if isinstance(node.parent.parent.parent, addnodes.glossary):
        self.body.append(self.starttag(node, "dt", "", CLASS="h4"))
    else:
        self.body.append('<dt class="col-sm-4">')


def depart_term(self, node: nodes.term):
    if isinstance(node.parent.parent.parent, addnodes.glossary):
        self.add_permalink_ref(node, "Permalink to this term")

    super(HTML5Translator, self).depart_term(node)


def visit_definition(self, node: nodes.definition):
    if isinstance(node.parent.parent.parent, addnodes.glossary):
        super(HTML5Translator, self).visit_definition(node)
    else:
        self.body.append('<dd class="col-sm-8">')


def depart_definition(self, node: nodes.definition):
    super(HTML5Translator, self).depart_definition(node)


def setup(app: "Sphinx") -> None:
    app.add_node(
        nodes.block_quote, html=(visit_block_quote, depart_block_quote), override=True
    )
    app.add_node(
        nodes.attribution, html=(visit_attribution, depart_attribution), override=True
    )
    app.add_node(
        nodes.definition_list,
        html=(visit_definition_list, depart_definition_list),
        override=True,
    )
    app.add_node(nodes.term, html=(visit_term, depart_term), override=True)
    app.add_node(
        nodes.definition, html=(visit_definition, depart_definition), override=True
    )
