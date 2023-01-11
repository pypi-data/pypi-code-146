from types import SimpleNamespace

from p3ui import *
from p3ui.element import Icons


#
# TODO: create with editor itself ..
class TemplateTreeTemplate(Row):

    def __init__(self):
        super().__init__(
            height=(1 | em, 4, 1),
            padding=(2 | px, 2 | px),
            align_items=Alignment.Stretch,
            children=[
                tree_view := ScrolledColumn(),
                Column(
                    width=(auto, 0, 1),
                    justify_content=Justification.Start,
                    padding=(0 | px, 0 | px),
                    children=[
                        add_node_button := Button(
                            width=(auto, 0, 0),
                            height=(auto, 0, 0),
                            label=f'{Icons.Add}'
                        ),
                        Spacer(height=(1 | em, 0, 0)),
                        move_up_button := Button(
                            width=(auto, 0, 0),
                            height=(auto, 0, 0),
                            label=f'{Icons.ArrowUpward}'
                        ),
                        move_down_button := Button(
                            width=(auto, 0, 0),
                            height=(auto, 0, 0),
                            label=f'{Icons.ArrowDownward}'
                        ),
                        Spacer(height=(1 | em, 0, 0)),
                        cut_button := Button(
                            width=(auto, 0, 0),
                            height=(auto, 0, 0),
                            label=f'{Icons.ContentCut}'
                        ),
                        copy_button := Button(
                            width=(auto, 0, 0),
                            height=(auto, 0, 0),
                            label=f'{Icons.ContentCopy}'
                        ),
                        paste_button := Button(
                            width=(auto, 0, 0),
                            height=(auto, 0, 0),
                            label=f'{Icons.ContentPaste}'
                        ),
                        Spacer(height=(1 | em, 1, 0)),
                        delete_button := Button(
                            width=(auto, 0, 0),
                            height=(auto, 0, 0),
                            label=f'{Icons.Delete}'
                        ),
                        Spacer(height=(1 | em, 0, 0))
                    ]
                )
            ]
        )
        self.unique = SimpleNamespace()
        self.unique.tree_view = tree_view
        self.unique.add_node_button = add_node_button
        self.unique.move_down_button = move_down_button
        self.unique.move_up_button = move_up_button
        self.unique.delete_button = delete_button
        self.unique.cut_button = cut_button
        self.unique.copy_button = copy_button
        self.unique.paste_button = paste_button
