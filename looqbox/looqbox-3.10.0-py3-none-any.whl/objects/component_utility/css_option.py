from dataclasses import dataclass
from looqbox.objects.component_utility.css import Css
from looqbox.objects.component_utility.flex_css import FlexCss
from looqbox.objects.component_utility.layout_css import LayoutCss
from looqbox.objects.component_utility.positional_css import PositionalCss
from looqbox.objects.component_utility.self_positional import SelfPositional
from looqbox.objects.component_utility.text_css import TextCss

"""
Draft with use example

import CssOptions as css

css_properties = [css.TextAlignLeft, css.BackgroundColor("Black")]

for p in css_properties:
    print(p.property + " : " + p.value)
    
"""


@dataclass(slots=True)
class CssOption:

    AlignContent = PositionalCss("alignContent", "center")
    AlignItems = PositionalCss("alignItems", "center")
    AlignSelf = SelfPositional("alignSelf", "center")
    Animation = Css("animation", None)
    Background = Css("background", None)
    BackgroundColor = Css("backgroundColor", None)
    Border = Css("border", None)
    BorderColor = Css("borderColor", None)
    BorderRadius = Css("borderRadius", None)
    BorderWidth = Css("borderWidth", None)
    BoxShadow = Css("boxShadow", None)
    BoxSizing = Css("boxSizing", None)
    Color = Css("color", None)
    Flex = Css("flex", None)
    FlexDirection = FlexCss("flexDirection", None)
    FlexWrap = Css("flexWrap", None)
    FontFamily = Css("fontFamily", None)
    FontSize = Css("fontSize", None)
    FontWeight = Css("fontWeight", None)
    Height = Css("height", None)
    JustifyContent = PositionalCss("justifyContent", "space-between")
    LetterSpacing = Css("letterSpacing", None)
    LineHeight = Css("lineHeight", None)
    Margin = LayoutCss("margin", None)
    MaxHeight = Css("maxHeight", None)
    MaxWidth = Css("maxWidth", None)
    MinHeight = Css("minHeight", None)
    MinWidth = Css("minWidth", None)
    Overflow = Css("overflow", None)
    Padding = LayoutCss("padding", None)
    Position = Css("position", None)
    Scale = Css("scale", None)
    TextAlign = TextCss("textAlign", "start")
    TextDecoration = Css("textDecoration", None)
    TextOverflow = Css("textOverflow", None)
    Transform = Css("transform", None)
    TransformOrigin = Css("transformOrigin", None)
    WhiteSpace = Css("whiteSpace", None)
    Width = Css("width", None)
    ZIndex = Css("zIndex", None)

    @classmethod
    def export(cls, css_options):
        if css_options is None:
            return []
        return {
            css.property: css.value
            for css in css_options if css.value is not None
        }

    @classmethod
    def add(cls, css_options, option):
        if css_options is None:
            css_options = [option]
        else:
            css_options = list(set(css_options).union({option}))
        return css_options

    @classmethod
    def clear(cls, css_options, option):
        if css_options is None:
            return css_options
        css_options = list(set(css_options).difference(set(option)))
        return css_options
