from typing import Final

from dataclass_to_diagram.models.c4.base import BaseRel

from .args_dict_to_str import args_dict_to_str

TEMPLATE: Final[str] = "{class_name}({args})"


def rel_to_puml(rel: BaseRel) -> str:
    args: dict[str, str] = {}
    args["$from"] = str(rel.begin.alias)
    args["$to"] = str(rel.end.alias)
    args["$label"] = '"{0}"'.format(rel.label)
    if rel.techn:
        args["$techn"] = '"{0}"'.format(rel.techn)
    if rel.descr:
        args["$descr"] = '"{0}"'.format(rel.descr)
    if rel.link:
        args["$link"] = '"{0}"'.format(rel.link)
    if rel.tags:
        tag_names: list[str] = [tag.tag_stereo for tag in rel.tags]
        args["$tags"] = '"{0}"'.format("+".join(sorted(tag_names)))
    args_str = args_dict_to_str(args)
    return TEMPLATE.format(
        class_name=rel.class_name_str,
        args=args_str,
    )
