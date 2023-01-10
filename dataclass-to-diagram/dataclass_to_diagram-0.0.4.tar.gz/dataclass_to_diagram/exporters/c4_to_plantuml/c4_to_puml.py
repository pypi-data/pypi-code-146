from typing import Final, Iterable

from dataclass_to_diagram.models import c4

from .context_to_puml import context_to_puml
from .container_to_puml import container_to_puml
from .rel_to_puml import rel_to_puml
from .sprites_to_puml import sprites_to_puml
from .tag_to_puml import element_tag_to_puml, relation_tag_to_puml

TEMPLATE: Final[
    str
] = """@startuml
!include C4_Dynamic.puml{sprites}{element_tags}{relation_tags}{contexts}{containers}{relations}{legend}
@enduml
"""


def _export_legend(show_legend: bool) -> str:
    if not show_legend:
        return ""
    return "\n\nSHOW_LEGEND()"


def _export_element_tag_declaration(tags: Iterable[c4.tag.ElementTag]) -> str:
    if not tags:
        return ""
    tags_list_str = [element_tag_to_puml(tag) for tag in tags]
    tags_str = "\n".join(sorted(tags_list_str))
    return "\n\n{0}".format(tags_str)


def _export_rel_tag_declaration(tags: Iterable[c4.tag.RelationTag]) -> str:
    if not tags:
        return ""
    tags_list_str = [relation_tag_to_puml(tag) for tag in tags]
    tags_str = "\n".join(sorted(tags_list_str))
    return "\n\n{0}".format(tags_str)


def c4_to_puml(diagram: c4.C4):
    if diagram.contexts:
        contexts_list: list[str] = [
            context_to_puml(context) for context in diagram.contexts
        ]
        contexts_str = "\n\n" + "\n".join(contexts_list)
    else:
        contexts_str = ""
    if diagram.containers:
        containers_list: list[str] = [
            container_to_puml(container) for container in diagram.containers
        ]
        containers_str = "\n\n" + "\n".join(containers_list)
    else:
        containers_str = ""
    if diagram.relations:
        rel_list: list[str] = [rel_to_puml(rel) for rel in diagram.relations]
        relations_str = "\n\n" + "\n".join(rel_list)
    else:
        relations_str = ""
    return TEMPLATE.format(
        sprites=sprites_to_puml(diagram.find_all_sprites()),
        element_tags=_export_element_tag_declaration(
            diagram.find_all_element_tags(),
        ),
        relation_tags=_export_rel_tag_declaration(
            diagram.find_all_relation_tags(),
        ),
        contexts=contexts_str,
        containers=containers_str,
        relations=relations_str,
        legend=_export_legend(diagram.show_legend),
    )
