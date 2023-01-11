from . import Definition
from .add_node_dialog import AddNodeDialog
from .node_proxy import NodeProxy
from p3ui import *
from ._config import *
from .template_tree_template import TemplateTreeTemplate
from ..element import Icons


class TemplateTreeItem(Row):
    """ row with background color, indentation and two text items """

    def __init__(self, editor):
        self.editor = editor
        self.node = None
        self.indent = 0

        super().__init__(
            background_color=self.eval_background,
            on_mouse_down=self._on_select,
            on_mouse_enter=self._on_mouse_enter,
            on_mouse_move=self._on_mouse_enter,
            #            on_mouse_leave=self._on_mouse_leave,
            padding=(0.618 | em, 0.618 | em),
            spacing=0 | px,
            align_items=Alignment.Stretch,
            justify_content=Justification.Start,
            children=[
                Spacer(width=lambda: (1.5 * model.item[1] | em, 0, 0)),
                Text(
                    value=self.eval_class_name,
                    color=lambda: '#555555' if not self.proxy else 'black' if self.is_hovered else None,
                ),
                Text(
                    value=self.eval_template_name,
                    color=lambda: '#555555' if not self.proxy else 'black' if self.is_hovered else emphasize_color,
                ),
                Text(
                    value=self.eval_identifier_name,
                    #                    color='#BA55D3'
                    color='#888888ff'
                )
            ]
        )

    def _on_select(self, _):
        self.editor.selected_node = None if self.editor.selected_node is self.node else self.node

    def _on_mouse_enter(self, e):
        if self.editor.active_node != self.node:
            self.editor.active_node = self.node

    def _on_mouse_leave(self, e):
        self.editor.active_node = None

    @property
    def proxy(self) -> NodeProxy:
        return self.editor.module_proxy.proxy_for_node(self.node) if self.editor.module_proxy else None

    @property
    def is_hovered(self) -> bool:
        if self.proxy:
            return self.proxy is self.editor.module_proxy.proxy_for_node(self.editor.active_node)
        else:
            return self.node == self.editor.active_node

    @property
    def is_selected(self) -> bool:
        if self.proxy:
            return self.proxy is self.editor.module_proxy.proxy_for_node(self.editor.selected_node)
        else:
            return self.node == self.editor.selected_node

    @property
    def is_template(self):
        return Definition.is_template_class(type(self.node))

    def eval_background(self):
        return active_color if self.is_hovered else selected_color if self.is_selected else '#77777711' if model.index % 2 == 0 else '#77777705'

    def eval_identifier_name(self):
        if self.proxy is None:
            return ''
        id = ' = ' + self.proxy.identifier if self.proxy.identifier else ''
        return id + f'  ({len(self.proxy.instances)})'

    def eval_class_name(self):
        t = type(self.node)
        t = t.Definition.node_type if Definition.is_template_class(t) else t
        # Icons.LibraryBooks, Icons.SubdirectoryArrowRight
        return f'{Icons.Layers if self.is_template else Icons.LabelOutline} {t.__name__}'

    def eval_template_name(self):
        return ' ' + type(self.node).__name__ if Definition.is_template_class(type(self.node)) else ''


class TemplateTreeController:

    def __init__(self, template: TemplateTreeTemplate, editor):
        self.template, self.editor = template, editor

        template.unique.add_node_button.on_click = AddNodeDialog.Instance.show
        template.unique.move_down_button.on_click = editor.move_selected_node_down
        template.unique.move_up_button.on_click = editor.move_selected_node_up
        template.unique.delete_button.on_click = editor.remove_selected_node
        template.unique.cut_button.on_click = self.editor.cut_selected
        template.unique.copy_button.on_click = self.editor.copy_selected
        template.unique.paste_button.on_click = self.editor.paste_selected
        # self.template.unique.paste_button.disabled = True

        self._repeater = Repeater(
            target_container=template.unique.tree_view,  # ScrolledColumn..
            delegate=lambda: TemplateTreeItem(self.editor),
            delegate_init=lambda index, item, delegate: setattr(delegate, 'node', item[0]),
            model=lambda: self._flatten_tree(self.editor.node_tree)
        )

        template.unique.tree_view.on_mouse_leave = self._on_mouse_leave

        self.template.eval()
        self.template.eval = self.eval

    def _on_mouse_leave(self, _):
        self.editor.active_node = None

    def _flatten_tree(self, node, indent=0):
        if node is None:
            return
        yield node, indent
        for child in node.children:
            for tree_item, tree_item_indent in self._flatten_tree(child, indent + 1):
                yield tree_item, tree_item_indent

    def eval(self):
        self.template.unique.add_node_button.disabled = self.editor.selected_node is None

        proxy: NodeProxy = self.editor.selected_node_proxy
        if proxy is None:
            self.template.unique.move_down_button.disabled = True
            self.template.unique.move_up_button.disabled = True
            self.template.unique.delete_button.disabled = True
            self.template.unique.cut_button.disabled = True
            self.template.unique.copy_button.disabled = True
            self.template.unique.paste_button.disabled = True
        else:
            self.template.unique.move_down_button.disabled = not proxy.can_move_down_as_sibling
            self.template.unique.move_up_button.disabled = not proxy.can_move_up_as_sibling
            self.template.unique.delete_button.disabled = proxy.definition.parent is None
            self.template.unique.cut_button.disabled = False
            self.template.unique.copy_button.disabled = False
            self.template.unique.paste_button.disabled = self.editor.clipboard_node is None or \
                                                         not proxy.can_contain(self.editor.clipboard_node)

        self._repeater.eval(self._repeater.model)
