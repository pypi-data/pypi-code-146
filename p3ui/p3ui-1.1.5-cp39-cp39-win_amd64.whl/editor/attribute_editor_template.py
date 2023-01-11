from types import SimpleNamespace

from p3ui import *


class AttributeEditorTemplate(Column):

    def __init__(self):
        super().__init__(
            padding=(0.618 | em, 0.618 | em),
            width=(24 | em, 0, 0),
            align_items=Alignment.Stretch,
            justify_content=Justification.Start,
            children=[
                Text('Node Editor:'),
                scrolled_column := ScrolledColumn()
            ]
        )
        self.unique = SimpleNamespace()
        self.unique.scrolled_column = scrolled_column
