import asyncio
from typing import Type, Callable, List

from .add_icon_dialog import AddIconDialog
from .. import Icons
from ..binding.boolean_binding import OptionalBooleanBinding, BooleanBinding
from ..native import *
from p3ui.binding import *

from .node_proxy import NodeProxy


class AttributeEditorFactory:
    class Group:

        def __init__(self, name, weight, topics: List):
            self.name = name
            self.weight = weight
            self.topics = topics

        def __le__(self, other):
            return self.weight <= other.weight

        def __lt__(self, other):
            return self.weight <= other.weight

    class Topic:

        def __init__(self, name, weight):
            self.name = name
            self.weight = weight

        def __le__(self, other):
            return self.weight <= other.weight

        def __lt__(self, other):
            return self.weight <= other.weight

    Topics = [
        InputText := Topic('data', 200),
        Identification := Topic('definition', 200),
        Text := Topic('text', 200),
        Main := Topic('main', 200),
        Width := Topic('width', 100),
        Height := Topic('height', 90),
        Positioning := Topic('absolute positioning (experimental)', 80),
        Flexible := Topic('flexible', 70),
        Spacer := Topic('space', 65),
        Coloring := Topic('coloring', 60),
    ]

    Groups = [
        Template := Group('Template', 9999, [
            Identification
        ]),
        StateGroup := Group('State', 1000, [
            Text,
            Main,
            Coloring
        ]),
        PositionAndSize := Group('Position & Size', 10, [
            Width,
            Height,
            Positioning
        ]),
        ContentGroup := Group('Content', 11, [
            Flexible,
            Spacer,
        ]),
        ModelGroup := Group('Main', 1000, [
            InputText
        ]),
        OtherGroup := Group('other', 0, [

        ])
    ]

    class Definition:

        def __init__(self, node_type: Type, creator):
            self.node_type: Type = node_type
            self.creator = creator

    definitions: List[Definition] = []

    @staticmethod
    def add_strategy(node_type: Type, creator: Callable):
        AttributeEditorFactory.definitions.append(AttributeEditorFactory.Definition(
            node_type=node_type,
            creator=creator
        ))

    @staticmethod
    def iterate(proxy: NodeProxy):
        for definition in AttributeEditorFactory.definitions:
            if issubclass(proxy.definition.node_type, definition.node_type):
                for item in definition.creator(proxy):
                    yield item

    @staticmethod
    def group_of_topic(topic):
        for group in AttributeEditorFactory.Groups:
            if topic in group.topics:
                return group
        return AttributeEditorFactory.OtherGroup

    @staticmethod
    def create(proxy: NodeProxy):
        groups = dict()
        for attribute_name, topic, attribute, elements in AttributeEditorFactory.iterate(proxy):
            group = AttributeEditorFactory.group_of_topic(topic)
            if group not in groups:
                groups[group] = dict()
            if topic not in groups[group]:
                groups[group][topic] = dict()
            groups[group][topic][attribute] = (attribute_name, elements)
        #
        # flatten & order
        flattened_and_sorted_groups = []
        for group_key, group in groups.items():
            group_topics = []
            for topic, attributes in group.items():
                topic_elements = []
                for element_name, elements in attributes.items():
                    topic_elements.append((element_name, elements))
                group_topics.append((topic, topic_elements))
            group_topics = sorted(group_topics, key=lambda t: t[0].weight, reverse=True)
            flattened_and_sorted_groups.append((group_key, group_topics))
        flattened_and_sorted_groups = sorted(flattened_and_sorted_groups, reverse=True)
        return flattened_and_sorted_groups


def _input_text_attribute_creator(node):
    yield 'value', AttributeEditorFactory.InputText, 'text', [
        StringAttribute(node.attributes, 'value')
    ]


AttributeEditorFactory.add_strategy(node_type=InputText, creator=_input_text_attribute_creator)
AttributeEditorFactory.add_strategy(node_type=Text, creator=_input_text_attribute_creator)


def _layout_attribute_creator(node_proxy):
    yield 'direction', AttributeEditorFactory.Flexible, 'direction', [
        EnumAttribute(Direction, node_proxy.attributes, 'direction')
    ]

    yield 'align_items', AttributeEditorFactory.Flexible, 'align', [
        EnumAttribute(Alignment, node_proxy.attributes, 'align_items')
    ]

    yield 'justify_content', AttributeEditorFactory.Flexible, 'justify', [
        EnumAttribute(Justification, node_proxy.attributes, 'justify_content')
    ]

    yield 'background_color', AttributeEditorFactory.Coloring, 'bg color', [
        OptionalAttribute(node_proxy.attributes, 'background_color', children=[
            Spacer(width=(1 | em, 1, 0)),
            ColorAttribute(node_proxy.attributes, 'background_color'),
            Spacer(width=(1 | em, 1, 0))
        ], default_to='#55555555')
    ]

    proxy = LengthAttributeProxy(node_proxy.attributes, 'spacing')
    yield 'spacing', AttributeEditorFactory.Spacer, 'spacing', [
        OptionalAttribute(node_proxy.attributes, 'spacing', children=[
            FloatAttribute(proxy, 'value'),
            UnitAttribute(proxy, 'unit')
        ], default_to=0 | px)
    ]

    proxy = LengthPairAttributeProxy(node_proxy.attributes, 'padding')
    yield 'padding', AttributeEditorFactory.Spacer, 'padding x', [
        OptionalAttribute(node_proxy.attributes, 'padding', children=[
            FloatAttribute(proxy, 'value_x'),
            UnitAttribute(proxy, 'unit_x')
        ], default_to=(1 | em, 1 | em))
    ]

    yield 'padding', AttributeEditorFactory.Spacer, 'padding y', [
        OptionalAttribute(node_proxy.attributes, 'padding', children=[
            FloatAttribute(proxy, 'value_y'),
            UnitAttribute(proxy, 'unit_y')
        ], default_to=(1 | em, 1 | em))
    ]


