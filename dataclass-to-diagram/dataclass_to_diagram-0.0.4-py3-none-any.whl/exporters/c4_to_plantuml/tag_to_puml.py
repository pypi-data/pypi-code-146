from typing import Final

from dataclass_to_diagram.models.c4.base import BaseTag
from dataclass_to_diagram.models.c4.tag import (
    ElementTag,
    RelationTag,
)

from .args_dict_to_str import args_dict_to_str


def _base_tag_to_puml(tag: BaseTag) -> dict[str, str]:
    args: dict[str, str] = {}
    args["$tagStereo"] = '"{0}"'.format(tag.tag_stereo)
    if tag.legend_text:
        args["$legendText"] = '"{0}"'.format(tag.legend_text)
    return args


ELEMENT_TAG: Final[str] = "AddElementTag({args})"
RELATION_TAG: Final[str] = "AddRelTag({args})"


def element_tag_to_puml(tag: ElementTag) -> str:
    args: dict[str, str] = _base_tag_to_puml(tag)
    if tag.bg_color:
        args["$bgColor"] = '"{0}"'.format(tag.bg_color)
    if tag.font_color:
        args["$fontColor"] = '"{0}"'.format(tag.font_color)
    if tag.border_color:
        args["$borderColor"] = '"{0}"'.format(tag.border_color)
    if tag.shadowing:
        args["$shadowing"] = '"{0}"'.format(tag.shadowing)
    if tag.shape:
        args["$shape"] = '"{0}"'.format(tag.shape)
    if tag.sprite:
        args["$sprite"] = '"{0}"'.format(tag.sprite)
    if tag.font_color:
        args["$fontColor"] = '"{0}"'.format(tag.font_color)
    args_str = args_dict_to_str(args)
    return ELEMENT_TAG.format(args=args_str)


def relation_tag_to_puml(tag: RelationTag) -> str:
    args: dict[str, str] = _base_tag_to_puml(tag)
    if tag.text_color:
        args["$textColor"] = '"{0}"'.format(tag.text_color)
    if tag.line_color:
        args["$lineColor"] = '"{0}"'.format(tag.line_color)
    if tag.line_style:
        args["$lineStyle"] = '"{0}"'.format(tag.line_style)
    if tag.sprite:
        args["$sprite"] = '"{0}"'.format(tag.sprite)
    if tag.techn:
        args["$techn"] = '"{0}"'.format(tag.techn)
    if tag.legend_sprite:
        args["$legendSprite"] = '"{0}"'.format(tag.legend_sprite)
    if tag.line_thickness:
        args["$lineThickness"] = '"{0}"'.format(tag.line_thickness)
    args_str = args_dict_to_str(args)
    return RELATION_TAG.format(args=args_str)
