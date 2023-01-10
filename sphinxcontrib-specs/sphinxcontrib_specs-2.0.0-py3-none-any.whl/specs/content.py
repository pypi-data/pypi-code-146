"""sphinxcontrib.specs.content"""

from cgitb import html
from typing import TYPE_CHECKING, Dict, Any, List

from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class specscontent(nodes.General, nodes.Element):
    pass


class specscontent_title(nodes.Part, nodes.TextElement):
    pass


class specscontent_body(nodes.General, nodes.Element):
    pass


def visit_specscontent(self, node: specscontent) -> None:
    self.body.append(
        f'<a class="specscontent-link text-body my-2 d-block" target="_blank" href="{node["link"]}">\n'
    )
    self.body.append(
        self.starttag(node, "div", classes=node["classes"] + ["card"])
    )
    self.body.append('<div class="row g-0">\n')
    self.body.append('<div class="col-1">\n')
    self.body.append(
        '<div class="h-100 bg-secondary rounded-start specscontent-icon text-light">\n'
    )
    self.body.append(node["icon_markup"])
    self.body.append("</div>\n")
    self.body.append("</div>\n")


def depart_specscontent(self, _) -> None:
    self.body.append("</div>\n")
    self.body.append("</div>\n")
    self.body.append("</a>\n")


def visit_specscontent_title(self, node: specscontent_title) -> None:
    self.body.append(self.starttag(node, "div", classes=node["classes"]))


def depart_specscontent_title(self, _) -> None:
    self.body.append("</div>\n")


def visit_specscontent_body(self, node: specscontent_body) -> None:
    self.body.append('<div class="col">\n')
    self.body.append(self.starttag(node, "div", classes=node["classes"]))


def depart_specscontent_body(self, _) -> None:
    self.body.append("</div>\n")
    self.body.append("</div>\n")


class BaseContentDirective(SphinxDirective):
    contenttype_name = ""
    contenttype_icon_markup = ""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {"link": directives.unchanged}
    has_content = True

    def run(self) -> List[Node]:
        node = specscontent(classes=["specscontent", self.contenttype_name])

        node["contenttype"] = self.contenttype_name
        node["link"] = self.options.get("link", "")

        icon_overrides = self.env.config.specs_contenttype_icons
        default_markup = self.contenttype_icon_markup
        node["icon_markup"] = (
            icon_overrides[self.contenttype_name]
            if self.contenttype_name in icon_overrides
            else default_markup
        )

        body_node = specscontent_body("", classes=["card-body"])

        title_text = self.arguments[0]
        text_nodes, messages = self.state.inline_text(title_text, self.lineno)
        title_node = specscontent_title(
            title_text,
            "",
            *text_nodes,
            classes=["specscontent-body-title", "card-title", "h6"],
        )
        (
            title_node.source,
            title_node.line,
        ) = self.state_machine.get_source_and_line(self.lineno)
        body_node += [title_node]

        if self.content:
            desc_node = nodes.container(
                "\n".join(self.content), classes=["specscontent-body"]
            )
            desc_node.document = self.state.document
            self.state.nested_parse(
                self.content, self.content_offset, desc_node
            )

            for child in desc_node.children:
                child["classes"].append("card-text")

            body_node += desc_node.children

        node += [body_node]

        return [node]


class Download(BaseContentDirective):
    contenttype_name = "download"
    contenttype_icon_markup = """\
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="currentColor" class="bi bi-cloud-download" viewBox="0 0 16 16">
  <path d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
  <path d="M7.646 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V5.5a.5.5 0 0 0-1 0v8.793l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z"/>
</svg>"""


class Video(BaseContentDirective):
    contenttype_name = "video"
    contenttype_icon_markup = """\
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="currentColor" class="bi bi-play-circle-fill" viewBox="0 0 16 16">
  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM6.79 5.093A.5.5 0 0 0 6 5.5v5a.5.5 0 0 0 .79.407l3.5-2.5a.5.5 0 0 0 0-.814l-3.5-2.5z"/>
</svg>"""


class Webpage(BaseContentDirective):
    contenttype_name = "webpage"
    contenttype_icon_markup = """\
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="currentColor" class="bi bi-link-45deg" viewBox="0 0 16 16">
  <path d="M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1.002 1.002 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4.018 4.018 0 0 1-.128-1.287z"/>
  <path d="M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243L6.586 4.672z"/>
</svg>"""


def setup(app: "Sphinx") -> Dict[str, Any]:
    app.add_config_value("specs_contenttype_icons", {}, "env")

    app.add_node(specscontent, html=(visit_specscontent, depart_specscontent))
    app.add_node(
        specscontent_title,
        html=(visit_specscontent_title, depart_specscontent_title),
    )
    app.add_node(
        specscontent_body,
        html=(visit_specscontent_body, depart_specscontent_body),
    )

    for directive in [Download, Video, Webpage]:
        app.add_directive(directive.contenttype_name, directive)