AttributeEditorFactory.add_strategy(node_type=Layout, creator=_layout_attribute_creator)


def _node_attribute_creator(node_proxy):
    yield 'identifier', AttributeEditorFactory.Identification, 'name', [
        StringAttribute(node_proxy, 'identifier')
    ]

    label_input = StringAttribute(node_proxy.attributes, 'label')
    async def insert():
        icon = await AddIconDialog.Instance.get()
        if icon is None:
            return
        label_input.focus()
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        it = label_input
        while it:
            if isinstance(it, UserInterface):
                break
            it = it.parent
        if not isinstance(it, UserInterface):
            return
        it.add_input_character(ord(icon))

    if node_proxy.definition.node_type is not Layout:
        yield 'label', AttributeEditorFactory.Main, 'label', [
            OptionalAttribute(node_proxy.attributes, 'label', children=[
                label_input,
                Button(width=(auto, 0, 0), label=f'{Icons.Image}', on_click=insert)
            ], default_to='')
        ]

    width_basis_proxy = LengthAttributeProxy(node_proxy.attributes, 'width_basis')
    yield 'width_basis', AttributeEditorFactory.Width, 'basis', [
        OptionalAttribute(node_proxy.attributes, 'width_basis', children=[
            FloatAttribute(width_basis_proxy, 'value'),
            UnitAttribute(width_basis_proxy, 'unit')
        ], default_to=1 | em)
    ]

    yield 'width_grow', AttributeEditorFactory.Width, 'grow', [
        FloatAttribute(node_proxy.attributes, 'width_grow')
    ]
    yield 'width_shrink', AttributeEditorFactory.Width, 'shrink', [
        FloatAttribute(node_proxy.attributes, 'width_shrink')
    ]
    height_basis_proxy = LengthAttributeProxy(node_proxy.attributes, 'height_basis')
    yield 'height_basis', AttributeEditorFactory.Height, 'basis', [
        OptionalAttribute(node_proxy.attributes, 'height_basis', children=[
            FloatAttribute(height_basis_proxy, 'value'),
            UnitAttribute(height_basis_proxy, 'unit')
        ], default_to=1 | em)
    ]
    yield 'height_grow', AttributeEditorFactory.Height, 'grow', [
        FloatAttribute(node_proxy.attributes, 'height_grow')
    ]
    yield 'height_shrink', AttributeEditorFactory.Height, 'shrink', [
        FloatAttribute(node_proxy.attributes, 'height_shrink')
    ]

    yield 'position', AttributeEditorFactory.Positioning, 'position', [
        EnumAttribute(Position, node_proxy.attributes, 'position')
    ]

    yield 'color', AttributeEditorFactory.Coloring, 'fg color', [
        OptionalAttribute(node_proxy.attributes, 'color', children=[
            Spacer(width=(1 | em, 1, 0)),
            ColorAttribute(node_proxy.attributes, 'color'),
            Spacer(width=(1 | em, 1, 0))
        ], default_to='#55555555')
    ]

    left_attribute_proxy = LengthAttributeProxy(node_proxy.attributes, 'left')
    yield 'left', AttributeEditorFactory.Positioning, 'left', [
        OptionalAttribute(node_proxy.attributes, 'left', children=[
            FloatAttribute(left_attribute_proxy, 'value'),
            UnitAttribute(left_attribute_proxy, 'unit')
        ], default_to=0 | px)
    ]

    top_attribute_proxy = LengthAttributeProxy(node_proxy.attributes, 'top')
    yield 'top', AttributeEditorFactory.Positioning, 'top', [
        OptionalAttribute(node_proxy.attributes, 'top', children=[
            FloatAttribute(top_attribute_proxy, 'value'),
            UnitAttribute(top_attribute_proxy, 'unit')
        ], default_to=0 | px)
    ]

    yield 'visible', AttributeEditorFactory.Main, 'visible', [
        BooleanBinding(node_proxy.attributes, 'visible')
    ]
    yield 'disabled', AttributeEditorFactory.Main, 'disabled', [
        BooleanBinding(node_proxy.attributes, 'disabled')
    ]


AttributeEditorFactory.add_strategy(node_type=Node, creator=_node_attribute_creator)
