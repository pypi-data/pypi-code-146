from p3ui import ScrollArea, Column, px, percent, auto


class ScrolledColumn(ScrollArea):

    def __init__(self, **kwargs):
        self.column = Column(
            width=(auto, 0, 0),
            height=(auto, 0, 0),
            spacing=0 | px,
            padding=(0 | px, 0 | px),
            on_resize=self._on_resize,
            children=kwargs.pop('children', [])
        )
        super().__init__(
            padding=(0 | px, 0 | px),
            content=self.column,
            on_resize=self._on_resize,
            **kwargs
        )

    def _on_resize(self, _):
        """ this is a workaround until there's a min-size attribute """
        _, _, crw, crh, bar = self.content_region
        h = self.column.minimum_content_height
        if h >= crh:
            crw -= bar
        actual = max([0] + [child.minimum_content_width for child in self.column.children])
        self.column.width = (crw | px, 0, 0) if actual < crw else (auto, 0, 0)

    def clear(self):
        self.column.clear()

    @property
    def children(self):
        return self.column.children

    @children.setter
    def children(self, children):
        self.column.children = children

    def add(self, node):
        self.column.add(node)

    def remove(self, node):
        self.column.remove(node)
