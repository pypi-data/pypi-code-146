from typing import TYPE_CHECKING

from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst.roles import set_classes
from docutils import nodes

from sphinx.writers.html5 import HTML5Translator

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class OverrideAdmonition(BaseAdmonition):
    optional_arguments = 1

    def run(self):
        if self.node_class is nodes.admonition or not self.arguments:
            return super().run()

        # All other admonition types can have a title (the first optional
        # argument). If we have a title, it needs to be included in the
        # admonition node's content so it can be parsed along with everything
        # else.

        set_classes(self.options)
        self.assert_has_content()
        text = f"{self.arguments[0]}\n" + "\n".join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)

        title_text = self.arguments[0]
        textnodes, messages = self.state.inline_text(title_text, self.lineno)
        title = nodes.paragraph(title_text, "", *textnodes)
        title["classes"] = ["h5", "admonition-title"]

        title.source, title.line = self.state_machine.get_source_and_line(self.lineno)
        admonition_node += title
        admonition_node += messages

        self.state.nested_parse(self.content, self.content_offset, admonition_node)

        return [admonition_node]


class Attention(OverrideAdmonition):

    node_class = nodes.attention


class Caution(OverrideAdmonition):

    node_class = nodes.caution


class Danger(OverrideAdmonition):

    node_class = nodes.danger


class Error(OverrideAdmonition):

    node_class = nodes.error


class Hint(OverrideAdmonition):

    node_class = nodes.hint


class Important(OverrideAdmonition):

    node_class = nodes.important


class Note(OverrideAdmonition):

    node_class = nodes.note


class Tip(OverrideAdmonition):

    node_class = nodes.tip


class Warning(OverrideAdmonition):

    node_class = nodes.warning


def visit_title(self, node: nodes.title):
    # Skip node if this is a title for a hint
    if isinstance(node.parent, nodes.hint) and node.parent.index(node) == 0:
        raise nodes.SkipNode

    super(HTML5Translator, self).visit_title(node)


def depart_title(self, node: nodes.title):
    super(HTML5Translator, self).depart_title(node)

    if isinstance(node.parent, nodes.hint):
        self.body.append('<details class="admonition-body">')
        self.body.append("<summary></summary>")


def visit_admonition(self, node: nodes.Element, name: str = ""):
    self.body.append(
        self.starttag(
            node, "div", CLASS=("admonition py-3 px-4 my-4 rounded border " + name)
        )
    )


def depart_admonition(self, node: nodes.Element):
    self.body.append("</div>\n")


def visit_attention(self, node: nodes.note):
    visit_admonition(self, node, "attention")


def visit_caution(self, node: nodes.note):
    visit_admonition(self, node, "caution")


def visit_danger(self, node: nodes.note):
    visit_admonition(self, node, "danger")


def visit_error(self, node: nodes.note):
    visit_admonition(self, node, "error")


def visit_important(self, node: nodes.note):
    visit_admonition(self, node, "important")


def visit_tip(self, node: nodes.note):
    visit_admonition(self, node, "tip")


def visit_warning(self, node: nodes.note):
    visit_admonition(self, node, "warning")


def visit_note(self, node: nodes.note):
    visit_admonition(self, node, "note")


def depart_hint(self, node: nodes.hint):
    self.body.append("</details>")

    super(HTML5Translator, self).depart_hint(node)


def visit_paragraph(self, node: nodes.paragraph):
    # For handling hints
    self.body.append(self.starttag(node, "p", CLASS=" ".join(node["classes"])))


def depart_paragraph(self, node: nodes.paragraph):
    super(HTML5Translator, self).depart_paragraph(node)

    # For handling hints
    if "admonition-title" in node["classes"] and isinstance(node.parent, nodes.hint):
        self.body.append("<details>")
        self.body.append("<summary></summary>")


def setup(app: "Sphinx") -> None:
    app.add_directive("attention", Attention, override=True)
    app.add_directive("caution", Caution, override=True)
    app.add_directive("danger", Danger, override=True)
    app.add_directive("error", Error, override=True)
    app.add_directive("hint", Hint, override=True)
    app.add_directive("important", Important, override=True)
    app.add_directive("note", Note, override=True)
    app.add_directive("tip", Tip, override=True)
    app.add_directive("warning", Warning, override=True)

    app.add_node(
        nodes.admonition, html=(visit_admonition, depart_admonition), override=True
    )
    app.add_node(
        nodes.attention, html=(visit_attention, depart_admonition), override=True
    )
    app.add_node(nodes.caution, html=(visit_caution, depart_admonition), override=True)
    app.add_node(nodes.danger, html=(visit_danger, depart_admonition), override=True)
    app.add_node(nodes.error, html=(visit_error, depart_admonition), override=True)
    app.add_node(
        nodes.hint, html=(HTML5Translator.visit_hint, depart_hint), override=True
    )
    app.add_node(
        nodes.important, html=(visit_important, depart_admonition), override=True
    )
    app.add_node(nodes.note, html=(visit_note, depart_admonition), override=True)
    app.add_node(nodes.tip, html=(visit_tip, depart_admonition), override=True)
    app.add_node(nodes.warning, html=(visit_warning, depart_admonition), override=True)
    app.add_node(
        nodes.paragraph, html=(visit_paragraph, depart_paragraph), override=True
    )
