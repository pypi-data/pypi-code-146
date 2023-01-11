from p3ui.element.dialog import Dialog
import inspect
import p3ui as p3
from p3ui import *
from p3ui.element.scrolled_column import ScrolledColumn
from .node_proxy import NodeProxy
from ..element import Icons
from ._config import *


def list_node_classes(*module_list):
    for module in module_list:
        for name in dir(module):
            if not name[0].isalpha() or not name[0].isupper():
                continue
            node_type = getattr(module, name)
            if inspect.isclass(node_type) and issubclass(node_type, p3.Node) and node_type is not p3.Node:
                yield node_type, module.__name__


class AddNodeDialog(Dialog):

    Instance = None

    def __init__(self, editor):
        self.editor = editor
        self._selected = None

        dialog = self

        class Item(Row):

            def __init__(self):
                self.item = None
                super().__init__(
                    padding=(0.618 | em, 0.618 | em),
                    children=[
                        Text(
                            value=lambda: f'{Icons.Layers if Definition.is_template_class(model.item[0]) else Icons.LabelOutline} {model.item[0].__name__}',
                        ),
                        Text(
                            value=lambda: f' ({model.item[1]})'
                        )
                    ],
                    background_color=lambda: self.eval_background_color(),
                    on_mouse_down=lambda _: setattr(dialog, 'selected', self.item[0]),
                    on_mouse_enter=lambda _: self.parent.parent.eval(),
                    on_mouse_leave=lambda _: self.parent.parent.eval()
                )

            def eval_background_color(self):
                return active_color if self.hover else selected_color if dialog.selected == model.item[
                    0] else list_background_color_even if model.index % 2 == 0 else list_background_color_odd

        super().__init__(
            label='Add Item',
            width=(30 | em, 0, 0),
            height=(30 | em, 0, 0),
            content=Column(children=[
                Column(
                    height=(auto, 0, 0),
                    children=[
                        Row(
                            padding=(0 | px, 0 | px),
                            justify_content=Justification.Start,
                            children=[
                                show_templates_check_box := CheckBox(
                                    width=(auto, 0, 0),
                                    label='Templates',
                                    value=True,
                                    on_change=lambda _: self.eval()
                                ),
                                show_nodes_check_box := CheckBox(
                                    width=(auto, 0, 0),
                                    label='Nodes',
                                    value=True,
                                    on_change=lambda _: self.eval()
                                ),
                            ]
                        ),
                        search_box := InputText(label=f'{Icons.Search}', on_change=self.eval),
                    ]
                ),
                column := ScrolledColumn(),
                identifier_input := InputText(label='Identifier'),
                create_button := Button(
                    label='create',
                    disabled=lambda: self.selected is None,
                    on_click=self._on_create
                )
            ])
        )
        self.identifier_input = identifier_input
        self.create_button = create_button
        self.show_nodes_check_box = show_nodes_check_box
        self.show_templates_check_box = show_templates_check_box
        self.search_box = search_box

        self.repeater = Repeater(
            target_container=column,
            delegate=Item,
            model=self.filtered_iterator,
            delegate_init=lambda _, item, delegate: setattr(delegate, 'item', item)
        )
        self.column = column

    def _on_create(self):
        proxy: NodeProxy = self.editor.selected_node_proxy
        if proxy is None:
            return
        proxy.add_child(self.selected, self.identifier_input.value)

    def filtered_iterator(self):
        if self.editor is None:
            return
        if self.editor.module_proxy is None:
            return
        search_string = self.search_box.value.lower()

        if self.show_nodes_check_box.value:
            for cls, module_name in list_node_classes(p3):
                if search_string and search_string not in cls.__name__.lower():
                    continue
                yield cls, module_name
        if self.show_templates_check_box.value:
            for cls in self.editor.module_proxy.templates:
                if search_string and search_string not in cls.__name__.lower():
                    continue
                yield cls, 'custom'

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.eval()

    async def show(self):
        self.selected = None
        await super().show()
        self.eval()
