"""sphinxcontrib.specs.objectives

Directives, transforms, etc. for rendering objectives.
"""

from typing import TYPE_CHECKING, Dict, Any, List, cast

from docutils import nodes
from docutils.nodes import Node
from sphinx.util.docutils import SphinxDirective
from sphinx.transforms import SphinxTransform
from sphinx.util import logging


if TYPE_CHECKING:
    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)


class objectives(nodes.General, nodes.Element):
    pass


class Objectives(SphinxDirective):
    has_content = True

    def run(self) -> List[Node]:
        node = objectives()
        node.document = self.state.document
        self.state.nested_parse(self.content, self.content_offset, node)

        if len(node.children) != 1 or not isinstance(
            node.children[0], nodes.bullet_list
        ):
            logger.warning(
                ".. objectives:: content is not a bulleted list",
                location=(self.env.docname, self.lineno),
            )
            return []

        node["parent_section"] = self.state.parent.parent

        return [node]


def visit_objectives(self, node: objectives) -> None:
    self.body.append(self.starttag(node, "div", classes=["objectives"]))


def depart_objectives(self, _) -> None:
    self.body.append("</div>\n")


class objectivesindex(nodes.Sequential, nodes.Element):
    pass


class objectivesindex_item(nodes.Part, nodes.Element):
    pass


class objectivesindex_name(nodes.Part, nodes.TextElement):
    pass


class objectivesindex_body(nodes.Part, nodes.Element):
    pass


class ObjectivesIndex(SphinxDirective):
    has_content = False

    def run(self) -> List[Node]:
        subnode = objectivesindex()

        return [subnode]


class ObjectivesIndexTransformer(SphinxTransform):
    default_priority = 900

    def apply(self, **kwargs: Any) -> None:
        objectives = self.create_objectivesindex_items()
        for objindex in self.document.findall(objectivesindex):
            objindex.extend([o.deepcopy() for o in objectives])

    def create_objectivesindex_items(self) -> nodes.field_list:
        items = []
        for o in self.document.findall(objectives):
            parent_section = cast(nodes.Element, o["parent_section"])
            title = parent_section.children[
                parent_section.first_child_matching_class(nodes.title)
            ]

            item = objectivesindex_item()
            item += objectivesindex_name(
                "", title.astext(), parent_section_ref=parent_section["ids"][0]
            )
            item += objectivesindex_body(
                "", *[child.deepcopy() for child in o.children]
            )

            items += [item]

        return items


def visit_objectivesindex(self, node: objectivesindex) -> None:
    self.body.append(
        self.starttag(
            node,
            "dl",
            classes=["objectivesindex", "list-group"],
        )
    )


def depart_objectivesindex(self, node: objectivesindex) -> None:
    self.body.append("</dl>\n")


def visit_objectivesindex_item(self, node: objectivesindex_item) -> None:
    self.body.append('<div class="objectivesindex-item list-group-item">\n')


def depart_objectivesindex_item(self, node: objectivesindex_item) -> None:
    self.body.append("</div>\n")


def visit_objectivesindex_name(self, node: objectivesindex_name) -> None:
    self.body.append(self.starttag(node, "dt", classes=["h5"]))
    self.body.append(f'<a href="#{node["parent_section_ref"]}">\n')


def depart_objectivesindex_name(self, node: objectivesindex_name) -> None:
    self.body.append("</a>")
    self.body.append("</dt>\n")


def visit_objectivesindex_body(self, node: objectivesindex_body) -> None:
    self.body.append(self.starttag(node, "dd"))


def depart_objectivesindex_body(self, node: objectivesindex_body) -> None:
    self.body.append("</dd>\n")


def ignore_node(self, _) -> None:
    raise nodes.SkipNode


def setup(app: "Sphinx") -> Dict[str, Any]:
    app.add_node(objectives, html=(visit_objectives, depart_objectives))
    app.add_node(
        objectivesindex, html=(visit_objectivesindex, depart_objectivesindex)
    )
    app.add_node(
        objectivesindex_item,
        html=(visit_objectivesindex_item, depart_objectivesindex_item),
    )
    app.add_node(
        objectivesindex_name,
        html=(visit_objectivesindex_name, depart_objectivesindex_name),
    )
    app.add_node(
        objectivesindex_body,
        html=(visit_objectivesindex_body, depart_objectivesindex_body),
    )

    app.add_directive("objectives", Objectives)
    app.add_directive("objectivesindex", ObjectivesIndex)

    app.add_transform(ObjectivesIndexTransformer)
