from p3ui import Column, px, Alignment, Justification, Position
from ._config import *


class Highlight(Column):

    def __init__(self, node, holder, **kwargs):
        super().__init__(
            position=Position.Absolute,
            align_items=Alignment.Center,
            justify_content=Justification.Center,
            left=node.x - holder.x | px,
            top=node.y - holder.y | px,
            width=(node.size[0] | px, 0, 0),
            height=(node.size[1] | px, 0, 0),
            **kwargs
        )


class EditorHighlighting:

    def __init__(self, editor: 'Editor'):
        self.editor = editor
        self.holder = editor.root_node.unique.highlight_root
        self._active_mark = []
        self._selected_mark = []

    def clear(self):
        for item in self._active_mark:
            item.parent.remove(item)
        self._active_mark.clear()
        for item in self._selected_mark:
            item.parent.remove(item)
        self._selected_mark.clear()

    def update(self):
        self.clear()
        if self.editor.selected_node:
            proxy = self.editor.module_proxy.proxy_for_node(self.editor.selected_node)
            targets = proxy.instances if proxy else [self.editor.selected_node]
            color = Color(selected_color)
            color.alpha = 70
            for target in targets:
                rect = Highlight(target, self.holder, background_color=color)
                self.holder.add(rect)
                self._selected_mark.append(rect)
        if self.editor.active_node:
            proxy = self.editor.module_proxy.proxy_for_node(self.editor.active_node)
            targets = proxy.instances if proxy else [self.editor.active_node]
            color = Color(active_color)
            color.alpha = 70
            for target in targets:
                rect = Highlight(target, self.holder, background_color=color)
                self.holder.add(rect)
                self._active_mark.append(rect)
