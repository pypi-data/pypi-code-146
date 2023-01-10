"""sphinxcontrib.specs.steps"""

from typing import TYPE_CHECKING, Dict, Any, List

from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.transforms import SphinxTransform

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class steps_list(nodes.General, nodes.Element):
    pass


def visit_steps_list(self, node: steps_list) -> None:
    classes = ["accordion"] + node["classes"]
    if "hidenums" in node.attributes:
        classes += ["hide-step-nums"]
    self.body.append(self.starttag(node, "div", classes=classes))


def depart_steps_list(self, _) -> None:
    self.body.append("</div>\n")


class step(nodes.Part, nodes.Element):
    pass


def visit_step(self, node: step) -> None:
    self.body.append(
        self.starttag(node, "div", classes=["accordion-item"] + node["classes"])
    )


def depart_step(self, _) -> None:
    self.body.append("</div>\n")
    self.body.append("</div>\n")
    self.body.append("</div>\n")


class step_title(nodes.Part, nodes.TextElement):
    pass


def visit_step_title(self, node: step_title) -> None:
    self.body.append('<h3 class ="accordion-header">')
    self.body.append(
        f'<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{node["ids"][0]}">'
    )
    self.body.append('<span class="specssteps-title">')


def depart_step_title(self, node: step_title) -> None:
    self.body.append("</span>")
    self.body.append("</button>\n")
    self.body.append("</h3>\n")
    self.body.append(
        f'<div id="{node["ids"][0]}" class="accordion-collapse collapse">\n'
    )
    self.body.append('<div class="accordion-body">\n')


class StepsList(SphinxDirective):
    has_content = True
    option_spec = {"hidenums": directives.flag}

    def run(self) -> List[Node]:
        node = steps_list(
            "\n".join(self.content), classes=["specssteps-list"], **self.options
        )

        node.document = self.state.document
        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class Step(SphinxDirective):
    has_content = True
    final_argument_whitespace = True
    required_arguments = 1

    def run(self) -> List[Node]:
        node = step("")

        title_text = self.arguments[0]
        text_nodes, messages = self.state.inline_text(title_text, self.lineno)
        title_node = step_title(
            title_text, "", *text_nodes, classes=["specssteps-title"]
        )
        (
            title_node.source,
            title_node.line,
        ) = self.state_machine.get_source_and_line(self.lineno)
        node += [title_node]

        body_node = nodes.container(
            "\n".join(self.content), classes=["specssteps-body"]
        )
        body_node.document = self.state.document
        self.state.nested_parse(self.content, self.content_offset, body_node)

        node += [body_node]

        return [node]


class StepsIDTransform(SphinxTransform):
    default_priority = 799

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.findall(steps_list):
            section = self.find_section_parent(node)
            section_id = section["ids"][0]

            counter = 0
            for step in node.findall(step_title):
                step["ids"] = [f"{section_id}-step-{counter}"]
                counter += 1

    def find_section_parent(self, node) -> nodes.section:
        curr = node
        while not isinstance(curr, nodes.section):
            curr = curr.parent

        return curr


def setup(app: "Sphinx") -> Dict[str, Any]:
    app.add_node(steps_list, html=(visit_steps_list, depart_steps_list))
    app.add_node(step, html=(visit_step, depart_step))
    app.add_node(step_title, html=(visit_step_title, depart_step_title))

    app.add_directive("stepslist", StepsList)
    app.add_directive("step", Step)

    app.add_transform(StepsIDTransform)
