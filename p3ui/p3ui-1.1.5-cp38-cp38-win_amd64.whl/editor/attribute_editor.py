from .. import Icons
from ..native import *
from ._config import *
from .attribute_editor_factory import AttributeEditorFactory


class AttributeEditorEditRow(Row):

    def __init__(self, proxy, attribute_name, left, right, **kwargs):
        def attribute_is_set():
            return proxy.attribute_is_set(attribute_name)

        def force_attribute_set(yes):
            proxy.set_attribute_enabled(attribute_name, yes)
            self.eval()

        super().__init__(
            padding=(0.618 | em, 4 | px),
            spacing=0.618 | em,
            width=(0 | em, 0, 0),
            height=(2 | em, 0, 0),
            background_color=list_background_color_odd,
            **kwargs,
            children=[
                Row(
                    padding=(AttributeEditor.Padding | em, AttributeEditor.Padding | em),
                    align_items=Alignment.Center,
                    justify_content=Justification.End,
                    width=(1 | em, 0.382, 1),
                    children=[
                                 check_box := CheckBox(
                        width=(auto, 0, 0),
                        value=attribute_is_set,
                        on_change=force_attribute_set,
                    )] + left + [Spacer(width=(1 | em, 1, 0))]
                ),
                Row(
#                    padding=(AttributeEditor.Padding | em, AttributeEditor.Padding | em),
                    align_items=Alignment.Center,
                    width=(1 | em, 0.618, 1),
                    children=right,
                    # disabled=lambda: not attribute_is_set(),
                    # opacity=lambda: 0.5 if not attribute_is_set() else None
                )
            ]
        )
        if attribute_name == 'identifier':
            check_box.opacity = 0.
            check_box.disabled = True


class AttributeEditorSpacerRow(Row):

    def __init__(self, **kwargs):
        super().__init__(
            background_color=list_background_color_odd,
            height=(1 | em, 0, 0),
            align_items=Alignment.Center,
            justify_content=Justification.Start,
            **kwargs
        )


class AttributeEditorTopicRow(Row):

    def __init__(self, **kwargs):
        super().__init__(
            background_color=kwargs.pop('background_color', list_background_color_even),
            height=(2 | em, 0, 0),
            padding=(0.618 | em, 0.618 | em),
            align_items=Alignment.Center,
            justify_content=Justification.Start,
            **kwargs
        )


class AttributeEditorGroupRow(Row):

    def __init__(self, **kwargs):
        super().__init__(
            background_color='black',
            height=(2 | em, 0, 0),
            padding=(0.618 | em, 0.618 | em),
            align_items=Alignment.Center,
            justify_content=Justification.Start,
            **kwargs
        )


class AttributeEditor:
    Padding = 0 | em

    def __init__(self, editor, template):
        self.editor, self.template = editor, template
        self._eval = template.eval
        self._proxy = None
        template.eval = self.eval

        self.eval()

    def make_interface(self):
        self.template.unique.scrolled_column.clear()
        if self._proxy is None:
            return
        groups = AttributeEditorFactory.create(self._proxy)
        for group, topics in groups:
            self.template.unique.scrolled_column.add(
                AttributeEditorGroupRow(
                    children=[Text(color=emphasize_color, value=f'{Icons.Label} {group.name}')]
                )
            )
            for topic, topic_group in topics:
                self.template.unique.scrolled_column.add(AttributeEditorSpacerRow())
                self.template.unique.scrolled_column.add(
                    AttributeEditorTopicRow(
                        children=[Text(f'{topic.name}', color=emphasize_color)]
                    )
                )
                self.template.unique.scrolled_column.add(AttributeEditorSpacerRow())
                for name, elements in topic_group:
                    self.template.unique.scrolled_column.add(
                        AttributeEditorEditRow(
                            self._proxy,
                            elements[0],
                            left=[Text(f' {name}')],
                            right=elements[1]
                        )
                    )
                self.template.unique.scrolled_column.add(AttributeEditorSpacerRow())
            self.template.unique.scrolled_column.add(AttributeEditorSpacerRow())

    def eval(self):
        proxy = self.editor.selected_node_proxy
        if proxy != self._proxy:
            self._proxy = proxy
            self.make_interface()
        self._eval()
